#coding=utf-8

'''

-- 查看表占用的空间

COLUMN size_mb      FORMAT '999,999,990.0'
COLUMN num_rows     FORMAT '999,999,990'
COLUMN fmt_short    FORMAT A24


COLUMN owner        FORMAT A16
COLUMN table_name   LIKE fmt_short
COLUMN tablespace_name  LIKE fmt_short

SET LINESIZE 200
SET AUTOTRACE OFF

COMPUTE SUM OF size_mb ON REPORT
BREAK ON REPORT

SELECT
    lower( owner )      AS owner
    ,lower(table_name)  AS table_name
    ,tablespace_name
    ,num_rows
    ,blocks*8/1024      AS size_mb
    ,pct_free
    ,compression
    ,logging
FROM    all_tables
WHERE   owner           LIKE UPPER('&1')
OR  owner           = USER
ORDER BY 1,2;

CLEAR COMPUTES
CLEAR BREAKS;


-- 查看表索引
select INDEX_NAME, TABLE_OWNER, TABLE_NAME, UNIQUENESS from USER_INDEXES where table_name like 'MSGIDX_PART_1';

or

select INDEX_NAME, TABLE_OWNER, TABLE_NAME, UNIQUENESS from ALL_INDEXES where INDEX_NAME like 'IDX_MSGSTORE_CTIME%';


select table_name, index_name, column_name
 from user_ind_columns
 where table_name = 'MESSAGESTORE_0';

select table_name, index_name, column_name
 from user_ind_columns
 where table_name = 'MSGIDX_PART_99';

'''

'''
数据清理,  保留2周
for i in range(200): print "create index idx_msgpart_ctime_%d on msgidx_part_%d(create_time) tablespace TBS_IDMMDB_IDX;"%(i, i)
for i in range(1000): print "create index idx_msgstore_ctime_%d on messagestore_%d(createtime) tablespace TBS_IDMMDB_IDX;"%(i, i)
'''

import sys
import time
from multiprocessing import Pool, Queue


tw = 3600 * 24 * 14  # 两周的秒数
index_count = 200
body_count = 1000

from local_db import conndb

def _store_one_table(db, cur, sql):
    while True:
        cur.execute(sql)
        rcount = cur.rowcount
        if rcount == 0:
            break
        db.commit()
        print "    ", time.time(), rcount

def _print_min_max(cur, sql, tag=""):
    cur.execute(sql, )
    mn, mx = cur.fetchone()
    mn_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(mn) / 1000))
    mx_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(mx) / 1000))
    print " %s  min_time:" % tag, mn_str, " max_time:", mx_str

def clear_messagestore(tbl_begin, tbl_end):
    db, cur = conndb()
    ctime = int ( (time.time() - tw) * 1000 ) # keep 2 weeks
    sql_tmpl = "delete messagestore_%d where createtime<%d and rownum<10001"
    for i in range(tbl_begin, tbl_end, 1):
        print "--table messagestore_", i
        _print_min_max(cur, "select min(createtime), max(createtime) from messagestore_%d" % i)
        _store_one_table(db, cur, sql_tmpl % (i, ctime))
        _print_min_max(cur, "select min(createtime), max(createtime) from messagestore_%d" % i)

def clear_msgidx(tbl_begin, tbl_end):
    db, cur = conndb()
    ctime = int((time.time() - tw) * 1000)  # keep 2 weeks
    sql_tmpl = "delete msgidx_part_%d where create_time<%d and rownum<10001"
    for i in range(tbl_begin, tbl_end, 1):
        print "--table msgidx_", i
        _print_min_max(cur, "select min(create_time), max(create_time) from msgidx_part_%d" % i)
        _store_one_table(db, cur, sql_tmpl % (i, ctime))
        _print_min_max(cur, "select min(create_time), max(create_time) from msgidx_part_%d" % i)



def _one_table(args):
    sql, tag, n = args
    # db, cur = conndb()
    count = 0
    while True:
        cur.execute(sql)
        rcount = cur.rowcount
        if rcount == 0:
            break
        db.commit()
        print "    %s %d %s %d" %(tag, n, time.time(), rcount )
        count += rcount
    # cur.close()
    # db.close()
    return (tag, n, count)

