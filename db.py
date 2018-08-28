#coding=utf-8

import sys
import time
from multiprocessing import Pool

'''
set pagesize 0
spool "a.txt"
select table_name from user_tables where (table_name like 'MESSAGESTORE_%' or table_name like 'MSGIDX_PART_%') and table_name like '%BAK%';
spool off;
exit

python -c "for l in open('a.txt'): t=l.strip(); print 'drop table %s;'%(t, )" >t.sql




查看表空间使用情况:
SELECT NVL(b.tablespace_name,nvl(a.tablespace_name,'UNKOWN')) name,
     ((Mbytes_alloc-NVL(Mbytes_free,0))/Mbytes_alloc)*100   pct_used, Mbytes_free, Mbytes_alloc as Total
     FROM   ( SELECT   SUM(bytes)/1024/1024 as Mbytes_free
                     , MAX(bytes)/1024 largest
                     , tablespace_name
              FROM sys.dba_free_space
              GROUP BY tablespace_name
            ) a
          , ( SELECT   SUM(bytes)/1024/1024 as Mbytes_alloc
                     , tablespace_name
              FROM sys.dba_data_files
              GROUP BY tablespace_name
            ) b
     WHERE a.tablespace_name (+) = b.tablespace_name;
'''

from local_db import conndb

tw = 3600 * 24 * 14  # 两周的秒数
index_count = 200
body_count = 1000

def _proc_init():
    global db
    global cur
    db, cur = conndb()
def _sub_proc(tbl):
    t = time.time()
    cur.execute("truncate table %s" % tbl)
    cur.execute("drop table %s" % tbl)
    t1 = time.time()
    print "%s done %.3f" % (tbl, t1-t)
    return 1

def mult_proc():
    print 'begin...'
    tables = [t.strip() for t in open("a.txt") if t.find('BAK')>0 ]
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    ret = pool.map(_sub_proc, tables)
    pool.close()

    for lst in ret:
        pass

# 把所有未消费的消息, 从备份表中捞出来放到当前表中
#
def sel_un_msg():
    src = "bak_"
    db, cur = conndb()
    cur1 = db.cursor()
    msgid_file = "mdgidx.txt"
    fo = open(msgid_file, "w")
    for i in range(200):
        sql = "select idmm_msg_id, dst_cli_id, dst_topic_id from msgidx_part_{1}{0} where commit_time=0".format(i, src)
        cur.execute(sql)
        c = 0
        for r in cur.fetchall():
            fo.write("{0} {1} {2}\n".format(*r))
            sql_ins = "insert into msgidx_part_{0} " \
                      "select idmm_msg_id,produce_cli_id,src_topic_id,dst_cli_id,dst_topic_id,src_commit_code,group_id,priority ," \
                      "idmm_resend ,consumer_resend ,create_time ,broker_id ,req_time ,commit_code ,commit_time ,commit_desc ," \
                      "next_topic_id ,next_client_id ,expire_time,to_char(sysdate, 'dd')" \
                      " from msgidx_part_{1}{0} where idmm_msg_id=:v1 and dst_cli_id=:v2 and dst_topic_id=:v3".format(i, src)
            cur1.execute(sql_ins, r)
            c += 1
        db.commit()
        print "idx {0} == count {1}".format(i, c)
    fo.close()

    ids = [l.split()[0].strip() for l in open(msgid_file) if len(l) > 10]
    c = 0
    for id in ids:
        td = id.split("::")[-1]
        sql = "insert into messagestore_{0} select id, properties, systemproperties, content, createtime, to_char(sysdate,'dd')" \
              " from messagestore_{1}{0} where id=:v1".format(td, src)
        try:
            cur1.execute(sql, (id, ))
            db.commit()
            c += 1
        except Exception,e:
            print e, id
        if c % 100 == 0:
            print " {0} / {1} ".format(c, len(ids))
    cur.close()
    cur1.close()
    db.close()

# 每个小时记录下数据库表空间的使用情况, 用于监控
# python -c "import db; db.tablespace_mon()"
def tablespace_mon():
    print time.strftime("%Y%m%d%H%M%S")
    sql = '''SELECT NVL(b.tablespace_name,nvl(a.tablespace_name,'UNKOWN')) name,
     ((Mbytes_alloc-NVL(Mbytes_free,0))/Mbytes_alloc)*100   pct_used, Mbytes_free, Mbytes_alloc as Total
     FROM   ( SELECT   SUM(bytes)/1024/1024 as Mbytes_free
                     , MAX(bytes)/1024 largest
                     , tablespace_name
              FROM sys.dba_free_space
              GROUP BY tablespace_name
            ) a
          , ( SELECT   SUM(bytes)/1024/1024 as Mbytes_alloc
                     , tablespace_name
              FROM sys.dba_data_files
              GROUP BY tablespace_name
            ) b
     WHERE a.tablespace_name (+) = b.tablespace_name'''
    db, cur = conndb()
    cur.execute(sql)
    for r in cur.fetchall():
        tname = r[0]
        if tname.find("IDMMDB") < 0:
            continue
        print "{0}\t{1:.3f}%\t{2:.0f}MB\t{3:.0f}MB".format(*r)
    cur.close(); db.close()


def _sub_proc_statics(args):
    i, topic, cli, bg, ed = args
    t = time.time()
    sql = "select  create_time, commit_time, idmm_msg_id from msgidx_part_{0} where dst_topic_id=:v1 and dst_cli_id=:v2 and commit_time between :v3 and :v4"
    cur.execute(sql.format(i), (topic, cli, bg, ed))
    ret = ["%d %d %d %d %s\n" % (r[0]/1000/60, r[1]/1000/60, r[0], r[1], r[2]) for r in cur.fetchall()]
    t1 = time.time()
    print "%s done %.3f" % (i, t1-t)
    return ret

