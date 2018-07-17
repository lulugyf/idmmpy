SET SESSION FOREIGN_KEY_CHECKS=0;

/* Drop Indexes */

DROP INDEX MESSAGE_NOTFOUND_index1 ON MESSAGE_NOTFOUND;
DROP INDEX MESSAGE_NOTFOUND_HIS_index1 ON MESSAGE_NOTFOUND_HIS;
DROP INDEX MSGIDX_PART_ERR_Index_1 ON MSGIDX_PART_ERR;
DROP INDEX MSGIDX_PART_ERR_Index_2 ON MSGIDX_PART_ERR;
DROP INDEX MSGIDX_PART_XXX_Index_1 ON MSGIDX_PART_XXX;
DROP INDEX MSGIDX_PART_XXX_Index_2 ON MSGIDX_PART_XXX;
DROP INDEX MSGIDX_PART_XXX_YYYYMM_Index_1 ON MSGIDX_PART_XXX_YYYYMM;
DROP INDEX MSGIDX_PART_XXX_YYYYMM_Index_2 ON MSGIDX_PART_XXX_YYYYMM;



/* Drop Tables */

DROP TABLE IF EXISTS BLE_BASE_INFO;
DROP TABLE IF EXISTS BLE_DEST_TOPIC_REL;
DROP TABLE IF EXISTS BLE_NOT_FOUND;
DROP TABLE IF EXISTS BROKER_BASE_INFO;
DROP TABLE IF EXISTS CLIENT_BASE_INFO;
DROP TABLE IF EXISTS CLIENT_LIMIT_INFO;
DROP TABLE IF EXISTS DEST_TOPIC_INFO;
DROP TABLE IF EXISTS IDMM_VERSION_INFO;
DROP TABLE IF EXISTS MESSAGESTORE_XXX;
DROP TABLE IF EXISTS MESSAGE_NOTFOUND;
DROP TABLE IF EXISTS MESSAGE_NOTFOUND_HIS;
DROP TABLE IF EXISTS MSGIDX_PART_ERR;
DROP TABLE IF EXISTS MSGIDX_PART_XXX;
DROP TABLE IF EXISTS MSGIDX_PART_XXX_YYYYMM;
DROP TABLE IF EXISTS PRIORITY_MAP;
DROP TABLE IF EXISTS SRC_TOPIC_INFO;
DROP TABLE IF EXISTS TENANT_CLIENT_REL;
DROP TABLE IF EXISTS TOPIC_ATTRIBUTE_INFO;
DROP TABLE IF EXISTS TOPIC_MAPPING_REL;
DROP TABLE IF EXISTS TOPIC_PUBLISH_REL;
DROP TABLE IF EXISTS TOPIC_SUBSCRIBE_REL;
DROP TABLE IF EXISTS WHITE_LIST;
DROP TABLE IF EXISTS WHITE_LIST_INDEX;




/* Create Tables */

-- BLE基本信息表
CREATE TABLE BLE_BASE_INFO
(
	BLE_ID numeric(8) NOT NULL COMMENT 'BLE节点标识',
	ID_NUMBER numeric(1) NOT NULL COMMENT '节点序号',
	ADDR_IP varchar(15) NOT NULL COMMENT '节点ip地址',
	ADDR_PORT numeric(5) NOT NULL COMMENT '节点通信端口',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (BLE_ID, ID_NUMBER),
	UNIQUE (BLE_ID, ID_NUMBER),
	UNIQUE (BLE_ID, ADDR_IP, ADDR_PORT)
) COMMENT = 'BLE基本信息表' DEFAULT CHARACTER SET utf8;


-- 目标主题归属BLE关系表
CREATE TABLE BLE_DEST_TOPIC_REL
(
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id',
	BLE_ID numeric(8) NOT NULL COMMENT 'BLE节点标识',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (DEST_TOPIC_ID, BLE_ID),
	UNIQUE (DEST_TOPIC_ID, BLE_ID)
) COMMENT = '目标主题归属BLE关系表' DEFAULT CHARACTER SET utf8;


