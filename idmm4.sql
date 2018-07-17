SET SESSION FOREIGN_KEY_CHECKS=0;

/* Drop Tables */

DROP TABLE IF EXISTS IDMM_C_BLE_EDIT;
DROP TABLE IF EXISTS IDMM_C_BLE_HIS;
DROP TABLE IF EXISTS IDMM_C_BLE_RLS;
DROP TABLE IF EXISTS IDMM_C_BROKER_EDIT;
DROP TABLE IF EXISTS IDMM_C_BROKER_HIS;
DROP TABLE IF EXISTS IDMM_C_BROKER_RLS;
DROP TABLE IF EXISTS IDMM_C_CLIENT_EDIT;
DROP TABLE IF EXISTS IDMM_C_CLIENT_HIS;
DROP TABLE IF EXISTS IDMM_C_CLIENT_LIMIT_EDIT;
DROP TABLE IF EXISTS IDMM_C_CLIENT_LIMIT_HIS;
DROP TABLE IF EXISTS IDMM_C_CLIENT_LIMIT_RLS;
DROP TABLE IF EXISTS IDMM_C_CLIENT_RLS;
DROP TABLE IF EXISTS IDMM_C_DEST_TOPIC_EDIT;
DROP TABLE IF EXISTS IDMM_C_DEST_TOPIC_HIS;
DROP TABLE IF EXISTS IDMM_C_DEST_TOPIC_RLS;
DROP TABLE IF EXISTS IDMM_C_SRC_TOPIC_EDIT;
DROP TABLE IF EXISTS IDMM_C_SRC_TOPIC_HIS;
DROP TABLE IF EXISTS IDMM_C_SRC_TOPIC_RLS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_ATTR_EDIT;
DROP TABLE IF EXISTS IDMM_C_TOPIC_ATTR_HIS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_ATTR_RLS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_BLE_EDIT;
DROP TABLE IF EXISTS IDMM_C_TOPIC_BLE_HIS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_BLE_RLS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_MAP_EDIT;
DROP TABLE IF EXISTS IDMM_C_TOPIC_MAP_HIS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_MAP_RLS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_PUB_EDIT;
DROP TABLE IF EXISTS IDMM_C_TOPIC_PUB_HIS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_PUB_RLS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_SUB_EDIT;
DROP TABLE IF EXISTS IDMM_C_TOPIC_SUB_HIS;
DROP TABLE IF EXISTS IDMM_C_TOPIC_SUB_RLS;
DROP TABLE IF EXISTS IDMM_C_VERSION;
DROP TABLE IF EXISTS IDMM_C_VERSION_CHECK;
DROP TABLE IF EXISTS IDMM_C_VERSION_HIS;
DROP TABLE IF EXISTS IDMM_C_WHITE_EDIT;
DROP TABLE IF EXISTS IDMM_C_WHITE_HIS;
DROP TABLE IF EXISTS IDMM_C_WHITE_INDEX_EDIT;
DROP TABLE IF EXISTS IDMM_C_WHITE_INDEX_HIS;
DROP TABLE IF EXISTS IDMM_C_WHITE_INDEX_RLS;
DROP TABLE IF EXISTS IDMM_C_WHITE_RLS;
DROP TABLE IF EXISTS IDMM_M_BLE;
DROP TABLE IF EXISTS IDMM_M_BLE_DETAIL;
DROP TABLE IF EXISTS IDMM_M_BLE_DETAIL_HIS;
DROP TABLE IF EXISTS IDMM_M_BLE_HIS;
DROP TABLE IF EXISTS IDMM_M_BLE_MEM_QUEUE;
DROP TABLE IF EXISTS IDMM_M_BLE_MEM_QUEUE_HIS;
DROP TABLE IF EXISTS IDMM_M_BROKER;
DROP TABLE IF EXISTS IDMM_M_BROKER_HIS;
DROP TABLE IF EXISTS IDMM_M_BROKER_TPS;
DROP TABLE IF EXISTS IDMM_M_BROKER_TPS_HIS;
DROP TABLE IF EXISTS IDMM_M_MANAGER;
DROP TABLE IF EXISTS IDMM_M_MANAGER_HIS;
DROP TABLE IF EXISTS KFK_C_AUTH_USER;
DROP TABLE IF EXISTS KFK_C_BROKER;
DROP TABLE IF EXISTS KFK_C_TOPIC;
DROP TABLE IF EXISTS KFK_C_TOPIC_AUTH_REC;
DROP TABLE IF EXISTS KFK_C_TOPIC_SUB;
DROP TABLE IF EXISTS KFK_M_TOPIC;
DROP TABLE IF EXISTS KFK_M_TOPIC_HIS;
DROP TABLE IF EXISTS SYS_CLUSTER;
DROP TABLE IF EXISTS SYS_DB;
DROP TABLE IF EXISTS SYS_FUNCTION;
DROP TABLE IF EXISTS SYS_FUNC_SVC;
DROP TABLE IF EXISTS SYS_HOST;
DROP TABLE IF EXISTS SYS_LOG;
DROP TABLE IF EXISTS SYS_MANAGER;
DROP TABLE IF EXISTS SYS_ROLE;
DROP TABLE IF EXISTS SYS_ROLE_FUNCTION;
DROP TABLE IF EXISTS SYS_TENANT_RES;
DROP TABLE IF EXISTS SYS_USER;
DROP TABLE IF EXISTS SYS_USER_CLUSTER;
DROP TABLE IF EXISTS SYS_USER_ROLE;
DROP TABLE IF EXISTS SYS_ZOOKEEPER;
DROP TABLE IF EXISTS T_C_DICT;
DROP TABLE IF EXISTS T_C_SEQ;
DROP TABLE IF EXISTS T_M_ALARM;
DROP TABLE IF EXISTS T_M_ALARM_HIS;
DROP TABLE IF EXISTS T_M_ALARM_OPTION;
DROP TABLE IF EXISTS T_M_CLUSTER;
DROP TABLE IF EXISTS T_M_CLUSTER_HIS;
DROP TABLE IF EXISTS T_M_HOST;
DROP TABLE IF EXISTS T_M_HOST_CONN;
DROP TABLE IF EXISTS T_M_HOST_CONN_HIS;
DROP TABLE IF EXISTS T_M_HOST_HIS;
DROP TABLE IF EXISTS T_M_LOG;
DROP TABLE IF EXISTS T_M_LOG_HIS;
DROP TABLE IF EXISTS T_M_PROCESS;
DROP TABLE IF EXISTS T_M_PROCESS_HIS;
DROP TABLE IF EXISTS T_M_ZOOKEEPER;
DROP TABLE IF EXISTS T_M_ZOOKEEPER_HIS;




/* Create Tables */

-- BLE基本信息表【编辑】
CREATE TABLE IDMM_C_BLE_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	ID_SEQ int COMMENT '节点序号',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int COMMENT 'TCP端口',
	JMX_PORT int COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, BLE_ID),
	UNIQUE (BLE_ID, ID_SEQ)
) COMMENT = 'BLE基本信息表【编辑】';


-- BLE基本信息表【历史】
CREATE TABLE IDMM_C_BLE_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	ID_SEQ int COMMENT '节点序号',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int COMMENT 'TCP端口',
	JMX_PORT int COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, BLE_ID),
	UNIQUE (BLE_ID, ID_SEQ)
) COMMENT = 'BLE基本信息表【历史】';


-- BLE基本信息表【发布】
CREATE TABLE IDMM_C_BLE_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	ID_SEQ int COMMENT '节点序号',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int COMMENT 'TCP端口',
	JMX_PORT int COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, BLE_ID),
	UNIQUE (BLE_ID, ID_SEQ)
) COMMENT = 'BLE基本信息表【发布】';


-- Broker基本信息表【编辑】
CREATE TABLE IDMM_C_BROKER_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int COMMENT 'TCP端口',
	HTTP_PORT int COMMENT 'HTTP端口',
	JMX_PORT int COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, BROKER_ID)
) COMMENT = 'Broker基本信息表【编辑】';


