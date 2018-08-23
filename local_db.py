#!/usr/bin/env python
# coding= UTF-8

# 从oracle 库中查询消息体的全部信息, 包括body内容

import string
import time

import sys
import json
import subprocess
import os

_host_conf = {
    "fqidmm1":{
        "dbname":"idmmdb1",
        "zk":'10.113.161.103:8671,10.113.161.104:8671,10.113.161.105:8671,10.105.92.50:8671,10.105.92.51:8671'  # fuqing
    },
    "xqidmm1":{
        "dbname":"idmmdb2",
        "zk":'10.113.172.56:8671,10.113.172.57:8671,10.113.172.58:8671,10.112.185.2:8671,10.112.185.3:8671' # xiqu
    },
    'zntd1':{
        'zk':'172.21.0.46:3181'
    }
}
def _get_conf(k):
    h = hostname()
    return _host_conf[h][k]

def hostname():
    return os.uname()[1]

def conndb():
    import cx_Oracle
    if 'xqgnidmm1' == hostname():
        db = cx_Oracle.connect('idmmopr', 'ykRwj_b6', 'billyzdb')
        cur = db.cursor()
        return db, cur
    #import data_decrypt
    #passwd=data_decrypt.decryptData_auth()
    # IDMMOPR/ykRwj_b6@idmmdb1
    passwd = 'ykRwj_b6'
    dbname = _get_conf("dbname")
    #print "PID %d connect to %s" % ( os.getpid(), dbname)
    db = cx_Oracle.connect('idmmopr',passwd, dbname)
    cur=db.cursor()
    return db, cur

def conf_zk_addr():
    return _get_conf('zk')