-- 找不到BLE的消息记录表 : 如果根据消息没有找到对应的ble，则将消息记入该表
CREATE TABLE BLE_NOT_FOUND
(
	MSG_ID varchar(128) NOT NULL COMMENT '消息ID',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	PROPERTIES varchar(4096) NOT NULL COMMENT '消息属性',
	OP_TIME timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '记录入表时间',
	PRIMARY KEY (MSG_ID, DEST_TOPIC_ID)
) COMMENT = '找不到BLE的消息记录表 : 如果根据消息没有找到对应的ble，则将消息记入该表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- Broker基本信息表
CREATE TABLE BROKER_BASE_INFO
(
	-- >0
	BROKER_ID numeric(8) NOT NULL COMMENT 'Broker节点标识 : >0',
	-- IP地址格式
	COMM_IP varchar(15) NOT NULL COMMENT 'ip地址 : IP地址格式',
	-- 1025-65535
	COMM_PORT numeric(15) NOT NULL COMMENT '通信端口 : 1025-65535',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (BROKER_ID)
) COMMENT = 'Broker基本信息表' DEFAULT CHARACTER SET utf8;


-- client基本信息表
CREATE TABLE CLIENT_BASE_INFO
(
	-- 客户端id
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端id : 客户端id',
	-- 子系统名称
	SUB_SYSTEM varchar(32) NOT NULL COMMENT '归属子系统 : 子系统名称',
	-- 自定义格式
	CLIENT_DESC varchar(2048) NOT NULL COMMENT 'Client身份说明 : 自定义格式',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (CLIENT_ID)
) COMMENT = 'client基本信息表' DEFAULT CHARACTER SET utf8;


-- client访问控制表
CREATE TABLE CLIENT_LIMIT_INFO
(
	-- 客户端id
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端id : 客户端id',
	-- 取值有两种:
	-- 密码限制_password
	-- 访问地址限制_ip，正则式配置
	LIMIT_KEY varchar(8) NOT NULL COMMENT '限制类型 : 取值有两种:
密码限制_password
访问地址限制_ip，正则式配置',
	LIMIT_VALUE varchar(2048) NOT NULL COMMENT '限制范围',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (CLIENT_ID, LIMIT_KEY)
) COMMENT = 'client访问控制表' DEFAULT CHARACTER SET utf8;


-- 目标主题信息表
CREATE TABLE DEST_TOPIC_INFO
(
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id',
	DEST_TOPIC_DESC varchar(2048) NOT NULL COMMENT '目标主题描述',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (DEST_TOPIC_ID)
) COMMENT = '目标主题信息表' DEFAULT CHARACTER SET utf8;


-- 版本管理表 : 该表中有且仅有一条记录的版本状态为’1’，就是当前在用的配置版本号；当有新版本发布时，在该表中插入新的记
CREATE TABLE IDMM_VERSION_INFO
(
	-- 配置版本号,>0
	CONFIG_VERSION numeric(8) NOT NULL COMMENT '配置版本号 : 配置版本号,>0',
	-- 0 审核通过
	-- 1 使用中
	-- 2 编辑中
	-- 3 待审核
	VERSION_STATUS char NOT NULL COMMENT '版本状态 : 0 审核通过
1 使用中
2 编辑中
3 待审核',
	VERSION_DESC varchar(2048) NOT NULL COMMENT '版本描述',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (CONFIG_VERSION)
) COMMENT = '版本管理表 : 该表中有且仅有一条记录的版本状态为’1’，就是当前在用的配置版本号；当有新版本发布时，在该表中插入新的记' DEFAULT CHARACTER SET utf8;