-- Broker基本信息表【历史】
CREATE TABLE IDMM_C_BROKER_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int COMMENT 'TCP端口',
	HTTP_PORT int COMMENT 'HTTP端口',
	JMX_PORT int COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, BROKER_ID)
) COMMENT = 'Broker基本信息表【历史】';


-- Broker基本信息表【发布】
CREATE TABLE IDMM_C_BROKER_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int COMMENT 'TCP端口',
	HTTP_PORT int COMMENT 'HTTP端口',
	JMX_PORT int COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, BROKER_ID)
) COMMENT = 'Broker基本信息表【发布】';


-- 客户端信息表【编辑】
CREATE TABLE IDMM_C_CLIENT_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	-- 自定义格式
	CLIENT_DESC varchar(60) NOT NULL COMMENT '客户端描述 : 自定义格式',
	-- 如归属于CRM、billing等
	SUB_SYSTEM varchar(32) NOT NULL COMMENT '归属子系统 : 如归属于CRM、billing等',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID)
) COMMENT = '客户端信息表【编辑】';


-- 客户端信息表【历史】
CREATE TABLE IDMM_C_CLIENT_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	-- 自定义格式
	CLIENT_DESC varchar(60) NOT NULL COMMENT '客户端描述 : 自定义格式',
	-- 如归属于CRM、billing等
	SUB_SYSTEM varchar(32) NOT NULL COMMENT '归属子系统 : 如归属于CRM、billing等',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, CLIENT_ID)
) COMMENT = '客户端信息表【历史】';


-- 客户端访问控制表【编辑】 : 客户端连接时的限制条件，如根据IP限制、根据密码限制等
CREATE TABLE IDMM_C_CLIENT_LIMIT_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	LIMIT_KEY varchar(8) NOT NULL COMMENT '限制类型',
	LIMIT_VALUE varchar(2048) NOT NULL COMMENT '限制范围',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID, LIMIT_KEY)
) COMMENT = '客户端访问控制表【编辑】 : 客户端连接时的限制条件，如根据IP限制、根据密码限制等';


-- 客户端访问控制表【历史】 : 客户端连接时的限制条件，如根据IP限制、根据密码限制等
CREATE TABLE IDMM_C_CLIENT_LIMIT_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	LIMIT_KEY varchar(8) NOT NULL COMMENT '限制类型',
	LIMIT_VALUE varchar(2048) NOT NULL COMMENT '限制范围',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, CLIENT_ID, LIMIT_KEY)
) COMMENT = '客户端访问控制表【历史】 : 客户端连接时的限制条件，如根据IP限制、根据密码限制等';


-- 客户端访问控制表【发布】 : 客户端连接时的限制条件，如根据IP限制、根据密码限制等
CREATE TABLE IDMM_C_CLIENT_LIMIT_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	LIMIT_KEY varchar(8) NOT NULL COMMENT '限制类型',
	LIMIT_VALUE varchar(2048) NOT NULL COMMENT '限制范围',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID, LIMIT_KEY)
) COMMENT = '客户端访问控制表【发布】 : 客户端连接时的限制条件，如根据IP限制、根据密码限制等';


-- 客户端信息表【发布】
CREATE TABLE IDMM_C_CLIENT_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	-- 自定义格式
	CLIENT_DESC varchar(60) NOT NULL COMMENT '客户端描述 : 自定义格式',
	-- 如归属于CRM、billing等
	SUB_SYSTEM varchar(32) NOT NULL COMMENT '归属子系统 : 如归属于CRM、billing等',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID)
) COMMENT = '客户端信息表【发布】';


-- 目标主题信息表【编辑】
CREATE TABLE IDMM_C_DEST_TOPIC_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	DEST_TOPIC_DESC varchar(60) NOT NULL COMMENT '目标主题描述',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, DEST_TOPIC_ID)
) COMMENT = '目标主题信息表【编辑】';


-- 目标主题信息表【历史】
CREATE TABLE IDMM_C_DEST_TOPIC_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	DEST_TOPIC_DESC varchar(60) NOT NULL COMMENT '目标主题描述',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, DEST_TOPIC_ID)
) COMMENT = '目标主题信息表【历史】';


-- 目标主题信息表【发布】
CREATE TABLE IDMM_C_DEST_TOPIC_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	DEST_TOPIC_DESC varchar(60) NOT NULL COMMENT '目标主题描述',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, DEST_TOPIC_ID)
) COMMENT = '目标主题信息表【发布】';


-- 原始主题信息表【编辑】
CREATE TABLE IDMM_C_SRC_TOPIC_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	SRC_TOPIC_DESC varchar(60) NOT NULL COMMENT '原始主题描述',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, SRC_TOPIC_ID)
) COMMENT = '原始主题信息表【编辑】';


-- 原始主题信息表【历史】
CREATE TABLE IDMM_C_SRC_TOPIC_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	SRC_TOPIC_DESC varchar(60) NOT NULL COMMENT '原始主题描述',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, SRC_TOPIC_ID)
) COMMENT = '原始主题信息表【历史】';


-- 原始主题信息表【发布】
CREATE TABLE IDMM_C_SRC_TOPIC_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	SRC_TOPIC_DESC varchar(60) NOT NULL COMMENT '原始主题描述',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, SRC_TOPIC_ID)
) COMMENT = '原始主题信息表【发布】';


-- 原始主题属性表【编辑】 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
-- 
CREATE TABLE IDMM_C_TOPIC_ATTR_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 含_all
	ATTR_KEY varchar(32) NOT NULL COMMENT '属性KEY : 含_all',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, SRC_TOPIC_ID, ATTR_KEY),
	UNIQUE (SRC_TOPIC_ID, ATTR_KEY)
) COMMENT = '原始主题属性表【编辑】 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
';


-- 原始主题属性表【历史】 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
-- 
CREATE TABLE IDMM_C_TOPIC_ATTR_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 含_all
	ATTR_KEY varchar(32) NOT NULL COMMENT '属性KEY : 含_all',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, SRC_TOPIC_ID, ATTR_KEY),
	UNIQUE (SRC_TOPIC_ID, ATTR_KEY)
) COMMENT = '原始主题属性表【历史】 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
';


-- 原始主题属性表【发布】 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
-- 
CREATE TABLE IDMM_C_TOPIC_ATTR_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 含_all
	ATTR_KEY varchar(32) NOT NULL COMMENT '属性KEY : 含_all',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, SRC_TOPIC_ID, ATTR_KEY),
	UNIQUE (SRC_TOPIC_ID, ATTR_KEY)
) COMMENT = '原始主题属性表【发布】 : 如果没有按照分区路由的需求，则只需要配置一个“_all”属性即可，表示不需要分区的情况；
';


-- 目标主题归属BLE关系表【编辑】
CREATE TABLE IDMM_C_TOPIC_BLE_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, DEST_TOPIC_ID),
	UNIQUE (DEST_TOPIC_ID, BLE_ID)
) COMMENT = '目标主题归属BLE关系表【编辑】';


-- 目标主题归属BLE关系表【历史】
CREATE TABLE IDMM_C_TOPIC_BLE_HIS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, VERSION_ID, DEST_TOPIC_ID),
	UNIQUE (DEST_TOPIC_ID, BLE_ID)
) COMMENT = '目标主题归属BLE关系表【历史】';


-- 目标主题归属BLE关系表【发布】
CREATE TABLE IDMM_C_TOPIC_BLE_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, DEST_TOPIC_ID),
	UNIQUE (DEST_TOPIC_ID, BLE_ID)
) COMMENT = '目标主题归属BLE关系表【发布】';


