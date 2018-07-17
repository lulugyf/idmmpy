#!/usr/bin/env python
# coding= UTF-8

# 从oracle 库中查询消息体的全部信息, 包括body内容

import string
import time
import cx_Oracle
import sys
import json


def conndb():
    #import data_decrypt
    #passwd=data_decrypt.decryptData_auth()
    # IDMMOPR/ykRwj_b6@idmmdb1
    passwd = 'ykRwj_b6'
    db=cx_Oracle.connect('idmmopr',passwd,'idmmdb2')
    cur=db.cursor()
    return db, cur

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

if __name__ == '__main__':
    selid()
    #sel_orderid_err('T101SmspDest-B', 'Sub113Order', '"crmOrderId"')
    #sel_orderid_err('T109SmspDest-B', 'Sub113Credit', '"orderId"')
    #sel_orderid_err('T105DataBatchSynDest-B',  'Sub113DataBatchSyn', '"WORK_ITEM_ID"')