-- 原始消息内容表 : 分表，从0、00、00等开始
CREATE TABLE MESSAGESTORE_XXX
(
	ID varchar(128) NOT NULL COMMENT '消息ID',
	PROPERTIES varchar(4096) COMMENT '消息属性',
	SYSTEMPROPERTIES varchar(1024) COMMENT '系统属性',
	CONTENT blob COMMENT '消息体',
	-- 毫秒数
	CREATETIME bigint(20) COMMENT '消息创建时间 : 毫秒数',
	PRIMARY KEY (ID)
) COMMENT = '原始消息内容表 : 分表，从0、00、00等开始' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 找不到消息体的消息记录表
CREATE TABLE MESSAGE_NOTFOUND
(
	ID varchar(128) NOT NULL COMMENT '消息ID',
	-- 毫秒表示，当前时间
	FOUND_TIME bigint(20) DEFAULT 0 COMMENT '记录入表时间 : 毫秒表示，当前时间',
	-- 毫秒表示，当前时间+60000ms
	NEXT_SCAN_TIME bigint(20) DEFAULT 0 COMMENT '下次扫描时间 : 毫秒表示，当前时间+60000ms',
	-- 目前都是0
	SCAN_RETRIES int DEFAULT 0 COMMENT '扫描重试次数 : 目前都是0',
	PRIMARY KEY (ID)
) COMMENT = '找不到消息体的消息记录表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 找不到消息体的消息记录历史表 : 目前没有找到用的地方
CREATE TABLE MESSAGE_NOTFOUND_HIS
(
	ID varchar(128) NOT NULL COMMENT '消息ID',
	-- 毫秒表示，当前时间
	FOUND_TIME bigint(20) DEFAULT 0 COMMENT '记录入表时间 : 毫秒表示，当前时间',
	-- 毫秒表示，当前时间+60000ms
	NEXT_SCAN_TIME bigint(20) DEFAULT 0 COMMENT '下次扫描时间 : 毫秒表示，当前时间+60000ms',
	-- 目前都是0
	SCAN_RETRIES int DEFAULT 0 COMMENT '扫描重试次数 : 目前都是0',
	PRIMARY KEY (ID)
) COMMENT = '找不到消息体的消息记录历史表 : 目前没有找到用的地方' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 错误消息的索引表
CREATE TABLE MSGIDX_PART_ERR
(
	-- idmm创建的消息id
	IDMM_MSG_ID varchar(60) NOT NULL COMMENT '消息ID : idmm创建的消息id',
	-- 生产者客户端id
	PRODUCE_CLI_ID varchar(32) COMMENT '生产者客户端id : 生产者客户端id',
	-- 原始主题
	SRC_TOPIC_ID varchar(32) COMMENT '原始主题 : 原始主题',
	-- 消费者客户端id
	DST_CLI_ID varchar(32) NOT NULL COMMENT '消费者客户端id : 消费者客户端id',
	-- 目标主题id	
	DST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id	 : 目标主题id	',
	-- 此字段没用
	SRC_COMMIT_CODE varchar(4) COMMENT 'SRC_COMMIT_CODE : 此字段没用',
	-- 分组号, 允许为null, 为null时则不以group_id分组及在途消息管理
	GROUP_ID varchar(32) COMMENT '分组号 : 分组号, 允许为null, 为null时则不以group_id分组及在途消息管理',
	-- 优先级
	PRIORITY int DEFAULT 100 NOT NULL COMMENT '优先级 : 优先级',
	IDMM_RESEND int COMMENT 'IDMM_RESEND',
	-- 消费者重发次数
	CONSUMER_RESEND int COMMENT '消费者重发次数 : 消费者重发次数',
	-- 生产消息提交时间, 恢复内存时按此字段排序
	CREATE_TIME bigint(20) COMMENT '生产消息提交时间 : 生产消息提交时间, 恢复内存时按此字段排序',
	-- 消费Broker节点id
	BROKER_ID varchar(21) COMMENT '消费Broker节点id : 消费Broker节点id',
	-- 消费请求时间
	REQ_TIME bigint(20) COMMENT '消费请求时间 : 消费请求时间',
	-- 此字段没用
	COMMIT_CODE varchar(4) COMMENT '消费提交代码 : 此字段没用',
	-- 消费提交时间
	COMMIT_TIME bigint(20) COMMENT '消费提交时间 : 消费提交时间',
	-- 消费结果描述
	COMMIT_DESC varchar(160) COMMENT '消费结果描述 : 消费结果描述',
	-- 顺序消费的下一个目标主题
	NEXT_TOPIC_ID varchar(32) COMMENT '顺序消费的下一个目标主题 : 顺序消费的下一个目标主题',
	-- 顺序消费的下一个消费者， 需要与next_topic_id 一起出现， 并有订阅关系
	NEXT_CLIENT_ID varchar(32) COMMENT '顺序消费的下一个消费者 : 顺序消费的下一个消费者， 需要与next_topic_id 一起出现， 并有订阅关系',
	-- 有效时间，unix时间戳记ms, 0为永久有效
	EXPIRE_TIME bigint(20) DEFAULT 0 COMMENT '有效时间 : 有效时间，unix时间戳记ms, 0为永久有效'
) COMMENT = '错误消息的索引表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 消息索引分表 : xxx表示分表后缀，从0、00、000等开始
-- src_commit_code、commit_code
CREATE TABLE MSGIDX_PART_XXX
(
	-- idmm创建的消息id
	IDMM_MSG_ID varchar(60) NOT NULL COMMENT '消息ID : idmm创建的消息id',
	-- 生产者客户端id
	PRODUCE_CLI_ID varchar(32) COMMENT '生产者客户端id : 生产者客户端id',
	-- 原始主题
	SRC_TOPIC_ID varchar(32) COMMENT '原始主题 : 原始主题',
	-- 消费者客户端id
	DST_CLI_ID varchar(32) NOT NULL COMMENT '消费者客户端id : 消费者客户端id',
	-- 目标主题id	
	DST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id	 : 目标主题id	',
	-- 此字段没用
	SRC_COMMIT_CODE varchar(4) COMMENT 'SRC_COMMIT_CODE : 此字段没用',
	-- 分组号, 允许为null, 为null时则不以group_id分组及在途消息管理
	GROUP_ID varchar(32) COMMENT '分组号 : 分组号, 允许为null, 为null时则不以group_id分组及在途消息管理',
	-- 优先级
	PRIORITY int DEFAULT 100 NOT NULL COMMENT '优先级 : 优先级',
	IDMM_RESEND int COMMENT 'IDMM_RESEND',
	-- 消费者重发次数
	CONSUMER_RESEND int COMMENT '消费者重发次数 : 消费者重发次数',
	-- 生产消息提交时间, 恢复内存时按此字段排序
	CREATE_TIME bigint(20) COMMENT '生产消息提交时间 : 生产消息提交时间, 恢复内存时按此字段排序',
	-- 消费Broker节点id
	BROKER_ID varchar(21) COMMENT '消费Broker节点id : 消费Broker节点id',
	-- 消费请求时间
	REQ_TIME bigint(20) COMMENT '消费请求时间 : 消费请求时间',
	-- 此字段没用
	COMMIT_CODE varchar(4) COMMENT '消费提交代码 : 此字段没用',
	-- 消费提交时间
	COMMIT_TIME bigint(20) COMMENT '消费提交时间 : 消费提交时间',
	-- 消费结果描述
	COMMIT_DESC varchar(160) COMMENT '消费结果描述 : 消费结果描述',
	-- 顺序消费的下一个目标主题
	NEXT_TOPIC_ID varchar(32) COMMENT '顺序消费的下一个目标主题 : 顺序消费的下一个目标主题',
	-- 顺序消费的下一个消费者， 需要与next_topic_id 一起出现， 并有订阅关系
	NEXT_CLIENT_ID varchar(32) COMMENT '顺序消费的下一个消费者 : 顺序消费的下一个消费者， 需要与next_topic_id 一起出现， 并有订阅关系',
	-- 有效时间，unix时间戳记ms, 0为永久有效
	EXPIRE_TIME bigint(20) DEFAULT 0 COMMENT '有效时间 : 有效时间，unix时间戳记ms, 0为永久有效',
	PRIMARY KEY (IDMM_MSG_ID, DST_CLI_ID, DST_TOPIC_ID),
	UNIQUE (DST_CLI_ID, DST_TOPIC_ID)
) COMMENT = '消息索引分表 : xxx表示分表后缀，从0、00、000等开始
src_commit_code、commit_code' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 消息索引年月历史表 : 该表中的数据由manager实时归档处理，只存放正常消费的消息
CREATE TABLE MSGIDX_PART_XXX_YYYYMM
(
	-- idmm创建的消息id
	IDMM_MSG_ID varchar(60) NOT NULL COMMENT '消息ID : idmm创建的消息id',
	-- 生产者客户端id
	PRODUCE_CLI_ID varchar(32) COMMENT '生产者客户端id : 生产者客户端id',
	-- 原始主题
	SRC_TOPIC_ID varchar(32) COMMENT '原始主题 : 原始主题',
	-- 消费者客户端id
	DST_CLI_ID varchar(32) NOT NULL COMMENT '消费者客户端id : 消费者客户端id',
	-- 目标主题id	
	DST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id	 : 目标主题id	',
	-- 此字段没用
	SRC_COMMIT_CODE varchar(4) COMMENT 'SRC_COMMIT_CODE : 此字段没用',
	-- 分组号, 允许为null, 为null时则不以group_id分组及在途消息管理
	GROUP_ID varchar(32) COMMENT '分组号 : 分组号, 允许为null, 为null时则不以group_id分组及在途消息管理',
	-- 优先级
	PRIORITY int DEFAULT 100 NOT NULL COMMENT '优先级 : 优先级',
	IDMM_RESEND int COMMENT 'IDMM_RESEND',
	-- 消费者重发次数
	CONSUMER_RESEND int COMMENT '消费者重发次数 : 消费者重发次数',
	-- 生产消息提交时间, 恢复内存时按此字段排序
	CREATE_TIME bigint(20) COMMENT '生产消息提交时间 : 生产消息提交时间, 恢复内存时按此字段排序',
	-- 消费Broker节点id
	BROKER_ID varchar(21) COMMENT '消费Broker节点id : 消费Broker节点id',
	-- 消费请求时间
	REQ_TIME bigint(20) COMMENT '消费请求时间 : 消费请求时间',
	-- 此字段没用
	COMMIT_CODE varchar(4) COMMENT '消费提交代码 : 此字段没用',
	-- 消费提交时间
	COMMIT_TIME bigint(20) COMMENT '消费提交时间 : 消费提交时间',
	-- 消费结果描述
	COMMIT_DESC varchar(160) COMMENT '消费结果描述 : 消费结果描述',
	-- 顺序消费的下一个目标主题
	NEXT_TOPIC_ID varchar(32) COMMENT '顺序消费的下一个目标主题 : 顺序消费的下一个目标主题',
	-- 顺序消费的下一个消费者， 需要与next_topic_id 一起出现， 并有订阅关系
	NEXT_CLIENT_ID varchar(32) COMMENT '顺序消费的下一个消费者 : 顺序消费的下一个消费者， 需要与next_topic_id 一起出现， 并有订阅关系',
	-- 有效时间，unix时间戳记ms, 0为永久有效
	EXPIRE_TIME bigint(20) DEFAULT 0 COMMENT '有效时间 : 有效时间，unix时间戳记ms, 0为永久有效'
) COMMENT = '消息索引年月历史表 : 该表中的数据由manager实时归档处理，只存放正常消费的消息' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 优先级映射表 : 优先级名称 与 数字的映射表
CREATE TABLE PRIORITY_MAP
(
	-- 优先级名称
	PNAME varchar(32) NOT NULL COMMENT '优先级名称 : 优先级名称',
	-- 优先级数字
	PVALUE int NOT NULL COMMENT '优先级数字 : 优先级数字',
	-- 是否默认优先级， 只能有一个
	-- Y 是
	-- N 否
	-- 
	IS_DEFAULT char(1) COMMENT '是否默认优先级 : 是否默认优先级， 只能有一个
Y 是
N 否
',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (PVALUE),
	UNIQUE (PVALUE)
) COMMENT = '优先级映射表 : 优先级名称 与 数字的映射表' DEFAULT CHARACTER SET utf8;