-- 主题映射关系表【编辑】 : 可以针对每一个属性值设置一个或者多个目标主题；
-- 属性值可以是“_default”，表示如果
CREATE TABLE IDMM_C_TOPIC_MAP_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 含_all
	ATTR_KEY varchar(32) NOT NULL COMMENT '属性KEY : 含_all',
	-- 含_default
	ATTR_VALUE varchar(32) NOT NULL COMMENT '属性值 : 含_default',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, SRC_TOPIC_ID, ATTR_KEY, ATTR_VALUE, DEST_TOPIC_ID)
) COMMENT = '主题映射关系表【编辑】 : 可以针对每一个属性值设置一个或者多个目标主题；
属性值可以是“_default”，表示如果';


-- 主题映射关系表【历史】 : 可以针对每一个属性值设置一个或者多个目标主题；
-- 属性值可以是“_default”，表示如果
CREATE TABLE IDMM_C_TOPIC_MAP_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 含_all
	ATTR_KEY varchar(32) NOT NULL COMMENT '属性KEY : 含_all',
	-- 含_default
	ATTR_VALUE varchar(32) NOT NULL COMMENT '属性值 : 含_default',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, SRC_TOPIC_ID, ATTR_KEY, ATTR_VALUE, DEST_TOPIC_ID)
) COMMENT = '主题映射关系表【历史】 : 可以针对每一个属性值设置一个或者多个目标主题；
属性值可以是“_default”，表示如果';


-- 主题映射关系表【发布】 : 可以针对每一个属性值设置一个或者多个目标主题；
-- 属性值可以是“_default”，表示如果
CREATE TABLE IDMM_C_TOPIC_MAP_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 含_all
	ATTR_KEY varchar(32) NOT NULL COMMENT '属性KEY : 含_all',
	-- 含_default
	ATTR_VALUE varchar(32) NOT NULL COMMENT '属性值 : 含_default',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, SRC_TOPIC_ID, ATTR_KEY, ATTR_VALUE, DEST_TOPIC_ID)
) COMMENT = '主题映射关系表【发布】 : 可以针对每一个属性值设置一个或者多个目标主题；
属性值可以是“_default”，表示如果';


-- 主题发布关系表【编辑】 : 用于描述生产者客户端发布原始主题消息的权限关系；
CREATE TABLE IDMM_C_TOPIC_PUB_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID, SRC_TOPIC_ID),
	UNIQUE (CLIENT_ID, SRC_TOPIC_ID)
) COMMENT = '主题发布关系表【编辑】 : 用于描述生产者客户端发布原始主题消息的权限关系；';


-- 主题发布关系表【历史】 : 用于描述生产者客户端发布原始主题消息的权限关系；
CREATE TABLE IDMM_C_TOPIC_PUB_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, CLIENT_ID, SRC_TOPIC_ID),
	UNIQUE (CLIENT_ID, SRC_TOPIC_ID)
) COMMENT = '主题发布关系表【历史】 : 用于描述生产者客户端发布原始主题消息的权限关系；';


-- 主题发布关系表【发布】 : 用于描述生产者客户端发布原始主题消息的权限关系；
CREATE TABLE IDMM_C_TOPIC_PUB_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID, SRC_TOPIC_ID),
	UNIQUE (CLIENT_ID, SRC_TOPIC_ID)
) COMMENT = '主题发布关系表【发布】 : 用于描述生产者客户端发布原始主题消息的权限关系；';


-- 主题订阅关系表【编辑】 : 用于描述消费者客户端接收主题消息的关系；
CREATE TABLE IDMM_C_TOPIC_SUB_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	MAX_REQUEST int COMMENT '最大并发数',
	MIN_TIMEOUT int COMMENT '最小超时时间',
	MAX_TIMEOUT int COMMENT '最大超时时间',
	-- 最大消费速度限制， 单位 n/min
	CONSUME_SPEED_LIMIT int DEFAULT -1 NOT NULL COMMENT '消费速度限制 : 最大消费速度限制， 单位 n/min',
	-- 积压消息数  最大值
	MAX_MESSAGES int COMMENT '积压消息数最大值 : 积压消息数  最大值',
	-- 积压消息数告警值
	WARN_MESSAGES int COMMENT '积压消息数告警值 : 积压消息数告警值',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	-- 记录为新增或更新时，取Y，Y 是，N 否
	IS_MODIFIED char NOT NULL COMMENT '是否修改 : 记录为新增或更新时，取Y，Y 是，N 否',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID, DEST_TOPIC_ID),
	UNIQUE (CLIENT_ID, DEST_TOPIC_ID)
) COMMENT = '主题订阅关系表【编辑】 : 用于描述消费者客户端接收主题消息的关系；';


-- 主题订阅关系表【历史】 : 用于描述消费者客户端接收主题消息的关系；
CREATE TABLE IDMM_C_TOPIC_SUB_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	MAX_REQUEST int COMMENT '最大并发数',
	MIN_TIMEOUT int COMMENT '最小超时时间',
	MAX_TIMEOUT int COMMENT '最大超时时间',
	-- 最大消费速度限制， 单位 n/min
	CONSUME_SPEED_LIMIT int DEFAULT -1 NOT NULL COMMENT '消费速度限制 : 最大消费速度限制， 单位 n/min',
	-- 积压消息数  最大值
	MAX_MESSAGES int COMMENT '积压消息数最大值 : 积压消息数  最大值',
	-- 积压消息数告警值
	WARN_MESSAGES int COMMENT '积压消息数告警值 : 积压消息数告警值',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, CLIENT_ID, DEST_TOPIC_ID),
	UNIQUE (CLIENT_ID, DEST_TOPIC_ID)
) COMMENT = '主题订阅关系表【历史】 : 用于描述消费者客户端接收主题消息的关系；';


-- 主题订阅关系表【发布】 : 用于描述消费者客户端接收主题消息的关系；
CREATE TABLE IDMM_C_TOPIC_SUB_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	MAX_REQUEST int COMMENT '最大并发数',
	MIN_TIMEOUT int COMMENT '最小超时时间',
	MAX_TIMEOUT int COMMENT '最大超时时间',
	-- 最大消费速度限制， 单位 n/min
	CONSUME_SPEED_LIMIT int DEFAULT -1 NOT NULL COMMENT '消费速度限制 : 最大消费速度限制， 单位 n/min',
	-- 积压消息数  最大值
	MAX_MESSAGES int COMMENT '积压消息数最大值 : 积压消息数  最大值',
	-- 积压消息数告警值
	WARN_MESSAGES int COMMENT '积压消息数告警值 : 积压消息数告警值',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, CLIENT_ID, DEST_TOPIC_ID),
	UNIQUE (CLIENT_ID, DEST_TOPIC_ID)
) COMMENT = '主题订阅关系表【发布】 : 用于描述消费者客户端接收主题消息的关系；';


-- 在用版本信息表 : 每个集群只能有一个当前在用版本
CREATE TABLE IDMM_C_VERSION
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID)
) COMMENT = '在用版本信息表 : 每个集群只能有一个当前在用版本';


-- 版本配置数据校验规则表
CREATE TABLE IDMM_C_VERSION_CHECK
(
	-- 00 版本发布时的校验
	-- 01 业务处理时的校验，如删除主题时，校验该主题是否在用
	CHECK_TYPE varchar(120) NOT NULL COMMENT '校验大类 : 00 版本发布时的校验
01 业务处理时的校验，如删除主题时，校验该主题是否在用',
	-- 建议使用有意义的缩写，如TOPIC_IN_USE
	CHECK_NUM varchar(120) NOT NULL COMMENT '校验规则编号 : 建议使用有意义的缩写，如TOPIC_IN_USE',
	CHECK_OBJECT varchar(120) NOT NULL COMMENT '校验对象',
	-- 校验不通过时的文字描述
	CHECK_DESC varchar(200) NOT NULL COMMENT '校验规则中文描述 : 校验不通过时的文字描述',
	CHECK_SQL varchar(4000) NOT NULL COMMENT '校验sql',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	OP_NOTE varchar(2048) COMMENT '操作备注',
	PRIMARY KEY (CHECK_TYPE, CHECK_NUM)
) COMMENT = '版本配置数据校验规则表';


