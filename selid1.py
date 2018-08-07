#!/usr/bin/env python
# coding= UTF-8

# 从oracle 库中查询消息体的全部信息, 包括body内容

import string
import time
import cx_Oracle
import sys
import json


# def conndb():
#     #import data_decrypt
#     #passwd=data_decrypt.decryptData_auth()
#     # IDMMOPR/ykRwj_b6@idmmdb1
#     passwd = 'ykRwj_b6'
#     db=cx_Oracle.connect('idmmopr',passwd,'idmmdb2')
#     cur=db.cursor()
#     return db, cur

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

    print '--error:'
    sql="select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, consumer_resend from msgidx_part_err where idmm_msg_id=:v"
    cur.execute(sql, (id, ))
    for row in cur.fetchall():
        print row

    print '--body:'
    sql="select id, properties, content from messagestore_%s where id=:v" %ii[-1]
    cur.execute(sql, (id, ))
    row = cur.fetchone()
    if row is not None:
        prop = json.loads(row[1])
        content = row[2].read()
        if prop.has_key('compress') and prop['compress'] == True:
            file('content.gz', 'w').write(content)
            content = '[[compressed]] content.gz'
        print row[0], row[1], content

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
def _selcontent(cur, id):
    ii = id.split("::")
    sql = "select id, properties, content from messagestore_%s where id=:v" % ii[-1]
    cur.execute(sql, (id,))
    row = cur.fetchone()
    if row is not None:
        prop = json.loads(row[1])
        content = row[2].read()
        if prop.has_key('compress') and prop['compress'] == True:
            content = gzu(content)
        return content
    return None

# 替
def sel_orderid_err(topic, client, tag):
    db, cur = conndb()
    cur.execute('select IDMM_MSG_ID from msgidx_part_err where DST_TOPIC_ID=:v1 and DST_CLI_ID=:v2', (topic, client))
    for (id,) in cur.fetchall():
        #print id
        content = _selcontent(cur, id)
        p = content.find(tag)
        if p < 0:
            print id, '-----not found', tag
        else:
            p1 = content.find(',', p)
            print topic, id, content[p:p1]
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

# python selid1.py seltopic T101RptOrderLineDest-B Sub111RptOrderLine T101RptOrderLineDest-B.txt
if __name__ == '__main__':
    if len(sys.argv) > 4 and sys.argv[1] == 'seltopic':
        dumpTopcIndexs(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        selid()
    #sel_orderid_err('T101SmspDest-B', 'Sub113Order', '"crmOrderId"')
    #sel_orderid_err('T109SmspDest-B', 'Sub113Credit', '"orderId"')
    #sel_orderid_err('T105DataBatchSynDest-B',  'Sub113DataBatchSyn', '"WORK_ITEM_ID"')