-- 原始主题信息表
CREATE TABLE SRC_TOPIC_INFO
(
	-- 前缀s
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题id : 前缀s',
	SRC_TOPIC_DESC varchar(2048) NOT NULL COMMENT '原始主题描述',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (SRC_TOPIC_ID)
) COMMENT = '原始主题信息表' DEFAULT CHARACTER SET utf8;


-- 租户客户端关系表 : 1个租户可以拥有多个客户端，1个客户端只能属于1个租户
CREATE TABLE TENANT_CLIENT_REL
(
	TENANT_ID varchar(120) NOT NULL COMMENT '租户ID',
	-- 客户端id
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端id : 客户端id',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (TENANT_ID, CLIENT_ID)
) COMMENT = '租户客户端关系表 : 1个租户可以拥有多个客户端，1个客户端只能属于1个租户' DEFAULT CHARACTER SET utf8;


-- 主题分区属性表 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
-- 如果有按
CREATE TABLE TOPIC_ATTRIBUTE_INFO
(
	-- 前缀s
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题id : 前缀s',
	-- 含_all
	ATTRIBUTE_KEY varchar(32) NOT NULL COMMENT '属性key : 含_all',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (SRC_TOPIC_ID, ATTRIBUTE_KEY),
	UNIQUE (SRC_TOPIC_ID, ATTRIBUTE_KEY)
) COMMENT = '主题分区属性表 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
如果有按' DEFAULT CHARACTER SET utf8;