# python -c "import db; db.ctime_statics()" T101Order2PrmDest-B	Sub117Prm "2018-08-22 16:00:00" "2018-08-22 16:30:00"
# cat out.txt|awk '{print $1}'|sort|uniq -c
# cat out.txt|awk '{print $2}'|sort|uniq -c
from tm import tmstr
def ctime_statics():
    if len(sys.argv) < 5:
        print "Usage: <topic> <cli> <begin_time> <end_time>"
        return

    topic, cli, bg, ed = sys.argv[1], sys.argv[2], tmstr(sys.argv[3]), tmstr(sys.argv[4])
    args = [(i, topic, cli, bg, ed) for i in range(200)]
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    ret = pool.map(_sub_proc_statics, args)

    f = open("out.txt", "w")
    for r in ret:
        for line in r:
            f.write(line)
    f.close()

def del_topic_idx_subproc(args):
    i, topic, cli = args
    sql = "delete msgidx_part_{0} where dst_topic_id=:v1 and dst_cli_id=:v2".format(i)
    cur.execute(sql, (topic, cli))
    numrows = cur.rowcount
    print "table %d rows %d"%(i, numrows)
    db.commit()
    return numrows, i
# 指定消费主题 删除索引表数据, 后续需要手工jmx重新加载内存数据
# python -c "import db; db.del_topic_idx('T101OrderStateSynDest-A', 'Sub103')"
# python -c "import db; db.del_topic_idx('T101OrderStateSynDest-B', 'Sub103')"
# curl http://10.113.181.87:8712/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/reload/Sub103/T101OrderStateSynDest-A
def del_topic_idx(topic, cli):
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    args = [(i, topic, cli) for i in range(200)]
    ret = pool.map(del_topic_idx_subproc, args)
    for numrows, i in ret:
        pass # print numrows, i


def check_unconsume_2w_subproc(args):
    tm, i = args
    #db, cur = conndb()
    cur.execute("select dst_topic_id, dst_cli_id, count(*) from msgidx_part_%d"
                " where create_time<:tm and commit_time=0"
                " group by dst_topic_id, dst_cli_id" % (i,),
                (tm,))
    ret = [("%s,%s" % (r[0], r[1]), r[2]) for r in cur.fetchall()]
    # cur.close()
    # db.close()
    return ret

# 检查是否有超过2周未消费的消息, 打印出主题
# python -c "import db; db.check_unconsume_2w()"
def check_unconsume_2w():
    print ' Checking unconsumed message created 2 weeks ago...'
    tm = int( ( time.time()-tw) * 1000)
    kv = {}
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    args = [(tm, i) for i in range(index_count)]
    ret = pool.map(check_unconsume_2w_subproc, args)
    pool.close()

    for lst in ret:
        for k, v in lst:
            kv[k] = kv.get(k, 0) + v

    print 'result: ---'
    for k, v in kv.items():
        print k, v

# 获取各主题未消费消息 最小和最大创建时间 和数量
# python -c "import db; db.check_unconsumed()"
def check_unconsumed_subproc(args):
    i,  = args
    sql = "select dst_topic_id, dst_cli_id, min(create_time), max(create_time), count(*) from msgidx_part_{0} where commit_time=0" \
          " group by dst_topic_id, dst_cli_id".format(i)
    cur.execute(sql, )
    rows = cur.fetchall()
    return rows
def check_unconsumed():
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    args = [(i, ) for i in range(index_count)]
    ret = pool.map(check_unconsumed_subproc, args)
    topics = {}
    for rows in ret:  #合并结果集
        for r in rows:
            k = r[0] + "@" + r[1]
            if topics.has_key(k):
                t = topics[k]
                t1 = (r[2], r[3], r[4])
                if(t[0] > t1[0]): t = (t1[0], t[1], t[2])
                if(t[1] < t1[1]): t = (t[0], t1[1], t[2])
                t = (t[0], t[1], t[2]+t1[2])
                topics[k] = t
            else:
                topics[k] = (r[2], r[3], r[4])
    for k, t in topics.items():
        print tmstr(str(t[0])), tmstr(str(t[1])), t[2], k

# delete后, 表的存储释放   python -c "import db; db.freetablestore()"
# select segment_name, segment_type, sum(bytes)/1024/1024 Mbytese
# from user_segments where  segment_name = 'MESSAGESTORE_BAK_7'
#  group by segment_name, segment_type
def freetablestore():
    tables = ['MESSAGESTORE_BAK_%d'%i for i in range(1000)]
    tables.extend(['MSGIDX_PART_BAK_%d'%i for i in range(200)])
    db, cur = conndb()
    for tbl in tables:
        cur.execute("select sum(bytes)/1024/1024 Mbytese from user_segments where  segment_name =:v1", (tbl, ) )
        sz_mb = cur.fetchone()[0]
        t1 = time.time()
        cur.execute("select INDEX_NAME from USER_INDEXES where table_name =:v1 and INDEX_NAME not like '%$$'", (tbl, ))
        idx = [r[0] for r in cur.fetchall()]
        cur.execute("alter table {0} move tablespace TBS_IDMMDB_DATA".format(tbl))
        for ii in idx:
            cur.execute("alter index %s rebuild" % ii)
        cur.execute("select sum(bytes)/1024/1024 Mbytese from user_segments where  segment_name =:v1", (tbl,))
        sz_mb1 = cur.fetchone()[0]
        t2 = time.time()
        print "table %s size from %d MB to %d MB  time: %.3f"%(tbl, sz_mb, sz_mb1, t2-t1)
    cur.close()
    db.close()

if __name__ == '__main__':
    mult_proc()
