

*****说明 2017-12-29
   这个文件是用于 idmm 测试连接 tidb 环境的, 其接口是 mysql 协议的.
   
/*
[crmpdscm@172.21.0.46]/crmpdscm/idmm3/broker1

zkCli.sh -server 172.21.0.46:7182
create /idmm 0 0 0
create /idmm/configServer 0 0 0
create /idmm/configServer/version 0 0 0

/crmpdscm/idmm3/broker1/py/idmm.py
   
e:/00work@2017/idmm/sc_py/idmm.py
*/ 

CREATE TABLE `ble_base_info_0` (
	`BLE_id` DECIMAL(8,0) NOT NULL COMMENT 'BLE节点标识',
	`id_number` DECIMAL(1,0) NOT NULL COMMENT '节点序号',
	`addr_ip` CHAR(15) NOT NULL COMMENT '节点ip地址',
	`addr_port` DECIMAL(5,0) NOT NULL COMMENT '节点通信端口',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1\\r\\n指配置上的节点使用标志，以方便人工停用某些节点，不是实际生产中节点的实际运行状态；\\r\\n生产中实际运行的节点状态可以从zookeeper中获得； \\r\\n1：在用\\r\\n0：停用',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`BLE_id`, `id_number`),
	UNIQUE INDEX `BLE_id` (`BLE_id`, `id_number`)
);

CREATE TABLE `ble_dest_topic_rel_0` (
	`dest_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`BLE_id` DECIMAL(8,0) NOT NULL COMMENT 'BLE节点标识',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`dest_topic_id`, `BLE_id`),
	UNIQUE INDEX `dest_topic_id` (`dest_topic_id`, `BLE_id`)
);

CREATE TABLE `broker_base_info_0` (
	`broker_id` DECIMAL(8,0) NOT NULL COMMENT 'Broker节点标识 : >0',
	`comm_ip` CHAR(15) NOT NULL COMMENT 'ip地址 : IP地址格式',
	`comm_port` DECIMAL(15,0) NOT NULL COMMENT '通信端口 : 1025-65535',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1\\r\\n指配置上的节点使用标志，以方便人工停用某些节点，不是实际生产中节点的实际运行状态；\\r\\n生产中实际运行的节点状态可以从zookeeper中获得； \\r\\n1：在用\\r\\n0：停用',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`broker_id`)
);

CREATE TABLE `client_base_info_0` (
	`client_id` VARCHAR(32) NOT NULL DEFAULT '',
	`sub_system` CHAR(32) NOT NULL COMMENT '归属子系统 : 子系统名称',
	`client_desc` VARCHAR(2048) NOT NULL COMMENT 'Client身份说明 : 自定义格式',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0：停用\\r\\n1：使用',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`client_id`)
);

CREATE TABLE `client_limit_info_0` (
	`client_id` CHAR(8) NOT NULL COMMENT 'client标识',
	`limit_key` CHAR(8) NOT NULL COMMENT '限制类型',
	`limit_value` VARCHAR(2048) NOT NULL COMMENT '限制范围',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`client_id`, `limit_key`)
);

CREATE TABLE `consume_notice_info_0` (
	`producer_client_id` CHAR(32) NOT NULL COMMENT '生产者客户端id',
	`src_topic_id` CHAR(32) NOT NULL COMMENT '原始主题id : 前缀s',
	`dest_topic_id` CHAR(32) NOT NULL COMMENT '目标主题id',
	`consumer_client_id` CHAR(32) NOT NULL COMMENT '消费者客户端',
	`notice_topic_id` CHAR(32) NOT NULL COMMENT '消费结果目标主题',
	`notice_client_id` CHAR(32) NOT NULL COMMENT '接收消费结果的客户端id，可以和生产者相同',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`producer_client_id`, `src_topic_id`, `dest_topic_id`, `consumer_client_id`, `notice_topic_id`),
	UNIQUE INDEX `producer_client_id` (`producer_client_id`, `src_topic_id`, `dest_topic_id`, `consumer_client_id`)
);

CREATE TABLE `consume_order_info_0` (
	`producer_client_id` CHAR(8) NOT NULL COMMENT '生产者客户端id',
	`src_topic_id` CHAR(8) NOT NULL COMMENT '原始主题id : 前缀s',
	`attribute_key` CHAR(32) NOT NULL COMMENT '属性key : 含_all',
	`attribute_value` CHAR(32) NOT NULL COMMENT '属性value : 含_default',
	`dest_topic_id` CHAR(8) NOT NULL COMMENT '目标主题id',
	`consumer_client_id` CHAR(8) NOT NULL COMMENT '消费者客户端',
	`consume_seq` INT(11) NOT NULL COMMENT '消费次序 : 从0开始计数',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`producer_client_id`, `src_topic_id`, `attribute_key`, `attribute_value`, `dest_topic_id`, `consumer_client_id`, `consume_seq`),
	UNIQUE INDEX `producer_client_id` (`producer_client_id`, `src_topic_id`, `attribute_key`, `attribute_value`, `dest_topic_id`, `consumer_client_id`, `consume_seq`)
);

CREATE TABLE `dest_topic_info_0` (
	`dest_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`dest_topic_desc` VARCHAR(2048) NOT NULL COMMENT '目标主题描述',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`dest_topic_id`)
);