-- 主题映射关系表 : 可以针对每一个属性值设置一个或者多个目标主题；
-- 属性值可以是“_default”，表示如果生产者没
CREATE TABLE TOPIC_MAPPING_REL
(
	-- 前缀s
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题id : 前缀s',
	-- 含_all
	ATTRIBUTE_KEY varchar(32) NOT NULL COMMENT '属性key : 含_all',
	-- 含_default
	ATTRIBUTE_VALUE varchar(32) NOT NULL COMMENT '属性value : 含_default',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (SRC_TOPIC_ID, ATTRIBUTE_KEY, ATTRIBUTE_VALUE, DEST_TOPIC_ID)
) COMMENT = '主题映射关系表 : 可以针对每一个属性值设置一个或者多个目标主题；
属性值可以是“_default”，表示如果生产者没' DEFAULT CHARACTER SET utf8;


-- 主题发布关系表 : 用于描述生产者客户端发布原始主题消息的权限关系；
CREATE TABLE TOPIC_PUBLISH_REL
(
	-- 客户端id
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端id : 客户端id',
	-- 前缀s
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题id : 前缀s',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (CLIENT_ID, SRC_TOPIC_ID),
	UNIQUE (CLIENT_ID, SRC_TOPIC_ID)
) COMMENT = '主题发布关系表 : 用于描述生产者客户端发布原始主题消息的权限关系；' DEFAULT CHARACTER SET utf8;


