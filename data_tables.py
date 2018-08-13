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


def parted_tables():
    print "set timing on;"
    sql = '''
    create table messagestore_%d_(
      id VARCHAR2(128) not null,
      properties VARCHAR2(2048),
      systemproperties VARCHAR2(1024),
      content BLOB,
      createtime NUMBER(20),
      mday char(2) default to_char(sysdate, 'MM')
    ) tablespace TBS_IDMMDB_DATA
    partition by list(mday)(
    	partition p_01 values ('01') tablespace TBS_IDMMDB_DATA,
    	partition p_02 values ('02') tablespace TBS_IDMMDB_DATA,
    	partition p_03 values ('03') tablespace TBS_IDMMDB_DATA,
    	partition p_04 values ('04') tablespace TBS_IDMMDB_DATA,
    	partition p_05 values ('05') tablespace TBS_IDMMDB_DATA,
    	partition p_06 values ('06') tablespace TBS_IDMMDB_DATA,
    	partition p_07 values ('07') tablespace TBS_IDMMDB_DATA,
    	partition p_08 values ('08') tablespace TBS_IDMMDB_DATA,
    	partition p_09 values ('09') tablespace TBS_IDMMDB_DATA,
    	partition p_10 values ('10') tablespace TBS_IDMMDB_DATA,
    	partition p_11 values ('11') tablespace TBS_IDMMDB_DATA,
    	partition p_12 values ('12') tablespace TBS_IDMMDB_DATA,
    	partition p_13 values ('13') tablespace TBS_IDMMDB_DATA,
    	partition p_14 values ('14') tablespace TBS_IDMMDB_DATA,
    	partition p_15 values ('15') tablespace TBS_IDMMDB_DATA,
    	partition p_16 values ('16') tablespace TBS_IDMMDB_DATA,
    	partition p_17 values ('17') tablespace TBS_IDMMDB_DATA,
    	partition p_18 values ('18') tablespace TBS_IDMMDB_DATA,
    	partition p_19 values ('19') tablespace TBS_IDMMDB_DATA,
    	partition p_20 values ('20') tablespace TBS_IDMMDB_DATA,
    	partition p_21 values ('21') tablespace TBS_IDMMDB_DATA,
    	partition p_22 values ('22') tablespace TBS_IDMMDB_DATA,
    	partition p_23 values ('23') tablespace TBS_IDMMDB_DATA,
    	partition p_24 values ('24') tablespace TBS_IDMMDB_DATA,
    	partition p_25 values ('25') tablespace TBS_IDMMDB_DATA,
    	partition p_26 values ('26') tablespace TBS_IDMMDB_DATA,
    	partition p_27 values ('27') tablespace TBS_IDMMDB_DATA,
    	partition p_28 values ('28') tablespace TBS_IDMMDB_DATA,
    	partition p_29 values ('29') tablespace TBS_IDMMDB_DATA,
    	partition p_30 values ('30') tablespace TBS_IDMMDB_DATA,
    	partition p_31 values ('31') tablespace TBS_IDMMDB_DATA,
    	partition p_def values (DEFAULT) tablespace TBS_IDMMDB_DATA
    	);
    alter table messagestore_%d_ add primary key (ID) using index tablespace TBS_IDMMDB_IDX;
    create index idx_ctime_messagestore_%d on messagestore_%d_(createtime) tablespace TBS_IDMMDB_IDX;

    alter table messagestore_%d rename to messagestore_%d_bak;
    alter table messagestore_%d_ rename to messagestore_%d;
    insert into messagestore_%d select id, properties, systemproperties, content, createtime, to_char(sysdate,'MM') from messagestore_%d_bak;
    commit;'''

    for i in range(1000): print sql % (i, i, i, i, i, i, i, i, i, i)

    sql = '''
    create table MSGIDX_PART_%d_(idmm_msg_id VARCHAR2(60) not null,produce_cli_id VARCHAR2(32),src_topic_id VARCHAR2(32),dst_cli_id VARCHAR2(32) not null,dst_topic_id VARCHAR2(32) not null,src_commit_code VARCHAR2(4),group_id VARCHAR2(32),priority NUMBER(11) not null,idmm_resend NUMBER(11),consumer_resend NUMBER(11),create_time NUMBER(20),broker_id VARCHAR2(21),req_time NUMBER(20),commit_code VARCHAR2(4),commit_time NUMBER(20),commit_desc VARCHAR2(1024),next_topic_id VARCHAR2(32),next_client_id VARCHAR2(32),expire_time NUMBER(20),
    mday char(2) default to_char(sysdate, 'MM')
    ) tablespace TBS_IDMMDB_DATA
    partition by list(mday)(
    	partition p_01 values ('01') tablespace TBS_IDMMDB_DATA,
    	partition p_02 values ('02') tablespace TBS_IDMMDB_DATA,
    	partition p_03 values ('03') tablespace TBS_IDMMDB_DATA,
    	partition p_04 values ('04') tablespace TBS_IDMMDB_DATA,
    	partition p_05 values ('05') tablespace TBS_IDMMDB_DATA,
    	partition p_06 values ('06') tablespace TBS_IDMMDB_DATA,
    	partition p_07 values ('07') tablespace TBS_IDMMDB_DATA,
    	partition p_08 values ('08') tablespace TBS_IDMMDB_DATA,
    	partition p_09 values ('09') tablespace TBS_IDMMDB_DATA,
    	partition p_10 values ('10') tablespace TBS_IDMMDB_DATA,
    	partition p_11 values ('11') tablespace TBS_IDMMDB_DATA,
    	partition p_12 values ('12') tablespace TBS_IDMMDB_DATA,
    	partition p_13 values ('13') tablespace TBS_IDMMDB_DATA,
    	partition p_14 values ('14') tablespace TBS_IDMMDB_DATA,
    	partition p_15 values ('15') tablespace TBS_IDMMDB_DATA,
    	partition p_16 values ('16') tablespace TBS_IDMMDB_DATA,
    	partition p_17 values ('17') tablespace TBS_IDMMDB_DATA,
    	partition p_18 values ('18') tablespace TBS_IDMMDB_DATA,
    	partition p_19 values ('19') tablespace TBS_IDMMDB_DATA,
    	partition p_20 values ('20') tablespace TBS_IDMMDB_DATA,
    	partition p_21 values ('21') tablespace TBS_IDMMDB_DATA,
    	partition p_22 values ('22') tablespace TBS_IDMMDB_DATA,
    	partition p_23 values ('23') tablespace TBS_IDMMDB_DATA,
    	partition p_24 values ('24') tablespace TBS_IDMMDB_DATA,
    	partition p_25 values ('25') tablespace TBS_IDMMDB_DATA,
    	partition p_26 values ('26') tablespace TBS_IDMMDB_DATA,
    	partition p_27 values ('27') tablespace TBS_IDMMDB_DATA,
    	partition p_28 values ('28') tablespace TBS_IDMMDB_DATA,
    	partition p_29 values ('29') tablespace TBS_IDMMDB_DATA,
    	partition p_30 values ('30') tablespace TBS_IDMMDB_DATA,
    	partition p_31 values ('31') tablespace TBS_IDMMDB_DATA,
    	partition p_def values (DEFAULT) tablespace TBS_IDMMDB_DATA
    	);
    create unique index MSGIDX_PART_%d__IDX on MSGIDX_PART_%d_ (IDMM_MSG_ID, DST_CLI_ID, DST_TOPIC_ID) tablespace TBS_IDMMDB_IDX;
    create Index msgidx_part_%d__idx1 on msgidx_part_%d_(dst_cli_id,dst_topic_id) tablespace TBS_IDMMDB_IDX;
    create Index msgidx_part_%d__idx2 on msgidx_part_%d_(create_time) tablespace TBS_IDMMDB_IDX;
    alter table MSGIDX_PART_%d rename to MSGIDX_PART_%d_bak;
    alter table MSGIDX_PART_%d_ rename to MSGIDX_PART_%d;
    insert into MSGIDX_PART_%d select idmm_msg_id,produce_cli_id,src_topic_id,dst_cli_id,dst_topic_id,src_commit_code,group_id,priority ,idmm_resend ,consumer_resend ,create_time ,broker_id ,req_time ,commit_code ,commit_time ,commit_desc ,next_topic_id ,next_client_id ,expire_time,to_char(sysdate, 'MM') from MSGIDX_PART_%d_bak;
    commit;'''
    for i in range(200): print sql % (i, i, i, i, i, i, i, i, i, i, i, i, i,)

import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "nothing to do!"
        print "Usage:  %s <create_0|create_1|drop_0|drop_1>"
    else:
        eval(sys.argv[1]+"()")
