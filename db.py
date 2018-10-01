#coding=utf-8

import sys
import os
import time
from multiprocessing import Pool
import cPickle as pickle

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
     
select DEST_TOPIC_ID, CLIENT_ID, NOTE from topic_subscribe_rel_5;    
'''

from local_db import conndb

from functools import wraps
def dbfunc(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        db, cur = conndb()
        try:
            return func(db, cur, *args, **kwargs)
        finally:
            cur.close()
            db.close()
    return func_wrapper

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
     ((Mbytes_alloc-NVL(Mbytes_free,0))/Mbytes_alloc)*100   pct_used, ROUND(Mbytes_free/1024,1) as free, ROUND(Mbytes_alloc/1024,1) as Total
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
        print "{0}\t{1:.3f}%\t{2:.0f}GB\t{3:.0f}GB".format(*r)
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
from tm import tmstr, datedelta
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
            k = r[0] + "," + r[1]
            if topics.has_key(k):
                t = topics[k]
                t1 = (r[2], r[3], r[4])
                if(t[0] > t1[0]): t = (t1[0], t[1], t[2])
                if(t[1] < t1[1]): t = (t[0], t1[1], t[2])
                t = (t[0], t[1], t[2]+t1[2])
                topics[k] = t
            else:
                topics[k] = (r[2], r[3], r[4])
    header = "目标主题 消费者 最小创建时间 最大创建时间 消息数".split()
    _rows = []
    for k, t in topics.items():
        print tmstr(str(t[0])), tmstr(str(t[1])), t[2], k
        tt = k.split(",")
        _rows.append([tt[0], tt[1], tmstr(str(t[0])), tmstr(str(t[1])), t[2]])
    return header, _rows

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
        cur.execute("alter table {0} move tablespace TBS_IDMMDB_IDX".format(tbl))  # TBS_IDMMDB_IDX  TBS_IDMMDB_DATA
        for ii in idx:
            cur.execute("alter index %s rebuild" % ii)
        cur.execute("select sum(bytes)/1024/1024 Mbytese from user_segments where  segment_name =:v1", (tbl,))
        sz_mb1 = cur.fetchone()[0]
        t2 = time.time()
        print "table %s size from %d MB to %d MB  time: %.3f"%(tbl, sz_mb, sz_mb1, t2-t1)
    cur.close()
    db.close()

# 查看表占用空间大小
# python -c "import db; db.table_store_list()"
def table_store_list():
    tables = ['MESSAGESTORE_BAK_%d'%i for i in range(1000)]
    tables.extend(['MSGIDX_PART_BAK_%d'%i for i in range(200)])
    db, cur = conndb()
    for tbl in tables:
        cur.execute("select sum(bytes)/1024/1024 Mbytese from user_segments where  segment_name =:v1", (tbl, ) )
        sz_mb = cur.fetchone()[0]
        cur.execute("select count(*) from %s"%tbl)
        count = cur.fetchone()[0]
        print tbl, sz_mb, count
    db.close()

# 查看表的各分区记录数
# python -c "import db; db.table_part_list()"
def table_part_list():
    headers = "表名 分区名 记录数 记录最小时间 记录最大时间".split()
    rows = []
    db, cur = conndb()
    for tbl, col in (("MESSAGESTORE_0", "createtime"), ("MSGIDX_PART_0", "create_time") ):
        print "====", tbl
        rows.append([tbl, "", "", "", ""])
        for i in range(1,32):
            sql = "select count(*), min(%s), max(%s) from %s partition(P_%02d)"%(col, col, tbl, i)
            cur.execute(sql )
            r = cur.fetchone()
            if r[0] > 0:
                print "    P_%02d"%i, r[0], tmstr(str(r[1])), tmstr(str(r[2]))
                rows.append(["", "P_%02d"%i, r[0], tmstr(str(r[1])), tmstr(str(r[2]))])
            else:
                print "    P_%02d"%i, 0
                rows.append(["", "P_%02d"%i, 0, "", ""])
    db.close()
    return headers, rows

@dbfunc
def table_part_list_sz(db, cur):
    import operator
    headers = "表名 分区名 占用空间大小(MB)".split()
    rows = []
    for tbl in ("MESSAGESTORE_0", "MSGIDX_PART_0" ):
        print "====", tbl
        rows.append([tbl, "", ""])
        cur.execute("select PARTITION_NAME, sum(bytes)/1024/1024 from user_segments where  segment_name =:v1 group by PARTITION_NAME", (tbl, ))
        _r = []
        for r in cur.fetchall():
            _r.append(["", r[0], r[1]])
        _r1 = sorted(_r, key=operator.itemgetter(1))
        rows.extend(_r1)
    return headers, rows

# python -c "import db; db.msgcountDate('2018-09-03 00:00:00', '2018-09-04 00:00:00')" |sort >9.3
# python -c "import db; db.msgcountDate('2018-09-02 00:00:00', '2018-09-03 00:00:00')" |sort >9.2
# python -c "import db; db.msgcountDate('2018-09-04 00:00:00', '2018-09-05 00:00:00')" |sort >9.4
# python -c "import db; db.msgcountDate('2018-09-01 00:00:00', '2018-09-02 00:00:00')" |sort >9.1
# python -c "import db; db.msgcountDate('2018-09-05 00:00:00', '2018-09-06 00:00:00')" |sort >9.5
def msgcountDate(beg_time, end_time):
    #
    t1 = tmstr(beg_time)
    t2 = tmstr(end_time)
    db, cur = conndb()
    sql = "select round(create_time/60000), count(*) from msgidx_part_{0} where create_time between :v1 and :v2 group by round(create_time/60000)"
    cur.execute(sql.format("0"), (t1, t2))
    for r in cur.fetchall():
        t = tmstr(str(int(r[0]) * 60000))[11:16]
        c = int(r[1]) * 200
        print t, c
    cur.close()
    db.close()

#按日 和 主题 统计消息的消费时间和数量
# python -c "import db; db.stastics(-1)"
def stastics_subproc(args):
    global cur
    i, part = args
    t1 = time.time()
    sql = """select dst_topic_id, dst_cli_id, count(*), round(avg(commit_time-create_time)), max(commit_time-create_time), min(commit_time-create_time)
      from msgidx_part_%d partition (p_%s) where commit_time>0
      group by dst_topic_id, dst_cli_id""" % (i, part)
    cur.execute(sql, )
    rows = cur.fetchall()
    print i, time.time()-t1
    return rows
def stastics(n, topics=None):
    st_date = datedelta(n)
    part = st_date[-2:]
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    args = [(i, part) for i in range(index_count)]
    ret = pool.map(stastics_subproc, args)
    pool.close()
    result = {}
    for rows in ret:
        for r in rows:
            k = ",".join(r[:2])
            c, a, mx, mn = r[2:]
            if result.has_key(k):
                l = result.get(k)
                l[0] += c
                l[1] = (l[1] + a) / 2
                if mx > l[2]: l[2]=mx
                if mn < l[3]: l[3]=mn
                result[k] = l
            else:
                result[k] = [c, a, mx, mn]
    if topics is None:
        header = 'topic,count,avg(ms),max(ms),min(ms)'.split(",")
        rows = []
        for k, l in result.items():
            l.insert(0, k)
            rows.append(l)
        return '按主题消息消费时间统计 %s'%st_date, st_date, header, rows
    else:
        header = 'topic,count,avg(ms),max(ms),min(ms),bleid,note'.split(",")
        rows = []
        for k, l in result.items():
            l.insert(0, k)
            nn = topics.get(k, ("[none]", "[none]"))
            l.extend(nn)
            rows.append(l)
        return '按主题消息消费时间统计 %s'%st_date, st_date, header, rows


# python -c "import db; r=db.getTopicsConf('5')"
def getTopicsConf(ver):
    db, cur = conndb()
    sql = """select a.ble_id, b.client_id, a.dest_topic_id, b.max_request, b.min_timeout,
       b.max_timeout,b.consume_speed_limit, b.max_messages, b.warn_messages, b.note
            from BLE_DEST_TOPIC_REL_{0} a, TOPIC_SUBSCRIBE_REL_{0} b
            where a.use_status='1' and b.use_status='1'
            and a.dest_topic_id=b.dest_topic_id """.format(ver,)
    # print sql
    cur.execute(sql)
    ret = {}
    for r in cur.fetchall():
        k = r[2].strip() + "," + r[1].strip()
        note = r[-1]
        if note is not None:
            note = note.decode('gbk').encode('utf-8')
        ret[k] = [r[0], note]  # [bleid, note]
    db.close()
    return ret

#读取全部主题映射数据
@dbfunc
def dumpAllTopicConf(db, cur, verfunc, cache_dir=None):
    header = "生产者 生产主题 映射key 映射value 消费者 消费主题 生产主题备注 消费主体备注".split()
    if cache_dir is not None:
        fpath = "%s/topics_all"%(cache_dir)
        if os.path.exists(fpath):
            st = os.stat(fpath)
            if st.st_mtime + 300.0 > time.time():
                with open(fpath, "rb") as f:
                    (ver, _rows) = pickle.load(f)
                    return ver, header, _rows
    ver = verfunc()
    sql = """select a.client_id, a.src_topic_id, b.attribute_key, b.attribute_value, c.client_id, c.dest_topic_id, a.note, c.note
      from topic_publish_rel_{0} a, topic_mapping_rel_{0} b, topic_subscribe_rel_{0} c 
      where c.dest_topic_id=b.dest_topic_id and a.src_topic_id=b.src_topic_id""".format(ver)
    #db, cur = conndb()
    cur.execute(sql)
    rows =  cur.fetchall()
    #cur.close(); db.close()
    _rows = []
    for r in rows:
        _r = [f for f in r[:-2]]
        if r[-2] != None:
            _r.append(r[-2].decode('gbk').encode('utf-8'))
        else:
            _r.append("")
        if r[-1] != None:
            _r.append(r[-1].decode('gbk').encode('utf-8') )
        else:
            _r.append("")
        _rows.append(_r)
    if cache_dir is not None:
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        with open(fpath, "wb") as f:
            pickle.dump((ver, _rows), f)
    return ver, header, _rows

# 14天前的分区清理
# python -c "import db; db.truncate_part()"
def truncate_part():
    # db, cur = conndb()
    print "begin to truncate partition before 14 days...", time.strftime("%Y-%m-%d,%H:%M:%S")
    part_no = datedelta(-14)[-2:]
    for i in range(body_count):
        sql = "alter table messagestore_%d truncate partition P_%s"%(i, part_no)
        print "  ", sql
    for i in range(index_count):
        sql = "alter table msgidx_part_%d truncate partition P_%s" %(i, part_no)
        print "  ", sql

# 读取excel文件的内容， 保存到文本文件中， utf-8格式
# 生成的文件直接手工改写为 .py,  把里面的内容赋值给python变量, 避免字符编码的问题
def read_topic_excel(out_file):
    from xlrd import open_workbook
    import codecs
    wb = open_workbook(r'E:\all_topics@20180921.xlsx')
    sheet = wb.sheets()[0]
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols
    print number_of_rows, number_of_columns
    with codecs.open(out_file, mode="w", encoding="utf-8") as f:
        for row in range(1, number_of_rows):
            for col in range(number_of_columns):
                value = sheet.cell(row, col).value
                try:
                    #print "%d %d %s"%(row, col, value.decode("gbk").encode("utf-8"))
                    #print row, col, value.replace("\n", "").replace("\r", "")
                    f.write(value.replace("\n", "").replace("\r", ""))
                    f.write('\t')
                except Exception,x:
                    #print row, col, repr(value), "FAIL: %s"%x
                    f.write("\t")
            f.write("\n")

def topic_file():
    import topics_conf as tc
    #from importlib import reload
    reload(tc)
    header = tc.header
    rows = []
    for line in tc.topics_conf.strip().split("\n"):
        line = line.replace("\t\t", "\t&nbsp;\t")
        rows.append(line.strip().split("\t"))
    return header, rows

def gen_bak_sql():
    part_str = "27"
    num_store = 1000
    num_idx = 200
    if len(sys.argv) > 1 and sys.argv[1] == 'insert':
        print "set timing on;"
        print "set AUTOCOMMIT on;"
        print """create table messagestore_daily_{0} tablespace TBS_IDMMDB_IDX as select * from messagestore_0 where 1=2;
    alter table messagestore_daily_{0} nologging;
    create table msgidx_part_daily_{0} tablespace TBS_IDMMDB_IDX as select * from msgidx_part_0 where 1=2;
    alter table msgidx_part_daily_{0} nologging;""".format(part_str)
        for i in range(num_store):
            print "insert into messagestore_daily_%s select * from messagestore_%d partition (p_%s) nologging;" % (
                    part_str, i, part_str)
        for i in range(num_idx):
            print "insert into msgidx_part_daily_%s select * from msgidx_part_%d partition (p_%s) nologging;" % (
                    part_str, i, part_str)
    else:
        print "set timing on;"
        print "set AUTOCOMMIT on;"
        for i in range(num_store): print "alter table messagestore_%d truncate partition p_%s;" % (i, part_str)
        for i in range(num_idx): print "alter table msgidx_part_%d truncate partition p_%s;" % (i, part_str)

'''
    cur.execute("create table messagestore_daily_{0} tablespace TBS_IDMMDB_IDX as select * from messagestore_0 where 1=2".format(part_str))
    cur.execute("alter table messagestore_daily_{0} nologging".format(part_str))
    cur.execute("create table msgidx_part_daily_{0} tablespace TBS_IDMMDB_IDX as select * from msgidx_part_0 where 1=2".format(part_str))
    cur.execute("alter table msgidx_part_daily_{0} nologging".format(part_str))
    for i in range(num_store):
        t1 = time.time()
        cur.execute("insert into messagestore_daily_%s select * from messagestore_%d partition (p_%s) nologging" % (
            part_str, i, part_str) )
        rowcount = cur.rowcount
        cur.execute("alter table messagestore_%d truncate partition p_%s" % (i, part_str) )
        db.commit()
        print "messagestore-%d  %d rows, time: %.3f s"%(i, rowcount, time.time()-t1)
    for i in range(num_idx):
        t1 = time.time()
        cur.execute("insert into msgidx_part_daily_%s select * from msgidx_part_%d partition (p_%s) nologging" % (
            part_str, i, part_str) )
        rowcount = cur.rowcount
        cur.execute("alter table msgidx_part_%d truncate partition p_%s;" % (i, part_str))
        db.commit()
        print "msgidx-%d  %d rows, time: %.3f s" % (i, rowcount, time.time() - t1)

    cur.execute("select sum(bytes)/1024/1024 Mbytese from user_segments where  segment_name =:v1", ('MESSAGESTORE_DAILY_%s'%part_str, ) )
    print "MESSAGESTORE_DAILY_ size in mbytes: %s" % cur.fetchone()[0]
    cur.execute("select sum(bytes)/1024/1024 Mbytese from user_segments where  segment_name =:v1", ('MSGIDX_PART_DAILY_%s'%part_str, ) )
    print "MSGIDX_PART_DAILY_ size in mbytes: %s" % cur.fetchone()[0]
    '''

import subprocess as sb
def shell_exec(cmd):
    try:
        p = sb.Popen(cmd, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
        sout = p.stdout.read()
        serr = p.stderr.read()
        p.terminate()
        return sout, serr, None
    except sb.CalledProcessError, x:
        sys.stderr.write("failed!  return code=%s" % x.returncode)
        return None, x.returncode, x.output

def lexec(cmd, shell=False):
    try:
        output = sb.check_output(cmd, shell=shell)
        return output, None
    except sb.CalledProcessError, x:
        sys.stderr.write("failed!  return code=%s" % x.returncode)
        return None, x.output

def __parted_backup_sub(args):
    dbstr, tbl, part, bak_dir = args
    log_file = open("/idmm/idmm3/log/pp_%d"%os.getpid(), "a")
    log_file.write("%.3f %s %s begin\n"%(time.time(), tbl, part))
    db, cur = conndb(dbstr)
    log_file.write("%.3f %s %s db connected\n"%(time.time(), tbl, part))
    try:
        cur.execute("select sum(bytes)/1024/1024 from user_segments where  segment_name =:v1 and PARTITION_NAME=:v2", (tbl, part) )
        if cur.fetchone()[0] < 1.0:
            print "partition %s - %s is empty"%(tbl, part)
            log_file.write("%.3f %s %s empty return\n" % (time.time(), tbl, part))
            return tbl, part, "0"
        log_file.write("%.3f %s %s empty checked\n" % (time.time(), tbl, part))
        t1 = time.time()
        cmd_str1 = "exp {2} file={3}/{0}.dmp tables={0}:{1} rows=y indexes=n triggers=n grants=n".format(tbl, part, dbstr, bak_dir)
        sout, serr, x = shell_exec(cmd_str1)
        log_file.write("%.3f %s %s done exp\n" % (time.time(), tbl, part))
        if type(serr) == str and serr.find("Export terminated successfully") > 0:
            t2 = time.time()
            cur.execute("alter table %s truncate partition %s" % (tbl, part))
            t3 = time.time()
            log_file.write("%.3f %s %s done truncat\n" % (time.time(), tbl, part))
            sout, _serr, x = shell_exec("gzip {0}/{1}.dmp".format(bak_dir, tbl))
            t4 = time.time()
            print "SUCC: %s \nexp-time: %.3f trunc-time: %.3f gz-time: %.3f %s" %( serr,
                                t2-t1, t3-t2, t4-t3, time.strftime("%Y%m%d-%H%M%S"))
        else:
            print "FAIL: serr: %s\nsout: %s\nx:%s  %s" % (serr, sout, x, time.strftime("%Y%m%d-%H%M%S"))
    except Exception,x:
        print "-----FAIL--%s"%x
        return tbl, part, str(x)
    finally:
        db.close()
        log_file.write("%.3f %s %s db closed\n" % (time.time(), tbl, part))
        log_file.close()
    return tbl, part, "%.3f"%(time.time()-t1)


# 分区表模式备份数据， 使用exp 工具按分区dump出来， 然后把该分区truncate 掉, 并把dump文件gz压缩, 最后上传到 hadoop上
# 备份29天前的分区
# insert 操作大概要30多分钟,   python -c "import db; db.parted_backup(-28)"
# 本地磁盘文件保存3天, hadoop上保留70天
def parted_backup(ndays=-29, keep_on_disk=3, keep_on_hdfs=70):
    import math
    os.putenv('NLS_LANG', 'American_America.zhs16gbk')
    back_date = datedelta(ndays)
    part_str = back_date[-2:]
    num_store = 1000
    num_idx = 200

    bak_dir = "/idmm/msg_bak/%s"%back_date
    lexec("mkdir -p %s"%bak_dir, shell=True)
    from local_db import getconndb_str
    dbstr = getconndb_str()

    args = [(dbstr, 'MESSAGESTORE_%d'%i, 'P_%s'%part_str, bak_dir) for i in range(num_store)]
    args.extend([(dbstr, 'MSGIDX_PART_%d'%i, 'P_%s'%part_str, bak_dir) for i in range(num_idx)])

    n_proc = 20
    print "----BEGIN proc=%d %s" %(n_proc, time.strftime("%Y-%m-%d %H:%M:%S") )
    if n_proc > 1:
        pool = Pool(processes=n_proc)
        ret = pool.map(__parted_backup_sub, args)
        pool.close()
    else:
        ret = [__parted_backup_sub(arg) for arg in args]
    for r in ret: print r
    try:
        print "----END %s" % time.strftime("%Y-%m-%d %H:%M:%S")
        print "-- HDFS upload %s, dir=%s"%( time.strftime("%Y-%m-%d %H:%M:%S"), back_date)
        os.chdir("/idmm/msg_bak")
        sb.check_output("hadoop fs -put %s"%back_date, shell=True)
        print "-- HDFS upload end %s, dir=%s"%( time.strftime("%Y-%m-%d %H:%M:%S"), back_date)
    # if __name__ == '__main__':
    #     import subprocess as sb
    #     import time
    #     import math
    #     back_date = '2018-09-02'
        sout = sb.check_output("hadoop fs -du|grep %s|awk '{print $1}'" % back_date, shell=True)
        sout1 = sb.check_output("du -sk *|grep %s|awk '{print $1}'"%back_date, shell=True)
        sz1 = float(sout.strip())/1024
        sz2 = float(sout1.strip())
        if math.fabs((sz1-sz2)/sz2) < 0.01:  # 比较hdfs和local disk上的同一文件目录体积差异, 小于0.01认为正常
            print "size correct, delete local file ndays=%d-3 " % ndays
            cmd = "rm -rf %s" % ( " ".join([datedelta(ndays-keep_on_disk-i) for i in range(3)]))
            out, err, x = shell_exec(cmd)
            print "cmd=%s\nout=%s\nerr=%s" % (cmd, out, err)
            cmd = "hadoop fs -rm -r %s" % ( " ".join(datedelta(ndays-keep_on_hdfs-i) for i in range(3)))
            out, err, x = shell_exec(cmd)
            print "cmd=%s\nout=%s\nerr=%s"% (cmd, out, err)
        else:
            print "WARN: size incorrect"
    except Exception,x:
        print "fail: %s" % x

    print "----ALL DONE %s" % time.strftime("%Y-%m-%d %H:%M:%S")


def test1():
    cmdstr = "exp idmmopr/ykRwj_b6@idmmdb2 file=/tmp/t1.dmp DIRECT=y BUFFER=2000000 tables=messagestore_4:p_29 rows=y indexes=n triggers=n grants=n"
    sout, serr, x = shell_exec(cmdstr)
    print "SOUT:", sout
    print "SERR:", serr
    print "X:", x

if __name__ == '__main__':
    #mult_proc()
    read_topic_excel("a.txt")