def clear_tw():
    print "Clearing data created two weeks ago..."
    pool = Pool(processes=20, initializer=_proc_init)
    ctime = int((time.time() - tw) * 1000)  # keep 2 weeks
    sqls = []
    sql_tmpl = "delete messagestore_bak_%d where createtime<%d and rownum<10001"
    for i in range(body_count):
        sqls.append( ( sql_tmpl % (i, ctime), 'body', i ) )
    sql_tmpl = "delete msgidx_part_bak_%d where create_time<%d and rownum<10001"
    for i in range(index_count):
        sqls.append( (sql_tmpl % (i, ctime), 'idx', i ) )
    ret = pool.map(_one_table, sqls)
    for r in ret:
        print r
    pool.close()

# 寻找在 store 中没有但 msgidx 中还未消费的数据
# {"topic":"T101Sreq-B","message-id":"1530136970640::200::10.113.182.147:52942::0::200","priority":4,"client-id":"Pub101","type":"SEND","group":"552553370"}
# select * from messagestore_200 where id='1530136970640::200::10.113.182.147:52942::0::200';
def find_no_store(tbl):
    db, cur = conndb()
    sql_tmpl = "select IDMM_MSG_ID, dst_topic_id, dst_cli_id, create_time, PRODUCE_CLI_ID, SRC_TOPIC_ID from msgidx_part_%d where commit_time=0" % tbl
    cur.execute(sql_tmpl)
    cur1 = db.cursor()
    sql1 = "select id from messagestore_%s where id=:v"
    sql2 = "insert into messagestore_%s(id, properties, SYSTEMPROPERTIES, createtime, content) values(:v1, :v2, '{}', :v3, utl_raw.cast_to_raw('{}'))"
    while True:
        rows = cur.fetchmany(300)
        if rows is None or len(rows) == 0:
            break
        for r in rows:
            id, topic, client, ctime, src_cli, src_topic = r
            tt = id.split("::")[-1]
            cur1.execute(sql1 % tt, (id, ))
            if cur1.fetchone() is None:
                props = '{"topic":"%s","message-id":"%s","priority":4,"client-id":"%s","type":"SEND","group":"1"}' %(
                    src_topic, id, src_cli
                )
                print topic, client, ctime, id, props
                cur1.execute(sql2 % tt, (id, props, ctime))
                db.commit()
    cur1.close()
    cur.close()
    db.close()


def _proc_init():
    global db
    global cur
    db, cur = conndb()
def _check_proc(args):
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
def check_unconsume_2w():
    print ' Checking unconsumed message created 2 weeks ago...'
    tm = int( ( time.time()-tw) * 1000)
    kv = {}
    n_proc = 20
    pool = Pool(processes=n_proc, initializer=_proc_init)
    args = [(tm, i) for i in range(index_count)]
    ret = pool.map(_check_proc, args)
    pool.close()

    for lst in ret:
        for k, v in lst:
            kv[k] = kv.get(k, 0) + v

    print 'result: ---'
    for k, v in kv.items():
        print k, v


def check_min_tm():
    db, cur = conndb()
    for i in range(index_count):
        _print_min_max(cur, "select min(create_time), max(create_time) from msgidx_part_%d" % i, "idx-%d"%i)

    for i in range(body_count):
        _print_min_max(cur, "select min(createtime), max(createtime) from messagestore_%d" % i, 'body-%d'%i)
    cur.close(); db.close()


def main():
    clear_msgidx(0, index_count)
    clear_messagestore(0, body_count)

if __name__ == '__main__':
    #main()
    if len(sys.argv) < 2:
        print "  Usage: %s <clear|check>"
        print "    check:  检查2周前仍未消费的消息的主题和消息数量"
        print "    clear:  删除2周前的数据(包括索引和body)"
        exit(0)
    cmd = sys.argv[1]
    if cmd == 'clear':
        clear_tw()
        import db as dblib
        dblib.freetablestore()
    elif cmd == 'check':
        check_unconsume_2w()

    #find_no_store(int(sys.argv[1]))
    #check_unconsume_2w()
    pass
