#!/usr/bin/env python
# coding= UTF-8

# 从oracle 库中查询消息体的全部信息, 包括body内容

import string
import time
import sys
import json
from tm import tmstr
from multiprocessing import Pool

from local_db import conndb

def _print_tmstr(t):
    print "  %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)/1000))

def _print_tm(s):
    print " %d" % (time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S"))*1000, )

def tm():
    if len(sys.argv) < 2:
        print "give me a time"
    else:
        s = sys.argv[1]
        if s.find(':') > 0:
            _print_tm(s)
        else:
            _print_tmstr(s)

def _proc_init():
    global db
    global cur
    db, cur = conndb()

# 查询单个消息,  分别从索引表 错误表 和 body表查,  如果遇到压缩的content, 则保存到文件中
def selid():
    id = sys.argv[1]
    ii = id.split("::")

    db, cur = conndb()

    print '--index:'
    sql="select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, commit_time-create_time, consumer_resend from msgidx_part_%s where idmm_msg_id=:v" %ii[-2]
    cur.execute(sql, (id, ))
    for row in cur.fetchall():
        print row
    sql="select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, commit_time-create_time, consumer_resend from msgidx_part_bak_%s where idmm_msg_id=:v" %ii[-2]
    cur.execute(sql, (id, ))
    for row in cur.fetchall():
        print row

    print '--error:'
    sql="select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, consumer_resend from msgidx_part_err where idmm_msg_id=:v"
    cur.execute(sql, (id, ))
    for row in cur.fetchall():
        print row

    print '--body:'
    id, props, content = _selcontent(cur, id)
    if id is not None:
        print id, props, content
    # sql="select id, properties, content from messagestore_%s where id=:v" %ii[-1]
    # cur.execute(sql, (id, ))
    # row = cur.fetchone()
    # if row is not None:
    #     prop = json.loads(row[1])
    #     content = row[2].read()
    #     if prop.has_key('compress') and prop['compress'] == True:
    #         file('content.gz', 'w').write(content)
    #         content = '[[compressed]] content.gz'
    #     print row[0], row[1], content

    db.close()

def qryid_web(id, out):
    db, cur = conndb()
    print "--1", time.time()

    try:
        ii = id.split("::")
        d_date = tmstr(ii[0])[8:10]
        out.write("<p/> ----index:<br />")
        out.write("<b>Cols</b>: idmm_msg_id, dst_cli_id,dst_topic_id, create_time, commit_time-create_time, consumer_resend <br />")
        cur.execute("""select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, commit_time-create_time,
        consumer_resend from msgidx_part_%s partition (P_%s) where idmm_msg_id=:v1""" % (ii[-2], d_date), (id, ) )
        for row in cur.fetchall():
            out.write(", ".join([ str(f) for f in row] ) )
            out.write("\n<br />   创建时间: %s" % tmstr(str(row[3])))
            out.write("<br />   消费提交时间: %s" % tmstr(str(row[4]+row[3])))
        print "--2", time.time()

        out.write("<p/> ----error:<br />")
        out.write("<b>Cols</b>: idmm_msg_id, dst_cli_id,dst_topic_id, create_time, consumer_resend <br />")
        cur.execute("select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, 0, consumer_resend from msgidx_part_err where idmm_msg_id=:id",
                    (id, ) )
        for row in cur.fetchall():
            out.write(" , ".join([str(f) for f in row]))
            out.write("<br />创建时间: %s" % tmstr(row[3]))
        print "--3", time.time()

        out.write("<p/> ----body:<br />\n")
        id, props, content = _selcontent(cur, id, d_date)
        if id is not None:
            out.write("<br /> <b>ID:</b>")
            out.write(id)
            out.write("<br /> <b>Properties:</b>")
            out.write(props)
            out.write("<br /> <b>Content:</b>")
            out.write(content)
        print "--4", time.time()
    except Exception,x:
        print x
        out.write("<pre>")
        out.write(x)
        out.write("</pre>")
    cur.close()
    db.close()

import gzip
from StringIO import StringIO

def gz(s):
    out = StringIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(s)
    return out.getvalue()

def gzu(s):
    return gzip.GzipFile(fileobj=StringIO(s)).read()

# 取单个消息的content内容, 遇到 gz 的body, 则解压
def _selcontent(cur, id, partition=""):
    ii = id.split("::")
    if partition != "":
        partition = "partition (P_%s)"%partition
    sql = "select id, properties, content from messagestore_%s %s where id=:v" % (ii[-1], partition)
    cur.execute(sql, (id,))
    row = cur.fetchone()
    # if row is None:
    #     sql = "select id, properties, content from messagestore_bak_%s where id=:v" % ii[-1]
    #     cur.execute(sql, (id,))
    #     row = cur.fetchone()
    if row is not None:
        prop = json.loads(row[1])
        content = row[2].read()
        if prop.has_key('compress') and prop['compress'] == True:
            content = gzu(content)
        return row[0], row[1], content
    return None, None, None


def sel_orderid_err(topic, client, tag):
    db, cur = conndb()
    cur.execute('select IDMM_MSG_ID from msgidx_part_err where DST_TOPIC_ID=:v1 and DST_CLI_ID=:v2', (topic, client))
    for (id,) in cur.fetchall():
        #print id
        _, _, content = _selcontent(cur, id)
        p = content.find(tag)
        if p < 0:
            print id, '-----not found', tag
        else:
            p1 = content.find(',', p)
            print topic, id, content[p:p1]
    cur.close()
    db.close()

# 从err表中把指定主题的消息body取出来放文件
# python -c "import selid1; selid1.sel_msgbody_err('T101Order2PrmDest-B','Sub117Prm','T101Order2PrmDest-B.txt')"
def sel_msgbody_err(topic, client, outfile):
    db, cur = conndb()
    cur.execute('select IDMM_MSG_ID from msgidx_part_err where DST_TOPIC_ID=:v1 and DST_CLI_ID=:v2', (topic, client))
    f = open(outfile, "w")
    for (id,) in cur.fetchall():
        #print id
        _, _, content = _selcontent(cur, id)
        f.write(id)
        f.write('\n')
        #print type(content)
        if content is None:
            f.write("\"[not found]\"")
        else:
            f.write(content)
        f.write('\n')
    f.close()
    cur.close()
    db.close()

#取单个主题的索引数据
def dumpTopcIndexs(topic, client, outfile):
    db, cur = conndb()
    fo = open(outfile, "w")
    for i in range(200):
        print 'table--', i
        ct = 0
        cur.execute('select idmm_msg_id, create_time, group_id, priority from msgidx_part_%d where DST_TOPIC_ID=:v1 and DST_CLI_ID=:v2' % i, (topic, client))
        while True:
            rows = cur.fetchmany(300)
            if rows is None or len(rows) == 0:
                break
            ct += len(rows)
            for r in rows:
                fo.write("%s %d %s %d\n"%( r[0], r[1], r[2], r[3] ))
        print '   rows: ', ct
    fo.close()
    db.close()

# 读取配置表中的主题对应关系到文件中
def get_mapping(fname="mapping.txt"):
    import os
    os.putenv("NLS_LANG", "American_America.zhs16gbk")
    sql = '''select a.client_id as pub_client,
       a.src_topic_id,
       a.note as src_note,
       b.attribute_key,
       b.attribute_value,
       c.client_id as sub_client,
       c.dest_topic_id,
       c.note as dst_note
  from topic_publish_rel_5   a,
       topic_mapping_rel_5   b,
       topic_subscribe_rel_5 c
 where  -- c.dest_topic_id = 'Test01Dest-A' and
   c.dest_topic_id = b.dest_topic_id
   and a.src_topic_id = b.src_topic_id
    '''
    db, cur = conndb()
    cur.execute(sql)
    f = open(fname, "w")
    for r in cur.fetchall():
        f.write(" ".join([str(k).strip() for k in r]))
        f.write("\n")
    f.close()
    cur.close()
    db.close()

# 获取每个表的空间使用情况
def get_table_space_used(fname="tables.txt"):
    db, cur = conndb()
    sql = """SELECT
    lower(table_name)  AS table_name
    ,tablespace_name
    ,num_rows
    ,blocks*8/1024      AS size_mb
    ,pct_free
    ,compression
    ,logging
FROM    user_tables
ORDER BY 1,2
    """   # all_tables
    f = open(fname, "w")
    cur.execute(sql)
    f.write(" ".join([d[0] for d in cur.description]) )
    f.write("\n")
    for r in cur.fetchall():
        f.write(" ".join([str(ff).strip() for ff in r]))
        f.write('\n')
    f.close()
    db.close()

def selids(fname):
    db, cur = conndb()
    for line in open(fname):
        flds = line.split()
        if len(flds) < 2: continue
        id = flds[1]
        ii = id.split("::")

        sql="select idmm_msg_id, dst_cli_id,dst_topic_id, group_id from msgidx_part_%s where idmm_msg_id=:v" %ii[-2]
        cur.execute(sql, (id, ))
        r = cur.fetchone()
        if r is None:
            print "[[[[not found]]]]", id
        else:
            print r[0], r[1], r[2], r[3]
    cur.close()
    db.close()


import re
# 按主题 和 时间取消息体中的局部数据
# python -c "import selid1; selid1.dumpTopcByTime('T103DataSynBOSSADest-A', 'Sub109DataSyn', '2018-09-05 06:30:00', '2018-09-05 10:10:00', 'T103DataSynBOSSADest-A.out')"
# python -c "import selid1; selid1.dumpTopcByTime('T103DataSynBOSSBDest-B', 'Sub109DataSyn', '2018-09-12 16:30:00', '2018-09-12 17:20:00', 'a.out')"
#
# python tm.py "2018-09-05 12:00:00"
# cat T103DataSynBOSSADest-A.out.id|awk '{if($4> 1536120000000) print $0}'
def dumpTopcByTime_sub(args):
    i, topic, client, t1, t2, status, patterns = args
    global cur
    patterns = [ re.compile(f.strip()) for f in patterns.split("\r\n")]
    # rr = re.compile(",\"PHONE_NO\":\"([\\d]+)\",")
    # rr1 = re.compile(',\"ServiceNo\":\"([\\d]+)\",')
    msg_stat = ""
    if status=="1": msg_stat = ""  # all
    elif status == "2": msg_stat=" and commit_time=0"
    elif status == "3": msg_stat="and commit_time>0"
    sql = 'select idmm_msg_id, group_id, create_time, commit_time from msgidx_part_%d where DST_TOPIC_ID=:v1 and DST_CLI_ID=:v2 and create_time between :v3 and :v4 %s' %( i, msg_stat)
    print sql
    cur.execute(sql,  (topic, client, t1, t2))
    ct = 0
    ret = []
    for r in cur.fetchall():
        ct += 1
        id = r[0]
        body = _selcontent(cur, id)
        body = body[2]
        ph = "[not found]"
        if body is not None:
            for rr in patterns:
                r = rr.search(body)
                if r is not None:
                    ph = r.group(1)
                    break
        ret.append("%s %s" % (id, ph))
    print 'table--', i, ct
    return ret
def dumpTopcByTime(topic, client, tm_begin, tm_end, status, patterns, table_count):
    n_proc = 20
    db, cur = conndb()
    t1 = tmstr(tm_begin)
    t2 = tmstr(tm_end)
    args = [(i, topic, client, int(t1), int(t2), status, patterns) for i in range(table_count)]
    pool = Pool(processes=n_proc, initializer=_proc_init)
    ret = pool.map(dumpTopcByTime_sub, args)
    result = []
    for r in ret:
        result.extend(r)
    return result

# python selid1.py seltopic T101RptOrderLineDest-B Sub111RptOrderLine T101RptOrderLineDest-B.txt
# python -c "import selid1 as s; s.get_mapping('mapping.txt')"
# python -c "import selid1 as s; s.get_table_space_used('tables.txt')"
if __name__ == '__main__':
    if len(sys.argv) > 4 and sys.argv[1] == 'seltopic':
        dumpTopcIndexs(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) > 2 and sys.argv[1] == 'byfile':
        selids(sys.argv[2])
    else:
        selid()
    #sel_orderid_err('T101SmspDest-B', 'Sub113Order', '"crmOrderId"')
    #sel_orderid_err('T109SmspDest-B', 'Sub113Credit', '"orderId"')
    #sel_orderid_err('T105DataBatchSynDest-B',  'Sub113DataBatchSyn', '"WORK_ITEM_ID"')