-- 版本历史表 : 该表中有且仅有一条记录的版本状态为’1’，就是当前在用的配置版本号；当有新版本发布时，在该表中插入新的记
CREATE TABLE IDMM_C_VERSION_HIS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	-- 用于描述版本创建的原因、来源等（如某需求）
	VERSION_DESC varchar(2048) NOT NULL COMMENT '版本描述 : 用于描述版本创建的原因、来源等（如某需求）',
	-- 描述版本变更的情况，如创建了xxx、删除了xxxx，json格式存储
	VERSION_CHANGE blob NOT NULL COMMENT '版本变更内容 : 描述版本变更的情况，如创建了xxx、删除了xxxx，json格式存储',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, VERSION_ID)
) COMMENT = '版本历史表 : 该表中有且仅有一条记录的版本状态为’1’，就是当前在用的配置版本号；当有新版本发布时，在该表中插入新的记';


-- 白名单信息表【编辑】 : 在该表中的IP都是允许接入的。
CREATE TABLE IDMM_C_WHITE_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 格式为:172.21.3.45
	IP varchar(15) NOT NULL COMMENT 'IP地址 : 格式为:172.21.3.45',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引ID : 用于与white_list_index关联',
	-- 0 无效，1 有效
	USE_STATUS char DEFAULT '1' NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, IP)
) COMMENT = '白名单信息表【编辑】 : 在该表中的IP都是允许接入的。';


-- 白名单信息表【历史】 : 在该表中的IP都是允许接入的。
CREATE TABLE IDMM_C_WHITE_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 格式为:172.21.3.45
	IP varchar(15) NOT NULL COMMENT 'IP地址 : 格式为:172.21.3.45',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引ID : 用于与white_list_index关联',
	-- 0 无效，1 有效
	USE_STATUS char DEFAULT '1' NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, IP)
) COMMENT = '白名单信息表【历史】 : 在该表中的IP都是允许接入的。';


-- 白名单信息索引表【编辑】
CREATE TABLE IDMM_C_WHITE_INDEX_EDIT
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引ID : 用于与white_list_index关联',
	BEGIN_IP varchar(15) NOT NULL COMMENT '起始IP地址',
	END_IP varchar(15) NOT NULL COMMENT '终止IP地址',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, INDEX_ID)
) COMMENT = '白名单信息索引表【编辑】';


-- 白名单信息索引表【历史】
CREATE TABLE IDMM_C_WHITE_INDEX_HIS
(
	-- 配置版本号
	VERSION_ID varchar(120) NOT NULL COMMENT '配置版本号 : 配置版本号',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引ID : 用于与white_list_index关联',
	BEGIN_IP varchar(15) NOT NULL COMMENT '起始IP地址',
	END_IP varchar(15) NOT NULL COMMENT '终止IP地址',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (VERSION_ID, CLUSTER_ID, INDEX_ID)
) COMMENT = '白名单信息索引表【历史】';


-- 白名单信息索引表【发布】
CREATE TABLE IDMM_C_WHITE_INDEX_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引ID : 用于与white_list_index关联',
	BEGIN_IP varchar(15) NOT NULL COMMENT '起始IP地址',
	END_IP varchar(15) NOT NULL COMMENT '终止IP地址',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, INDEX_ID)
) COMMENT = '白名单信息索引表【发布】';


-- 白名单信息表【发布】 : 在该表中的IP都是允许接入的。
CREATE TABLE IDMM_C_WHITE_RLS
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 格式为:172.21.3.45
	IP varchar(15) NOT NULL COMMENT 'IP地址 : 格式为:172.21.3.45',
	-- 用于与white_list_index关联
	INDEX_ID varchar(60) NOT NULL COMMENT '索引ID : 用于与white_list_index关联',
	-- 0 无效，1 有效
	USE_STATUS char DEFAULT '1' NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, IP)
) COMMENT = '白名单信息表【发布】 : 在该表中的IP都是允许接入的。';


-- BLE监控总表
CREATE TABLE IDMM_M_BLE
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int NOT NULL COMMENT 'TCP端口',
	JMX_PORT int NOT NULL COMMENT 'JMX端口',
	TCP_CONN_COUNT int NOT NULL COMMENT 'TCP端口连接数',
	JMX_CONN_COUNT int NOT NULL COMMENT 'JMX端口连接数',
	-- 0 备，1 主
	BLE_TYPE char NOT NULL COMMENT 'ble节点类型 : 0 备，1 主',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'BLE监控总表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- BLE监控明细表
CREATE TABLE IDMM_M_BLE_DETAIL
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'BLE监控明细表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- BLE监控明细表【历史】
CREATE TABLE IDMM_M_BLE_DETAIL_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'BLE监控明细表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- BLE监控总表【历史】
CREATE TABLE IDMM_M_BLE_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int NOT NULL COMMENT 'TCP端口',
	JMX_PORT int NOT NULL COMMENT 'JMX端口',
	TCP_CONN_COUNT int NOT NULL COMMENT 'TCP端口连接数',
	JMX_CONN_COUNT int NOT NULL COMMENT 'JMX端口连接数',
	-- 0 备，1 主
	BLE_TYPE char NOT NULL COMMENT 'ble节点类型 : 0 备，1 主',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'BLE监控总表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- BLE内存队列监控表
CREATE TABLE IDMM_M_BLE_MEM_QUEUE
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	TOTAL_MSG_COUNT bigint NOT NULL COMMENT '消息总数',
	CONSUMED_MSG_COUNT int NOT NULL COMMENT '已消费消息数',
	UN_CONSUMED_MSG_COUNT int NOT NULL COMMENT '未消费消息数',
	ON_WAY_MSG_COUNT int NOT NULL COMMENT '在途消息数',
	DB_QUEUE_MSG_COUNT int NOT NULL COMMENT 'DB队列消息数',
	ERROR_MSG_COUNT bigint NOT NULL COMMENT '错误消息数',
	MAX_UNSUB_TIME varchar(30) NOT NULL COMMENT '最长未消费时间',
	MAX_UNSIGN_TIME varchar(30) NOT NULL COMMENT '最长未签收时间',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'BLE内存队列监控表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- BLE内存队列监控表【历史】
CREATE TABLE IDMM_M_BLE_MEM_QUEUE_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	BLE_ID int NOT NULL COMMENT 'BLE节点标识',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	DEST_TOPIC_ID varchar(32) NOT NULL COMMENT '目标主题ID',
	-- 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。
	CLIENT_ID varchar(32) NOT NULL COMMENT '客户端ID : 客户端ID，生产者以P开头，消费者以S开头，特殊情况同一客户端会同时作为生产者与消费者。',
	TOTAL_MSG_COUNT bigint NOT NULL COMMENT '消息总数',
	CONSUMED_MSG_COUNT int NOT NULL COMMENT '已消费消息数',
	UN_CONSUMED_MSG_COUNT int NOT NULL COMMENT '未消费消息数',
	ON_WAY_MSG_COUNT int NOT NULL COMMENT '在途消息数',
	DB_QUEUE_MSG_COUNT int NOT NULL COMMENT 'DB队列消息数',
	ERROR_MSG_COUNT bigint NOT NULL COMMENT '错误消息数',
	MAX_UNSUB_TIME varchar(30) NOT NULL COMMENT '最长未消费时间',
	MAX_UNSIGN_TIME varchar(30) NOT NULL COMMENT '最长未签收时间',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'BLE内存队列监控表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- broker监控总表