-- 主题订阅关系表 : 用于描述消费者客户端接收主题消息的关系；
CREATE TABLE TOPIC_SUBSCRIBE_REL
(
	-- 客户端id
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端id : 客户端id',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题id',
	MAX_REQUEST int(3) COMMENT '最大并发数',
	MIN_TIMEOUT int(8) COMMENT '最小超时时间',
	MAX_TIMEOUT int(8) COMMENT '最大超时时间',
	-- 消费速度限制， 单位 n/miniute
	CONSUME_SPEED_LIMIT int DEFAULT -1 NOT NULL COMMENT '消费速度限制 : 消费速度限制， 单位 n/miniute',
	-- 积压消息数  最大值
	MAX_MESSAGES int COMMENT '积压消息数最大值 : 积压消息数  最大值',
	-- 积压消息数告警值
	WARN_MESSAGES int COMMENT '积压消息数告警值 : 积压消息数告警值',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	LOGIN_NO varchar(32) COMMENT '操作工号',
	OPR_TIME datetime COMMENT '操作时间',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (CLIENT_ID, DEST_TOPIC_ID),
	UNIQUE (CLIENT_ID, DEST_TOPIC_ID)
) COMMENT = '主题订阅关系表 : 用于描述消费者客户端接收主题消息的关系；' DEFAULT CHARACTER SET utf8;


