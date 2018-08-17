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
# python -c "import db; db.sel_un_msg()"
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


if __name__ == '__main__':
    mult_proc()
