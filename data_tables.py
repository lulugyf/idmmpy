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


'''
create table MSGIDX_PART_err(idmm_msg_id VARCHAR2(60) not null,produce_cli_id VARCHAR2(32),src_topic_id VARCHAR2(32),dst_cli_id VARCHAR2(32) not null,dst_topic_id VARCHAR2(32) not null,src_commit_code VARCHAR2(4),group_id VARCHAR2(32),priority NUMBER(11) not null,idmm_resend NUMBER(11),consumer_resend NUMBER(11),create_time NUMBER(20),broker_id VARCHAR2(21),req_time NUMBER(20),commit_code VARCHAR2(4),commit_time NUMBER(20),commit_desc VARCHAR2(1024),next_topic_id VARCHAR2(32),next_client_id VARCHAR2(32),expire_time NUMBER(20)) tablespace TBS_IDMMDB_DATA;
create unique index MSGIDX_PART_err_IDX on MSGIDX_PART_err (IDMM_MSG_ID, DST_CLI_ID, DST_TOPIC_ID) tablespace TBS_IDMMDB_IDX;
create Index msgidx_part_err_idx1 on msgidx_part_err(dst_cli_id,dst_topic_id) tablespace TBS_IDMMDB_IDX;
'''

#  python data_tables.py parted_tables >parted_tables.sql
def parted_tables():
    print "set timing on;"
    parts = ",\n".join([" partition p_{0:02d} values ('{0:02d}') storage(initial 64k)"
                        " LOB (\"CONTENT\") STORE AS SECUREFILE ( STORAGE(INITIAL 64K) )".format(i) for i in range(1,32)])
    sql = '''create table {1}_{0}(
      id VARCHAR2(128) not null,
      properties VARCHAR2(2048),
      systemproperties VARCHAR2(1024),
      content BLOB,
      createtime NUMBER(20),
      mday char(2) default to_char(sysdate, 'dd')
    ) 
    partition by list(mday)(
    	''' + parts + '''
    	) tablespace TBS_IDMMDB_DATA;
    create index idx_id_ms_p_{0} on {1}_{0}(ID) LOCAL tablespace TBS_IDMMDB_IDX storage(initial 64K);
    create index idx_ctime_ms_p_{0} on {1}_{0}(createtime) LOCAL tablespace TBS_IDMMDB_IDX storage(initial 64K);'''

    for i in range(1000): print sql.format(i, "messagestore_p", "messagestore", "messagestore_bak")

    parts1 = ",\n".join([" partition p_{0:02d} values ('{0:02d}') storage(initial 64k)".format(i) for i in range(1,32)])
    sql = '''create table {1}_{0}(idmm_msg_id VARCHAR2(60) not null,produce_cli_id VARCHAR2(32),src_topic_id VARCHAR2(32),
    dst_cli_id VARCHAR2(32) not null,dst_topic_id VARCHAR2(32) not null,src_commit_code VARCHAR2(4),group_id VARCHAR2(32),
    priority NUMBER(11) not null,idmm_resend NUMBER(11),consumer_resend NUMBER(11),create_time NUMBER(20),broker_id VARCHAR2(21),
    req_time NUMBER(20),commit_code VARCHAR2(4),commit_time NUMBER(20),commit_desc VARCHAR2(1024),next_topic_id VARCHAR2(32),
    next_client_id VARCHAR2(32),expire_time NUMBER(20),
    mday char(2) default to_char(sysdate, 'dd')
    ) 
    partition by list(mday)(
    	''' + parts1 + '''
    	) tablespace TBS_IDMMDB_DATA;
    create index {1}_{0}_idx0 on {1}_{0} (IDMM_MSG_ID, DST_CLI_ID, DST_TOPIC_ID) LOCAL tablespace TBS_IDMMDB_IDX storage(initial 64K);
    create Index mi{1}_{0}_idx1 on {1}_{0}(dst_cli_id,dst_topic_id) LOCAL tablespace TBS_IDMMDB_IDX storage(initial 64K);
    create Index mi{1}_{0}_idx2 on {1}_{0}(create_time) LOCAL tablespace TBS_IDMMDB_IDX storage(initial 64K);
    create Index mi{1}_{0}_idx3 on {1}_{0}(dst_cli_id,dst_topic_id,commit_time) LOCAL tablespace TBS_IDMMDB_IDX storage(initial 64K);'''

    for i in range(200): print sql.format (i, "msgidx_part_p", "msgidx_part", "msgidx_part_bak")

# 表切换,  日期分区表和普通表的切换, 暂时没有处理表中数据
# python -c "import data_tables as dt; dt.table_switch_go('p_', 'bak_')" >go.sql
# python -c "import data_tables as dt; dt.table_switch_go('bak_', 'p_')" >bak.sql
def table_switch_go(use="p_", bak="bak_"):
    print "set timing on;"
    for i in range(1000):
        print "alter table messagestore_{0} rename to messagestore_{1}{0};".format(i, bak)
        print "alter table messagestore_{1}{0} rename to messagestore_{0};".format(i, use)
    for i in range(200):
        print "alter table msgidx_part_{0} rename to msgidx_part_{1}{0};".format(i, bak)
        print "alter table msgidx_part_{1}{0} rename to msgidx_part_{0};".format(i, use)

# 前后都是分区表， 表结构相同， 重建索引为LOCAL模式后重新切换表
# python -c "import data_tables as dt; dt.table_again('p_', 'bak1_')" >ren.sql
def table_again(use="p_", bak="bak1_"):
    print "set timing on;"
    for i in range(1000):
        print "alter table messagestore_{0} rename to messagestore_{1}{0};".format(i, bak)
        print "alter table messagestore_{1}{0} rename to messagestore_{0};".format(i, use)
        print "insert into messagestore_{0} select * from messagestore_{1}{0};".format(i, bak)
        print "commit;"
        print "drop table messagestore_{1}{0};".format(i, bak)
    for i in range(200):
        print "alter table msgidx_part_{0} rename to msgidx_part_{1}{0};".format(i, bak)
        print "alter table msgidx_part_{1}{0} rename to msgidx_part_{0};".format(i, use)
        print "insert into msgidx_part_{0} select * from msgidx_part_{1}{0};".format(i, bak)
        print "commit;"
        print "drop table msgidx_part_{1}{0};".format(i, bak)

import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "nothing to do!"
        print "Usage:  %s <create_0|create_1|drop_0|drop_1>"
    else:
        eval(sys.argv[1]+"()")