CREATE TABLE IDMM_M_BROKER
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int NOT NULL COMMENT 'TCP端口',
	HTTP_PORT int NOT NULL COMMENT 'HTTP端口',
	JMX_PORT int NOT NULL COMMENT 'JMX端口',
	TCP_CONN_COUNT int NOT NULL COMMENT 'TCP端口连接数',
	HTTP_CONN_COUNT int NOT NULL COMMENT 'HTTP端口连接数',
	JMX_CONN_COUNT int NOT NULL COMMENT 'JMX端口连接数',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int DEFAULT 0.00 NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	-- 已发送消息数
	SEND_MSG_COUNT int NOT NULL COMMENT '已发送状态的消息数 : 已发送消息数',
	-- 发送且提交消息数，即已确认消息数
	SEND_COMMIT_MSG_COUNT int NOT NULL COMMENT '发送且提交状态的消息数 : 发送且提交消息数，即已确认消息数',
	-- 已接收且提交消息数，fetch确认消息数
	RECEIVE_COMMIT_MSG_COUNT int NOT NULL COMMENT '已接收且提交状态的消息数 : 已接收且提交消息数，fetch确认消息数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'broker监控总表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- broker监控总表【历史】
CREATE TABLE IDMM_M_BROKER_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int NOT NULL COMMENT 'TCP端口',
	HTTP_PORT int NOT NULL COMMENT 'HTTP端口',
	JMX_PORT int NOT NULL COMMENT 'JMX端口',
	TCP_CONN_COUNT int NOT NULL COMMENT 'TCP端口连接数',
	HTTP_CONN_COUNT int NOT NULL COMMENT 'HTTP端口连接数',
	JMX_CONN_COUNT int NOT NULL COMMENT 'JMX端口连接数',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int DEFAULT 0.00 NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	-- 已发送消息数
	SEND_MSG_COUNT int NOT NULL COMMENT '已发送状态的消息数 : 已发送消息数',
	-- 发送且提交消息数，即已确认消息数
	SEND_COMMIT_MSG_COUNT int NOT NULL COMMENT '发送且提交状态的消息数 : 发送且提交消息数，即已确认消息数',
	-- 已接收且提交消息数，fetch确认消息数
	RECEIVE_COMMIT_MSG_COUNT int NOT NULL COMMENT '已接收且提交状态的消息数 : 已接收且提交消息数，fetch确认消息数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'broker监控总表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- broker监控明细表
CREATE TABLE IDMM_M_BROKER_TPS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'broker监控明细表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- broker监控明细表【历史】
CREATE TABLE IDMM_M_BROKER_TPS_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	SRC_TOPIC_ID varchar(32) NOT NULL COMMENT '原始主题ID',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'broker监控明细表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- manager节点监控信息表
CREATE TABLE IDMM_M_MANAGER
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'manager节点监控信息表';


-- manager节点监控信息表【历史】
CREATE TABLE IDMM_M_MANAGER_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'manager节点监控信息表【历史】';


-- kafka授权用户信息表 : 用于做kafka的权限控制，该表的数据由manager后台定时写入。
-- 每次写入前，先将原
CREATE TABLE KFK_C_AUTH_USER
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	AUTH_USER_NAME varchar(120) NOT NULL COMMENT '授权用户名',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, AUTH_USER_NAME)
) COMMENT = 'kafka授权用户信息表 : 用于做kafka的权限控制，该表的数据由manager后台定时写入。
每次写入前，先将原';


-- kafka-Broker信息表
CREATE TABLE KFK_C_BROKER
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- >0
	BROKER_ID int NOT NULL COMMENT 'Broker节点标识 : >0',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	TCP_PORT int NOT NULL COMMENT 'TCP端口',
	HTTP_PORT int NOT NULL COMMENT 'HTTP端口',
	JMX_PORT int NOT NULL COMMENT 'JMX端口',
	INSTALL_DIR varchar(200) NOT NULL COMMENT '安装目录',
	-- 0 无效，1 有效
	USE_STATUS char NOT NULL COMMENT '使用标志 : 0 无效，1 有效',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, BROKER_ID)
) COMMENT = 'kafka-Broker信息表';


-- kafka主题信息表
CREATE TABLE KFK_C_TOPIC
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- broker监控明细表中存储的是原始主题
	-- ble监控明细表中存储的是目标主题
	TOPIC_ID varchar(32) NOT NULL COMMENT '主题ID : broker监控明细表中存储的是原始主题
ble监控明细表中存储的是目标主题',
	TOPIC_NAME varchar(32) NOT NULL COMMENT '主题名称',
	PARTITION_COUNT varchar(32) NOT NULL COMMENT '分区数',
	REPLICA_COUNT varchar(512) NOT NULL COMMENT '副本数',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, TOPIC_ID)
) COMMENT = 'kafka主题信息表';


-- kafka主题授权记录表 : 记录主题授权的流水记录
CREATE TABLE KFK_C_TOPIC_AUTH_REC
(
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- broker监控明细表中存储的是原始主题
	-- ble监控明细表中存储的是目标主题
	TOPIC_ID varchar(32) NOT NULL COMMENT '主题ID : broker监控明细表中存储的是原始主题
ble监控明细表中存储的是目标主题',
	AUTH_TYPE char NOT NULL COMMENT '授权类型',
	COND_USER_NAME varchar(120) COMMENT '用户名条件',
	COND_CLIENT_ID varchar(120) COMMENT '客户端ID条件',
	COND_OPERATION_TYPE char COMMENT '操作类型条件',
	-- *表示所有IP
	COND_IP varchar(120) COMMENT 'IP条件 : *表示所有IP',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (LOGIN_ACCEPT)
) COMMENT = 'kafka主题授权记录表 : 记录主题授权的流水记录';


-- kafka主题订阅关系表 : 用于描述消费者客户端接收主题消息的关系；
CREATE TABLE KFK_C_TOPIC_SUB
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- broker监控明细表中存储的是原始主题
	-- ble监控明细表中存储的是目标主题
	TOPIC_ID varchar(32) NOT NULL COMMENT '主题ID : broker监控明细表中存储的是原始主题
ble监控明细表中存储的是目标主题',
	CONSUME_GROUP_ID varchar(32) NOT NULL COMMENT '消费组ID',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, TOPIC_ID, CONSUME_GROUP_ID)
) COMMENT = 'kafka主题订阅关系表 : 用于描述消费者客户端接收主题消息的关系；';


-- kafka主题监控表
CREATE TABLE KFK_M_TOPIC
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	-- broker监控明细表中存储的是原始主题
	-- ble监控明细表中存储的是目标主题
	TOPIC_ID varchar(32) NOT NULL COMMENT '主题ID : broker监控明细表中存储的是原始主题
ble监控明细表中存储的是目标主题',
	PARTITION_ID varchar(30) NOT NULL COMMENT '分区',
	-- 消费者ID
	CONSUMER_ID varchar(32) COMMENT '消费者ID : 消费者ID',
	-- 表示该partition已经写了多少条message
	LOGSIZE int COMMENT '消息总量 : 表示该partition已经写了多少条message',
	-- 表示该parition已经消费了多少条message
	OFFSET int COMMENT 'OFFSET量 : 表示该parition已经消费了多少条message',
	-- 表示有多少条message没有被消费。
	LAG int COMMENT 'LAG量 : 表示有多少条message没有被消费。',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	RECEIVE_TPS int COMMENT '收TPS',
	SEND_TPS int COMMENT '发TPS',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'kafka主题监控表';


-- kafka主题监控表【历史】
CREATE TABLE KFK_M_TOPIC_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	-- broker监控明细表中存储的是原始主题
	-- ble监控明细表中存储的是目标主题
	TOPIC_ID varchar(32) NOT NULL COMMENT '主题ID : broker监控明细表中存储的是原始主题
ble监控明细表中存储的是目标主题',
	PARTITION_ID varchar(30) NOT NULL COMMENT '分区',
	-- 消费者ID
	CONSUMER_ID varchar(32) COMMENT '消费者ID : 消费者ID',
	-- 表示该partition已经写了多少条message
	LOGSIZE int COMMENT '消息总量 : 表示该partition已经写了多少条message',
	-- 表示该parition已经消费了多少条message
	OFFSET int COMMENT 'OFFSET量 : 表示该parition已经消费了多少条message',
	-- 表示有多少条message没有被消费。
	LAG int COMMENT 'LAG量 : 表示有多少条message没有被消费。',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	RECEIVE_TPS int COMMENT '收TPS',
	SEND_TPS int COMMENT '发TPS',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'kafka主题监控表【历史】';


