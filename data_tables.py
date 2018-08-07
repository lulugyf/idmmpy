#coding=utf-8


def create_0():
    for i in range(0, 1000,1):
        print "create table messagestore_%d(id VARCHAR2(128) not null,properties VARCHAR2(2048),systemproperties VARCHAR2(1024),content BLOB,createtime NUMBER(20)) tablespace TBS_IDMMDB_DATA;" % i
        print "alter table messagestore_%d add primary key (ID) using index tablespace TBS_IDMMDB_IDX;" % i
    for i in range(0, 200, 1):
        print "create table MSGIDX_PART_%d(idmm_msg_id VARCHAR2(60) not null,produce_cli_id VARCHAR2(32),src_topic_id VARCHAR2(32),dst_cli_id VARCHAR2(32) not null,dst_topic_id VARCHAR2(32) not null,src_commit_code VARCHAR2(4),group_id VARCHAR2(32),priority NUMBER(11) not null,idmm_resend NUMBER(11),consumer_resend NUMBER(11),create_time NUMBER(20),broker_id VARCHAR2(21),req_time NUMBER(20),commit_code VARCHAR2(4),commit_time NUMBER(20),commit_desc VARCHAR2(1024),next_topic_id VARCHAR2(32),next_client_id VARCHAR2(32),expire_time NUMBER(20)) tablespace TBS_IDMMDB_DATA;" % i
        print "create unique index MSGIDX_PART_%d_IDX on MSGIDX_PART_%d (IDMM_MSG_ID, DST_CLI_ID, DST_TOPIC_ID) tablespace TBS_IDMMDB_IDX;" % (i, i)
        print "create Index msgidx_part_%d_idx1 on msgidx_part_%d(dst_cli_id,dst_topic_id) tablespace TBS_IDMMDB_IDX;" %(i , i)

# 另一份表的表空间与前面的交叉, 使表空间使用平衡一些
def create_1():
    for i in range(1000, 2000,1):
        print "create table messagestore_%d(id VARCHAR2(128) not null,properties VARCHAR2(2048),systemproperties VARCHAR2(1024),content BLOB,createtime NUMBER(20)) tablespace TBS_IDMMDB_IDX;" % i
        print "alter table messagestore_%d add primary key (ID) using index tablespace TBS_IDMMDB_DATA;" % i
    for i in range(200, 400, 1):
        print "create table MSGIDX_PART_%d(idmm_msg_id VARCHAR2(60) not null,produce_cli_id VARCHAR2(32),src_topic_id VARCHAR2(32),dst_cli_id VARCHAR2(32) not null,dst_topic_id VARCHAR2(32) not null,src_commit_code VARCHAR2(4),group_id VARCHAR2(32),priority NUMBER(11) not null,idmm_resend NUMBER(11),consumer_resend NUMBER(11),create_time NUMBER(20),broker_id VARCHAR2(21),req_time NUMBER(20),commit_code VARCHAR2(4),commit_time NUMBER(20),commit_desc VARCHAR2(1024),next_topic_id VARCHAR2(32),next_client_id VARCHAR2(32),expire_time NUMBER(20)) tablespace TBS_IDMMDB_IDX;" % i
        print "create unique index MSGIDX_PART_%d_IDX on MSGIDX_PART_%d (IDMM_MSG_ID, DST_CLI_ID, DST_TOPIC_ID) tablespace TBS_IDMMDB_DATA;" % (i, i)
        print "create Index msgidx_part_%d_idx1 on msgidx_part_%d(dst_cli_id,dst_topic_id) tablespace TBS_IDMMDB_DATA;" %(i , i)

def drop_0():
    for i in range(0, 1000, 1):
        print "drop table messagestore_%d;" % i
    for i in range(0, 200, 1):
        print "drop table msgidx_part_%d;" % i

def drop_1():
    for i in range(1000, 2000, 1):
        print "drop table messagestore_%d;" % i
    for i in range(200, 400, 1):
        print "drop table msgidx_part_%d;" % i

import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "nothing to do!"
        print "Usage:  %s <create_0|create_1|drop_0|drop_1>"
    else:
        eval(sys.argv[1]+"()")