CREATE TABLE `priority_map_0` (
	`pname` VARCHAR(32) NOT NULL COMMENT '优先级名称',
	`pvalue` INT(11) NOT NULL COMMENT '优先级数字',
	`is_default` CHAR(1) NULL DEFAULT NULL COMMENT '是否默认优先级， 只能有一个,取值Y|N',
	`note` VARCHAR(64) NULL DEFAULT NULL COMMENT '描述',
	UNIQUE INDEX `Index 1` (`pname`)
);

CREATE TABLE `src_topic_info_0` (
	`src_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`src_topic_desc` VARCHAR(2048) NOT NULL COMMENT '原始主题描述',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`src_topic_id`)
);

CREATE TABLE `topic_attribute_info_0` (
	`src_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`attribute_key` CHAR(32) NOT NULL COMMENT '属性key : 含_all',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`src_topic_id`, `attribute_key`),
	UNIQUE INDEX `src_topic_id` (`src_topic_id`, `attribute_key`)
);

CREATE TABLE `topic_mapping_rel_0` (
	`src_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`attribute_key` CHAR(32) NOT NULL COMMENT '属性key : 含_all',
	`attribute_value` CHAR(32) NOT NULL COMMENT '属性value : 含_default',
	`dest_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`src_topic_id`, `attribute_key`, `attribute_value`, `dest_topic_id`)
);