-- 集群信息
CREATE TABLE SYS_CLUSTER
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	CLUSTER_NAME varchar(60) NOT NULL COMMENT '集群名称',
	-- IDMM 交易型
	-- KAFKA 流处理型
	CLUSTER_TYPE varchar(5) NOT NULL COMMENT '集群类型 : IDMM 交易型
KAFKA 流处理型',
	CREATE_NO varchar(32) NOT NULL COMMENT '创建工号',
	CREATE_TIME datetime NOT NULL COMMENT '创建时间',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID)
) COMMENT = '集群信息';


-- 数据库信息表 : 记录集群使用的数据库信息，1个集群对应多个数据库
CREATE TABLE SYS_DB
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 0 配置库，1 消息运行库
	DB_USE_TYPE char NOT NULL COMMENT '数据库用途 : 0 配置库，1 消息运行库',
	-- MYSQL、ORACLE、HBASE等
	DB_TYPE varchar(20) NOT NULL COMMENT '数据库类型 : MYSQL、ORACLE、HBASE等',
	-- 可能是1个或多个ip地址，逗号分隔
	DB_IP varchar(200) NOT NULL COMMENT '数据库IP : 可能是1个或多个ip地址，逗号分隔',
	-- 存储多个ip对应的端口，逗号分隔
	DB_PORT varchar(200) NOT NULL COMMENT '数据库端口 : 存储多个ip对应的端口，逗号分隔',
	DB_USER varchar(60) COMMENT '数据库用户名',
	-- 需要加密
	DB_PWD varchar(60) COMMENT '数据库密码 : 需要加密',
	-- 不同的数据库有不同的附加信息，json格式表示
	DB_EXT_INFO varchar(600) COMMENT '数据库附加信息 : 不同的数据库有不同的附加信息，json格式表示',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注'
) COMMENT = '数据库信息表 : 记录集群使用的数据库信息，1个集群对应多个数据库';


-- 功能信息表
CREATE TABLE SYS_FUNCTION
(
	-- 默认顶级节点为9999
	-- 编码为4位，
	-- 第3位意义：
	-- 0 idmm、kafka公用
	-- 1 idmm使用
	-- 2 kafka使用
	-- 
	-- 
	FUNC_CODE varchar(30) NOT NULL COMMENT '功能编码 : 默认顶级节点为9999
编码为4位，
第3位意义：
0 idmm、kafka公用
1 idmm使用
2 kafka使用

',
	FUNC_NAME varchar(120) NOT NULL COMMENT '功能名称',
	PARENT_CODE varchar(30) NOT NULL COMMENT '父功能',
	NODE_LEVEL int NOT NULL COMMENT '层级',
	-- N 否，Y 是
	IS_LEAF char NOT NULL COMMENT '是否为叶子节点 : N 否，Y 是',
	-- IDMM 交易型
	-- KAFKA 流处理型
	FUNC_TYPE char COMMENT '功能类型 : IDMM 交易型
KAFKA 流处理型',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (FUNC_CODE)
) COMMENT = '功能信息表';


-- 功能对应的服务
CREATE TABLE SYS_FUNC_SVC
(
	-- 默认顶级节点为9999
	-- 编码为4位，
	-- 第3位意义：
	-- 0 idmm、kafka公用
	-- 1 idmm使用
	-- 2 kafka使用
	-- 
	-- 
	FUNC_CODE varchar(30) NOT NULL COMMENT '功能编码 : 默认顶级节点为9999
编码为4位，
第3位意义：
0 idmm、kafka公用
1 idmm使用
2 kafka使用

',
	-- rest请求链接
	SVC_URL varchar(120) NOT NULL COMMENT '服务链接 : rest请求链接',
	SVC_DESC varchar(120) NOT NULL COMMENT '服务用途描述',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (FUNC_CODE, SVC_URL)
) COMMENT = '功能对应的服务';


-- 主机信息表 : 用于存储集群用到的主机信息
CREATE TABLE SYS_HOST
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	HOST_USER varchar(120) NOT NULL COMMENT '主机用户名',
	-- 密文保存
	HOST_PWD varchar(60) COMMENT '主机密码 : 密文保存',
	HOST_OS varchar(120) NOT NULL COMMENT '主机操作系统',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, IP)
) COMMENT = '主机信息表 : 用于存储集群用到的主机信息';


-- 系统日志表 : 记录谁在什么时间做了什么事情
CREATE TABLE SYS_LOG
(
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	CLUSTER_ID varchar(120) COMMENT '集群ID',
	-- 默认顶级节点为9999
	-- 编码为4位，
	-- 第3位意义：
	-- 0 idmm、kafka公用
	-- 1 idmm使用
	-- 2 kafka使用
	-- 
	-- 
	FUNC_CODE varchar(30) NOT NULL COMMENT '功能编码 : 默认顶级节点为9999
编码为4位，
第3位意义：
0 idmm、kafka公用
1 idmm使用
2 kafka使用

',
	-- 配置版本号
	VERSION_ID varchar(120) COMMENT '配置版本号 : 配置版本号',
	-- 描述操作的具体内容
	LOG_TEXT varchar(2048) COMMENT '操作描述 : 描述操作的具体内容',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (LOGIN_ACCEPT)
) COMMENT = '系统日志表 : 记录谁在什么时间做了什么事情';


-- manager信息表 : 集群对应的manager节点信息
CREATE TABLE SYS_MANAGER
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, IP, PORT)
) COMMENT = 'manager信息表 : 集群对应的manager节点信息';


-- 角色信息表
CREATE TABLE SYS_ROLE
(
	ROLE_CODE varchar(60) NOT NULL COMMENT '角色编码',
	ROLE_NAME varchar(120) NOT NULL COMMENT '角色名称',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (ROLE_CODE)
) COMMENT = '角色信息表';


-- 角色功能关系表
CREATE TABLE SYS_ROLE_FUNCTION
(
	ROLE_CODE varchar(60) NOT NULL COMMENT '角色编码',
	-- 默认顶级节点为9999
	-- 编码为4位，
	-- 第3位意义：
	-- 0 idmm、kafka公用
	-- 1 idmm使用
	-- 2 kafka使用
	-- 
	-- 
	FUNC_CODE varchar(30) NOT NULL COMMENT '功能编码 : 默认顶级节点为9999
编码为4位，
第3位意义：
0 idmm、kafka公用
1 idmm使用
2 kafka使用

',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (ROLE_CODE, FUNC_CODE)
) COMMENT = '角色功能关系表';


-- 租户资源关系表 : 存储租户拥有的资源，如集群、客户端等
CREATE TABLE SYS_TENANT_RES
(
	LOGIN_NO varchar(120) NOT NULL COMMENT '用户编码',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 00 客户端，01 xxx
	RES_TYPE varchar(2) NOT NULL COMMENT '资源类型 : 00 客户端，01 xxx',
	RES_VALUE varchar(200) NOT NULL COMMENT '资源标识取值',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (LOGIN_NO, CLUSTER_ID, RES_TYPE, RES_VALUE)
) COMMENT = '租户资源关系表 : 存储租户拥有的资源，如集群、客户端等';


-- 用户信息表
CREATE TABLE SYS_USER
(
	LOGIN_NO varchar(120) NOT NULL COMMENT '用户编码',
	LOGIN_NAME varchar(120) NOT NULL COMMENT '用户名称',
	PWD varchar(60) NOT NULL COMMENT '用户密码',
	-- 0 未登录，1 已登录
	IS_LOGIN char NOT NULL COMMENT '是否已登录 : 0 未登录，1 已登录',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (LOGIN_NO)
) COMMENT = '用户信息表';


