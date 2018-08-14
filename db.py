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

'''

def conndb():
    import cx_Oracle  #idmmopr/ykRwj_b6@billyzdb
    db = cx_Oracle.connect('idmmopr', 'ykRwj_b6', 'billyzdb')
    cur = db.cursor()
    return db, cur

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



if __name__ == '__main__':
    mult_proc()