CREATE TABLE `topic_publish_rel_0` (
	`client_id` VARCHAR(32) NOT NULL DEFAULT '',
	`src_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`client_pswd` CHAR(32) NULL DEFAULT NULL COMMENT '客户端密码 : 支持“_null”',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	PRIMARY KEY (`client_id`, `src_topic_id`),
	UNIQUE INDEX `client_id` (`client_id`, `src_topic_id`)
);


CREATE TABLE `white_list_0` (
	`ip` VARCHAR(15) NOT NULL COMMENT 'ip地址',
	`index_id` VARCHAR(60) NOT NULL COMMENT '索引id : 用于与white_list_index关联',
	`use_status` VARCHAR(1) NOT NULL DEFAULT '1' COMMENT '使用标志 : 0&1',
	PRIMARY KEY (`ip`, `use_status`)
);

CREATE TABLE `topic_subscribe_rel_0` (
	`client_id` VARCHAR(32) NOT NULL DEFAULT '',
	`dest_topic_id` VARCHAR(32) NOT NULL DEFAULT '',
	`client_pswd` CHAR(32) NULL DEFAULT NULL COMMENT '客户端密码 : 支持“_null”',
	`max_request` INT(3) NULL DEFAULT NULL COMMENT '最大并发数',
	`min_timeout` INT(8) NULL DEFAULT NULL COMMENT '最小超时时间',
	`max_timeout` INT(8) NULL DEFAULT NULL COMMENT '最大超时时间',
	`use_status` CHAR(1) NOT NULL COMMENT '使用标志 : 0&1',
	`login_no` CHAR(32) NULL DEFAULT NULL COMMENT '操作工号',
	`opr_time` DATETIME NULL DEFAULT NULL COMMENT '操作时间',
	`note` VARCHAR(2048) NULL DEFAULT NULL COMMENT '备注',
	`consume_speed_limit` int(8) DEFAULT 0,
	`max_messages` int(8) DEFAULT 10000,
	`warn_messages` int(8) DEFAULT 1000,
	PRIMARY KEY (`client_id`, `dest_topic_id`),
	UNIQUE INDEX `client_id` (`client_id`, `dest_topic_id`)
);

create table tenant_client_rel_9(tenant_id char(32) not null, client_id char(32) not null, use_status char(1) default '1');

for i in range(40):
    print '''
CREATE TABLE messagestore_%d (
  id varchar(128) NOT NULL,
  properties varchar(2048) DEFAULT NULL,
  systemProperties varchar(1024) DEFAULT NULL,
  content blob,
  createtime bigint(20),
  PRIMARY KEY (id)
);'''%i
for i in range(100):
    print '''
CREATE TABLE `msgidx_part_%d` (
  `idmm_msg_id` varchar(60) NOT NULL,
  `dst_cli_id` varchar(32) NOT NULL,
  `dst_topic_id` varchar(32) NOT NULL,
  `produce_cli_id` varchar(32) DEFAULT NULL,
  `src_topic_id` varchar(32) DEFAULT NULL,
  `src_commit_code` char(4) DEFAULT NULL,
  `group_id` varchar(32) DEFAULT NULL,
  `priority` int(11) NOT NULL DEFAULT '100',
  `idmm_resend` int(11) DEFAULT NULL,
  `consumer_resend` int(11) DEFAULT NULL,
  `create_time` bigint(20) DEFAULT NULL,
  `broker_id` varchar(21) DEFAULT NULL,
  `req_time` bigint(20) DEFAULT NULL,
  `commit_code` char(4) DEFAULT NULL,
  `commit_time` bigint(20) DEFAULT NULL,
  `commit_desc` varchar(160) DEFAULT NULL,
  `next_topic_id` varchar(32) DEFAULT NULL,
  `next_client_id` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`idmm_msg_id`,`dst_cli_id`,`dst_topic_id`),
  KEY `Index 1` (`dst_cli_id`,`dst_topic_id`)
);''' % i


-- 单个消息队列对应数据配置， 生产者-Pub000  源主题-TSrc1 目标主题-TDst1 消费者- Sub000
INSERT INTO `topic_subscribe_rel_0` VALUES ('Sub000', 'TDst1', '_null', '20', '60', '600', '1', 'admin', now(), null, 0, 10000, 1000);
INSERT INTO `ble_dest_topic_rel_0` VALUES ('TDst1', '50000001', '1', 'admin', now(), null);
INSERT INTO `topic_mapping_rel_0` VALUES ('TSrc1', '_all', '_default', 'TDst1', '1', 'admin', now(), null);
INSERT INTO `topic_publish_rel_0` VALUES ('Pub000', 'TSrc1', '_null', '1', 'admin', now(), null);
INSERT INTO `client_base_info_0` VALUES ('Pub000', '订单处理', '订单处理', '1', 'admin', now(), null);
INSERT INTO `client_base_info_0` VALUES ('Sub000', '统一接触操作类', '统一接触', '1', 'admin', now(), null);
INSERT INTO `src_topic_info_0` VALUES ('TSrc1', '操作类接触信息工单', '1', 'admin', now(), null);
INSERT INTO `dest_topic_info_0` VALUES ('TDst1', '操作类接触信息工单', '1', 'admin', now(), null);
INSERT INTO `ble_base_info_0` VALUES (50000001, 0, '0.0.0.0', 3301, '1', 'admin', now(), null);

insert into tenant_client_rel_9 values('gyf', 'Pub2', '1');
insert into tenant_client_rel_9 values('gyf', 'Sub2', '1');