-- 用户集群关系表
CREATE TABLE SYS_USER_CLUSTER
(
	LOGIN_NO varchar(120) NOT NULL COMMENT '用户编码',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (LOGIN_NO, CLUSTER_ID)
) COMMENT = '用户集群关系表';


-- 用户角色关系表
CREATE TABLE SYS_USER_ROLE
(
	LOGIN_NO varchar(120) NOT NULL COMMENT '用户编码',
	ROLE_CODE varchar(60) NOT NULL COMMENT '角色编码',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (LOGIN_NO)
) COMMENT = '用户角色关系表';


-- zookeeper信息表 : 用于存储集群用到的zookeeper信息，1个集群对应多个zookeeper
CREATE TABLE SYS_ZOOKEEPER
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	-- 操作工号
	OP_NO varchar(32) NOT NULL COMMENT '操作工号 : 操作工号',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	OP_NOTE varchar(120) COMMENT '操作备注',
	PRIMARY KEY (CLUSTER_ID, IP, PORT)
) COMMENT = 'zookeeper信息表 : 用于存储集群用到的zookeeper信息，1个集群对应多个zookeeper';


-- 代码表 : 用于存储各种枚举值
CREATE TABLE T_C_DICT
(
	-- 表名称，大写
	TABLE_NAME varchar(120) NOT NULL COMMENT '表名 : 表名称，大写',
	-- 列名称，大写
	COLUMN_NAME varchar(120) NOT NULL COMMENT '列名称 : 列名称，大写',
	-- 默认为1
	ORDER_ID int NOT NULL COMMENT '排列顺序 : 默认为1',
	VALUE varchar(120) NOT NULL COMMENT '取值',
	TEXT_ZH_CN varchar(120) NOT NULL COMMENT '中文文本',
	NOTE varchar(2048) COMMENT '备注',
	PRIMARY KEY (TABLE_NAME, COLUMN_NAME, ORDER_ID)
) COMMENT = '代码表 : 用于存储各种枚举值';


-- 序列取值表 : 该表用于模拟序列生成各种ID的值，
CREATE TABLE T_C_SEQ
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 00 集群ID
	-- 01 idmm的版本号ID
	-- 02 idmm的brokerID
	-- 03 idmm的BLEID
	-- 04 kafka的brokerID
	SEQ_TYPE char(2) NOT NULL COMMENT '序列类型 : 00 集群ID
01 idmm的版本号ID
02 idmm的brokerID
03 idmm的BLEID
04 kafka的brokerID',
	INIT_VAL int NOT NULL COMMENT '初始值',
	NEXT_VAL int NOT NULL COMMENT '下一个值',
	CUR_VAL int NOT NULL COMMENT '当前值',
	VAL_STEP int NOT NULL COMMENT '序列增长步长',
	PRIMARY KEY (CLUSTER_ID, SEQ_TYPE)
) COMMENT = '序列取值表 : 该表用于模拟序列生成各种ID的值，';


-- 告警记录表
CREATE TABLE T_M_ALARM
(
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	ALARM_TYPE char NOT NULL COMMENT '告警类型',
	ALARM_CONTENT varchar(2048) NOT NULL COMMENT '告警详情',
	ALARM_LEVEL char NOT NULL COMMENT '告警级别',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	-- 格式为YYYYMMDD
	OP_TIME_YMD varchar(8) NOT NULL COMMENT '操作时间YMD格式 : 格式为YYYYMMDD',
	PRIMARY KEY (LOGIN_ACCEPT)
) COMMENT = '告警记录表';


-- 告警记录表【历史】
CREATE TABLE T_M_ALARM_HIS
(
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	ALARM_TYPE char NOT NULL COMMENT '告警类型',
	ALARM_CONTENT varchar(2048) NOT NULL COMMENT '告警详情',
	ALARM_LEVEL char NOT NULL COMMENT '告警级别',
	OP_TIME datetime NOT NULL COMMENT '操作时间',
	-- 格式为YYYYMMDD
	OP_TIME_YMD varchar(8) NOT NULL COMMENT '操作时间YMD格式 : 格式为YYYYMMDD',
	PRIMARY KEY (LOGIN_ACCEPT)
) COMMENT = '告警记录表【历史】';


-- 告警提醒方式配置表
CREATE TABLE T_M_ALARM_OPTION
(
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 00 提醒方式
	-- 11 提醒频率日期
	-- 12 提醒频率时间段
	-- 20 阀值：主机
	-- 21 阀值：积压消息
	OPTION_KEY varchar(2) NOT NULL COMMENT '告警配置key : 00 提醒方式
11 提醒频率日期
12 提醒频率时间段
20 阀值：主机
21 阀值：积压消息',
	-- 00 提醒方式：短信--则此处填写手机号，多个以逗号隔开
	-- 01 提醒方式：邮件--则此处填写邮箱，多个以逗号隔开
	-- 11 提醒排除月日期--1，表示每月的1日不提醒，此配置优先级最高
	-- 12 提醒周日期--00000000,代表周一~周日，如果对应位为1，则表示选中
	-- 13 提醒时间段--格式：8:00~9:00,10:00~12:00，多个时间段用逗号隔开
	-- 20 阀值：主机CPU--0.9,0.8,0.7,0.6, 表示4个级别的告警阀值，级别从高到低,以逗号隔开
	-- 21 阀值：积压消息--123,100,50,1, 表示4个级别的告警阀值，级别从高到低,以逗号隔开
	OPTION_VALUE varchar(1024) NOT NULL COMMENT '告警配置项value : 00 提醒方式：短信--则此处填写手机号，多个以逗号隔开
01 提醒方式：邮件--则此处填写邮箱，多个以逗号隔开
11 提醒排除月日期--1，表示每月的1日不提醒，此配置优先级最高
12 提醒周日期--00000000,代表周一~周日，如果对应位为1，则表示选中
13 提醒时间段--格式：8:00~9:00,10:00~12:00，多个时间段用逗号隔开
20 阀值：主机CPU--0.9,0.8,0.7,0.6, 表示4个级别的告警阀值，级别从高到低,以逗号隔开
21 ',
	PRIMARY KEY (CLUSTER_ID, OPTION_KEY)
) COMMENT = '告警提醒方式配置表';


-- 集群监控表
CREATE TABLE T_M_CLUSTER
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int DEFAULT 0.00 NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	-- tps/5min
	TPS_5 int NOT NULL COMMENT 'TPS/5min : tps/5min',
	-- tps/10min
	TPS_10 int NOT NULL COMMENT 'TPS/10min : tps/10min',
	-- tps/30min
	TPS_30 int NOT NULL COMMENT 'TPS/30min : tps/30min',
	HOST_COUNT int NOT NULL COMMENT '主机数',
	BROKER_COUNT int NOT NULL COMMENT 'Broker实例数',
	TOPIC_COUNT int NOT NULL COMMENT '主题数',
	SUB_COUNT int NOT NULL COMMENT '订阅者数量',
	-- 客户端连接数，当前在线的客户端连接数
	CLIENT_CONN_COUNT int NOT NULL COMMENT '客户端连接数 : 客户端连接数，当前在线的客户端连接数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '集群监控表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 集群监控表【历史】
CREATE TABLE T_M_CLUSTER_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	SEND_TPS int NOT NULL COMMENT '发TPS',
	RECEIVE_TPS int NOT NULL COMMENT '收TPS',
	-- 收的tps+发的tps，60s计算一次的tps
	TPS int DEFAULT 0.00 NOT NULL COMMENT 'TPS : 收的tps+发的tps，60s计算一次的tps',
	-- tps/5min
	TPS_5 int NOT NULL COMMENT 'TPS/5min : tps/5min',
	-- tps/10min
	TPS_10 int NOT NULL COMMENT 'TPS/10min : tps/10min',
	-- tps/30min
	TPS_30 int NOT NULL COMMENT 'TPS/30min : tps/30min',
	HOST_COUNT int NOT NULL COMMENT '主机数',
	BROKER_COUNT int NOT NULL COMMENT 'Broker实例数',
	TOPIC_COUNT int NOT NULL COMMENT '主题数',
	SUB_COUNT int NOT NULL COMMENT '订阅者数量',
	-- 客户端连接数，当前在线的客户端连接数
	CLIENT_CONN_COUNT int NOT NULL COMMENT '客户端连接数 : 客户端连接数，当前在线的客户端连接数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '集群监控表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 主机资源监控表 : kafka与idmm公用