-- 白名单信息表
CREATE TABLE WHITE_LIST
(
	IP varchar(15) NOT NULL COMMENT 'ip地址',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引id : 用于与white_list_index关联',
	-- 0 不启用,1 启用
	USE_STATUS char(1) DEFAULT '1' NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	PRIMARY KEY (IP, USE_STATUS)
) COMMENT = '白名单信息表' DEFAULT CHARACTER SET utf8;


-- 白名单信息索引表
CREATE TABLE WHITE_LIST_INDEX
(
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引id : 用于与white_list_index关联',
	BEGIN_IP varchar(15) NOT NULL COMMENT '起始ip地址',
	END_IP varchar(15) NOT NULL COMMENT '终止ip地址',
	-- 0 不启用,1 启用
	USE_STATUS char(1) NOT NULL COMMENT '使用标识 : 0 不启用,1 启用',
	PRIMARY KEY (INDEX_ID)
) COMMENT = '白名单信息索引表' DEFAULT CHARACTER SET utf8;



/* Create Indexes */

CREATE INDEX MESSAGE_NOTFOUND_index1 USING BTREE ON MESSAGE_NOTFOUND (NEXT_SCAN_TIME ASC);
CREATE INDEX MESSAGE_NOTFOUND_HIS_index1 USING BTREE ON MESSAGE_NOTFOUND_HIS (NEXT_SCAN_TIME ASC);
CREATE INDEX MSGIDX_PART_ERR_Index_1 ON MSGIDX_PART_ERR (IDMM_MSG_ID ASC, DST_CLI_ID ASC, DST_TOPIC_ID ASC);
CREATE INDEX MSGIDX_PART_ERR_Index_2 ON MSGIDX_PART_ERR (DST_CLI_ID ASC, DST_TOPIC_ID ASC);
CREATE UNIQUE INDEX MSGIDX_PART_XXX_Index_1 USING BTREE ON MSGIDX_PART_XXX (IDMM_MSG_ID ASC, DST_CLI_ID ASC, DST_TOPIC_ID ASC);
CREATE INDEX MSGIDX_PART_XXX_Index_2 USING BTREE ON MSGIDX_PART_XXX (DST_CLI_ID ASC, DST_TOPIC_ID ASC);
CREATE INDEX MSGIDX_PART_XXX_YYYYMM_Index_1 ON MSGIDX_PART_XXX_YYYYMM (IDMM_MSG_ID ASC, DST_CLI_ID ASC, DST_TOPIC_ID ASC);
CREATE INDEX MSGIDX_PART_XXX_YYYYMM_Index_2 ON MSGIDX_PART_XXX_YYYYMM (DST_CLI_ID ASC, DST_TOPIC_ID ASC);



