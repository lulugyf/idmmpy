#!/usr/bin/env python
# coding= UTF-8

import string
import time
import cx_Oracle
import sys
import json

# def conndb():
#     passwd = 'ykRwj_b6'
#     db = cx_Oracle.connect('idmmopr', 'ykRwj_b6', 'idmmdb2')
#     cur = db.cursor()
#     return db, cur

from local_db import conndb

def restore_idx(db, cur, topic, client, tblcount):
    for i in range(tblcount):
        cur.execute("""update msgidx_part_%d set commit_time=0 where dst_topic_id=:v1
            and dst_cli_id=:v2 and create_time>0""" %i, (topic, client))
        print("--%d rowcount= %d"%(i, cur.rowcount))
    db.commit()

def restore_err(db, cur, topic, client):
    cur.execute("select IDMM_MSG_ID from msgidx_part_err where dst_topic_id=:v1 and dst_cli_id=:v2",
                (topic, client))

    sql = """insert into msgidx_part_%s(IDMM_MSG_ID,PRODUCE_CLI_ID,SRC_TOPIC_ID,DST_CLI_ID,DST_TOPIC_ID,
SRC_COMMIT_CODE,GROUP_ID,PRIORITY,IDMM_RESEND,CONSUMER_RESEND,
CREATE_TIME,BROKER_ID,REQ_TIME,COMMIT_CODE,COMMIT_TIME,
COMMIT_DESC,NEXT_TOPIC_ID,NEXT_CLIENT_ID,EXPIRE_TIME)
select IDMM_MSG_ID,PRODUCE_CLI_ID,SRC_TOPIC_ID,DST_CLI_ID,DST_TOPIC_ID,
SRC_COMMIT_CODE,GROUP_ID,PRIORITY,IDMM_RESEND,CONSUMER_RESEND,
CREATE_TIME,BROKER_ID,REQ_TIME,COMMIT_CODE,COMMIT_TIME,
COMMIT_DESC,NEXT_TOPIC_ID,NEXT_CLIENT_ID,-1 from msgidx_part_err
where dst_topic_id=:v1 and dst_cli_id=:v2 and IDMM_MSG_ID=:v3"""
    for row in cur.fetchall():
        id = row[0]
        ii = id.split("::")[-2]
        sql1 = sql % ii
        cur.execute(sql1, (topic, client, id))
        print("err %s %s affectted= %d"%(id, ii, cur.rowcount))
    db.commit()

def main():
    topic = "T103DataSynRESDest-B"
    client = "Sub105DataSyn"

    db, cur = conndb()
    restore_idx(db, cur, topic, client, 200)
    restore_err(db, cur, topic, client)

    cur.close()
    db.close()

    print("curl http://<jmxaddr>/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/reload/%s/%s"%(client, topic))

if __name__ == '__main__':
    main()