CREATE TABLE T_M_HOST
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	DISK_IO varchar(120) NOT NULL COMMENT '磁盘IO',
	NETWORK_IO varchar(30) NOT NULL COMMENT '网卡IO',
	-- 磁盘使用率
	DISK_USE float(5,2) NOT NULL COMMENT '磁盘使用率 : 磁盘使用率',
	-- 内存使用率
	MEM_USE float(5,2) NOT NULL COMMENT '内存使用率 : 内存使用率',
	-- CPU使用率
	CPU_USE float(5,2) NOT NULL COMMENT 'CPU使用率 : CPU使用率',
	LOAD_COUNT int NOT NULL COMMENT 'LOAD次数',
	CONN_COUNT int NOT NULL COMMENT '连接数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '主机资源监控表 : kafka与idmm公用';


-- 主机连接明细表 : kafka与idmm公用
CREATE TABLE T_M_HOST_CONN
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	-- 用于区分是broker或ble或其他
	PROCESS_TYPE char(2) NOT NULL COMMENT '进程类型 : 用于区分是broker或ble或其他',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	CLIENT_IP varchar(15) NOT NULL COMMENT '客户端IP',
	CLIENT_PORT int NOT NULL COMMENT '客户端端口',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '主机连接明细表 : kafka与idmm公用';


-- 主机连接明细表【历史】 : kafka与idmm公用
CREATE TABLE T_M_HOST_CONN_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应
	PARENT_ACCEPT varchar(128) NOT NULL COMMENT '父流水ID : 用于批量操作，一笔业务需要记录多条日志时，与总表中的LOGIN_ACCEPT对应',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	-- 用于区分是broker或ble或其他
	PROCESS_TYPE char(2) NOT NULL COMMENT '进程类型 : 用于区分是broker或ble或其他',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	CLIENT_IP varchar(15) NOT NULL COMMENT '客户端IP',
	CLIENT_PORT int NOT NULL COMMENT '客户端端口',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '主机连接明细表【历史】 : kafka与idmm公用';


-- 主机资源监控表【历史】 : kafka与idmm公用
CREATE TABLE T_M_HOST_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	DISK_IO varchar(120) NOT NULL COMMENT '磁盘IO',
	NETWORK_IO varchar(30) NOT NULL COMMENT '网卡IO',
	-- 磁盘使用率
	DISK_USE float(5,2) NOT NULL COMMENT '磁盘使用率 : 磁盘使用率',
	-- 内存使用率
	MEM_USE float(5,2) NOT NULL COMMENT '内存使用率 : 内存使用率',
	-- CPU使用率
	CPU_USE float(5,2) NOT NULL COMMENT 'CPU使用率 : CPU使用率',
	LOAD_COUNT int NOT NULL COMMENT 'LOAD次数',
	CONN_COUNT int NOT NULL COMMENT '连接数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '主机资源监控表【历史】 : kafka与idmm公用';


-- 日志监控表
CREATE TABLE T_M_LOG
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	-- 0 broker日志
	-- 1 ble日志
	-- 2 zookeeper日志
	LOG_TYPE char NOT NULL COMMENT '日志类型 : 0 broker日志
1 ble日志
2 zookeeper日志',
	-- 根目录文件名，如/xxx/xxx/x/
	LOG_DIR varchar(120) NOT NULL COMMENT '日志目录 : 根目录文件名，如/xxx/xxx/x/',
	LOG_FILIE_NAME varchar(120) NOT NULL COMMENT '日志文件名称',
	LOG_KEY_WORD varchar(120) NOT NULL COMMENT '日志关键字',
	FIND_TIMES int NOT NULL COMMENT '日志关键字出现次数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '日志监控表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 日志监控表【历史】
CREATE TABLE T_M_LOG_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	-- 0 broker日志
	-- 1 ble日志
	-- 2 zookeeper日志
	LOG_TYPE char NOT NULL COMMENT '日志类型 : 0 broker日志
1 ble日志
2 zookeeper日志',
	-- 根目录文件名，如/xxx/xxx/x/
	LOG_DIR varchar(120) NOT NULL COMMENT '日志目录 : 根目录文件名，如/xxx/xxx/x/',
	LOG_FILIE_NAME varchar(120) NOT NULL COMMENT '日志文件名称',
	LOG_KEY_WORD varchar(120) NOT NULL COMMENT '日志关键字',
	FIND_TIMES int NOT NULL COMMENT '日志关键字出现次数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '日志监控表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 进程监控总表
CREATE TABLE T_M_PROCESS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PROCESS_PATH varchar(120) NOT NULL COMMENT '进程路径',
	PROCESS_NAME varchar(1024) NOT NULL COMMENT '进程名称（带参数）',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	LIVE_TIME bigint NOT NULL COMMENT '存活时间（单位：秒）',
	LAST_START_TIME datetime NOT NULL COMMENT '进程最近一次启动时间',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '进程监控总表' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 进程监控总表【历史】
CREATE TABLE T_M_PROCESS_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PROCESS_PATH varchar(120) NOT NULL COMMENT '进程路径',
	PROCESS_NAME varchar(1024) NOT NULL COMMENT '进程名称（带参数）',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	LIVE_TIME bigint NOT NULL COMMENT '存活时间（单位：秒）',
	LAST_START_TIME datetime NOT NULL COMMENT '进程最近一次启动时间',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = '进程监控总表【历史】' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- zookeeper监控信息表
CREATE TABLE T_M_ZOOKEEPER
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	ZK_NODE_ID int NOT NULL COMMENT 'zk集群中的节点id',
	-- 0:follower,1:leader
	IDENTITY char NOT NULL COMMENT 'zookeeper节点类型 : 0:follower,1:leader',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	-- 客户端连接数，当前在线的客户端连接数
	CLIENT_CONN_COUNT int NOT NULL COMMENT '客户端连接数 : 客户端连接数，当前在线的客户端连接数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'zookeeper监控信息表';


-- zookeeper监控信息表【历史】
CREATE TABLE T_M_ZOOKEEPER_HIS
(
	LOT_NO varchar(60) NOT NULL COMMENT '批次号',
	-- 唯一标识，使用uuid生成
	LOGIN_ACCEPT varchar(128) NOT NULL COMMENT '流水ID : 唯一标识，使用uuid生成',
	-- 监控时间,YYYYMMDDHH24MISS
	MONITOR_TIME datetime NOT NULL COMMENT '监控时间 : 监控时间,YYYYMMDDHH24MISS',
	CLUSTER_ID varchar(120) NOT NULL COMMENT '集群ID',
	IP varchar(15) NOT NULL COMMENT 'IP地址',
	PORT int NOT NULL COMMENT '端口',
	ZK_NODE_ID int NOT NULL COMMENT 'zk集群中的节点id',
	-- 0:follower,1:leader
	IDENTITY char NOT NULL COMMENT 'zookeeper节点类型 : 0:follower,1:leader',
	-- 0 异常，1 正常
	RUN_STATUS char NOT NULL COMMENT '运行状态 : 0 异常，1 正常',
	-- 客户端连接数，当前在线的客户端连接数
	CLIENT_CONN_COUNT int NOT NULL COMMENT '客户端连接数 : 客户端连接数，当前在线的客户端连接数',
	PRIMARY KEY (LOT_NO, LOGIN_ACCEPT)
) COMMENT = 'zookeeper监控信息表【历史】';



