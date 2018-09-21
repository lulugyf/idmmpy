#coding=utf-8


header = "生产者ID	生产者归属系统	生产者负责人	生产者主题名	订阅者归属系统	订阅者负责人	订阅者ID	订阅者主题名	备注	消息涉及主要业务	是否影响用户感知	影响内容	消息涉及主要业务	是否影响用户感知	影响内容".split("\t")
topics_conf = """
Pub113	服务开通	wangxg	T113Smsp-A	订单处理	xuag	Sub101Smsp	T113SmspDest-A	长流程报竣	G网长流程业务	是	影响G网长流程业务订单的正常归档计费	订处-13	否	影响订单归档和在途订单	
Pub103	服务请求	xuag	TBatchOrder-A	订单处理	xuag	Sub101Batch	TBatchOrderDest-A								
Pub103	服务请求	xuag	TBatchOrderBack-A	订单处理	xuag	Sub101OrderBack	TBatchOrderBackDest-A								
Pub101	订单处理	xuag	T101DataSyn-A	营销管理	zhoucg	Sub115	T101DataSynDest-A								
Pub101	订单处理	xuag	T101OrderDataSyn-A	服务请求	xuag	Sub103OrderDataSyn	T101OrderDataSynDest-A		订处-16	是	影响客户费用	订处-16	是	影响客户费用	
Pub101	订单处理	xuag	T101BusiOrder-A	账务管理	wenjie	Sub109BusiOdr	T101BusiOrderDest-A		未启用-xuag			未启用-wenjie			
Pub101	订单处理	xuag	T101Smsp-A	服务开通	wangxg	Sub113Order	T101SmspDest-A	CRM订单接收	订处-13	是	影响后续的指令发送	G网及宽带等业务开通	是	影响客户业务的正常开通	
Pub101	订单处理	xuag	T101RptOrder-A	台帐报表	xuag	Sub111RptOrder	T101RptOrderDest-A		订单创建	是	订单创建超时，jdbc池获取不到链接				
Pub101	订单处理	xuag	T101RptOrderLine-A	台帐报表	xuag	Sub111RptOrderLine	T101RptOrderLineDest-A		订处-10	否	影响订单处理速度和在途订单				
Pub101	订单处理	xuag	TRecOprCntt-A	服务请求	xuag	Sub103Opr	TRecOprCnttDest-A	(已删除-20180620)							
Pub101	订单处理	xuag	TRecOprCntt-A	统一接触系统	xuag	Sub119	TRecOprCntt-A		订单创建	是	订单创建超时，jdbc池获取不到链接				
Pub101	订单处理	xuag	TOrderBatch-A	服务请求	xuag	Sub103Batch	TOrderBatchDest-A								
Pub101	订单处理	xuag	T101Confirm-A	订单处理	xuag	Sub101Conf	T101ConfirmDest-A		未启用-xuag						
Pub101	订单处理	xuag	T101Sreq-A	服务请求	xuag	Sub103Sreq	T101SreqDest-A		订处-13	是	影响后续的指令发送	订处-13	是	影响后续的指令发送	
Pub101	订单处理	xuag	T101Rptb2cOrder-A	台帐报表	xuag	Sub111Rptb2cOrder	T101Rptb2cOrderDest-A		未启用-xuag						
Pub131	计费	wangjxa	TSmsMiddle-A	信息通知平台	chenmy	Sub129Middle	TSmsMiddleDest-A		未启用-wenjie						
Pub130	计费	wangjxa	TSmsHigh-A	信息通知平台	chenmy	Sub129High	TSmsHighDest-A		未启用-wenjie						
Pub109	账务管理	huaqi	T109BusiOrder-A	服务请求	zhangxina	Sub103BusiOdr	T109BusiOrderDest-A	业务工单	未启用-wenjie						
Pub109	账务管理	huaqi	T109Smsp-A	服务开通	lirh	Sub113Credit	T109SmspDest-A	批量信控停开机	未启用-wenjie						
Pub109	账务管理	huaqi	TSmsHigh-A	信息通知平台	chenmy	Sub129High	TSmsHighDest-A	短信-高优先级	未启用-wenjie						
Pub109	账务管理	huaqi	TSmsMiddle-A	信息通知平台	chenmy	Sub129Middle	TSmsMiddleDest-A	短信-中优先级	未启用-wenjie						
Pub109	账务管理	huaqi	TSmsLow-A	信息通知平台	chenmy	Sub129Low	TSmsLowDest-A	短信-底优先级	未启用-wenjie						
Pub109	账务管理	huaqi	Tsmsgroup-A	信息通知平台	chenmy	Sub129group	TSmsgroupDest-A	短信-群发	未启用-wenjie						
Pub109	账务管理	huaqi	T109Rpt-A	台帐报表	zhaoxl_bj	Sub111RptBoss	T109RptDest-A	缴费报表	未启用-wenjie						
Pub109	账务管理	huaqi	TRecQryCntt-A	台帐报表	zhaoxl_bj	Sub111Cntt	TRecQryCnttDest-A	操作日志	未启用-wenjie						
Pub109	账务管理	huaqi	TRecQryCntt-A	统一接触系统	chenzc	Sub119	TRecQryCnttDest-A	操作日志	未启用-wenjie						
Pub109	账务管理	huaqi	TRecOprCntt-A	服务请求	zhangxina	Sub103Opr	TRecOprCnttDest-A	(已删除-20180620)	未启用-wenjie						
Pub109	账务管理	huaqi	TRecOprCntt-A	统一接触系统	chenzc	Sub119Opr	TRecOprCnttDest-A	操作日志	未启用-wenjie						
Pub109	账务管理	huaqi	T109Market-A	营销管理	weiqiang	Sub115Zw	T109MarketDest-A	营销数据	未启用-wenjie						
Pub109	账务管理	huaqi	T109Order-A	账务管理	huaqi	Sub109Busi	T109OrderDest-A	帐务管理内部业务工单?	未启用-wenjie						
Pub109	账务管理	huaqi	T109OrderBatch-A	账务管理	huaqi	Sub109Busi	T109OrderDest-A	帐务管理内部业务工单?	未启用-wenjie						
Pub109	账务管理	huaqi	T109DataRpt-A	账务管理	huaqi	Sub109DataRpt	T109DataRptDest-A	积分数据同步	未启用-wenjie						
Pub109	账务管理	wangxin	T109ElecInvcReq-A	订单管理	liujj	Sub101ElecInvcReq	T109ElecInvcReqDest-A	电子发票信息回传	未启用-wenjie						
Pub109	账务管理	wenjie	T109SmspGW-A	服务开通	wangxg	Sub113Credit	T109SmspGWDest-A	PBOSS跟账管侧关于固网业务	宽带局拆业务	是	影响宽带局拆业务	信控停开机和宽带局拆业务	是	影响客户开机	
Pub109	账务管理	qiaolin	TFundBind-A	渠道管理平台资金归集	songjia	Sub117FundBind	TFundBindDest-A	代理商资金管理接口	未启用-wenjie						
Pub113			TSmsHigh-A			Sub129High	TSmsHighDest-A								
Pub113			T113Smsp-A			Sub101Smsp	T113SmspDest-A								
Pub109	账务管理	wenjie	T109Smsp-A	服务开通	wangxg	Sub113Credit	T109SmspDest-A		信控停开机和局拆业务	是	影响客户开关机	信控停开机和局拆业务	是	影响客户开关机	
Pub107			TSynLoginNo-A			Sub113SynLoginNo	TSynLoginNoDest-A								
Pub101			T101Smsp-A			Sub113Order	T101SmspDest-A								
Pub117			TSmsMiddle-A			Sub129Middle	TSmsMiddleDest-A								
PubPayment	支付中心	tangpeng	TrechargeOrder-A	支付中心	tangpeng	SubPayment	TrechargeOrder-A	充值订单入库         	充值订单入库	否		充值订单入库	否		
PubPayment	支付中心	tangpeng	TrechargeOrderItem-A	支付中心	tangpeng	SubPayment	TrechargeOrderItem-A	充值订单明细入库     	充值订单明细入库	否		充值订单明细入库	否		
PubPayment	支付中心	tangpeng	TrechargeOrderNotify-A	支付中心	tangpeng	SubPayment	TrechargeOrderNotify-A	充值订单通知数据入库 	充值订单通知数据入库	否		充值订单通知数据入库	否		
PubPayment	支付中心	tangpeng	TrechargeBusiness-A	支付中心	tangpeng	SubPayment	TrechargeBusiness-A	异步处理充值业务     	异步处理充值业务	是	充值不能到账	异步处理充值业务	是	充值不能到账	
PubPayment	支付中心	tangpeng	TrechargeRoDoBusiness-A	支付中心	tangpeng	SubPayment	TrechargeRoDoBusiness-A	异步处理充值重试业务 	异步处理充值重试业务	是	充值不能到账	异步处理充值重试业务	是	充值不能到账	
PubPayment	支付中心	tangpeng	TrechargeResultNotify-A	支付中心	tangpeng	SubPayment	TrechargeResultNotify-A	充值结果通知         	充值结果通知	是	影响用户充值订单状态	充值结果通知	是	影响用户充值订单状态	
PubPayment	支付中心	tangpeng	TrechargeResultRedoNotify-A	支付中心	tangpeng	SubPayment	TrechargeResultRedoNotify-A	充值结果重试通知     	充值结果重试通知	是	影响用户充值订单状态	充值结果重试通知	是	影响用户充值订单状态	
PubPayment	支付中心	tangpeng	TrechargeBusiBill-A	支付中心	tangpeng	SubPayment	TrechargeBusiBill-A	充值业务数据入库     	充值业务数据入库	否		充值业务数据入库	否		
PubPayment	支付中心	tangpeng	TpaymentPayUser-A	支付中心	tangpeng	SubPayment	TpaymentPayUser-A	用户信息入库        	用户信息入库	否		用户信息入库	否		
PubPayment	支付中心	tangpeng	TpaymentRefund-A	支付中心	tangpeng	SubPayment	TpaymentRefund-A	支付退款单信息入库    	支付退款单信息入库	否		支付退款单信息入库	否		
PubPayment	支付中心	tangpeng	TpaymentRefundItem-A	支付中心	tangpeng	SubPayment	TpaymentRefundItem-A	支付退款单明细入库        	支付退款单明细入库	否		支付退款单明细入库	否		
PubPayment	支付中心	tangpeng	TpaymentOrder-A	支付中心	tangpeng	SubPayment	TpaymentOrder-A	支付结果通知业务     	支付订单入库	否		支付订单入库	否		
PubPayment	支付中心	tangpeng	TpaymentOrderItem-A	支付中心	tangpeng	SubPayment	TpaymentOrderItem-A	 支付结果重试通知业务	支付订单明细入库	否		支付订单明细入库	否		
PubPayment	支付中心	tangpeng	TpaymentOrderNotify-A	支付中心	tangpeng	SubPayment	TpaymentOrderNotify-A	支付通知入库	支付通知入库	否		支付通知入库	否		
PubPayment	支付中心	tangpeng	TpaymentResultNotify-A	支付中心	tangpeng	SubPayment	TpaymentResultNotify-A	支付结果通知业务	支付结果通知业务	是	影响用户支付订单状态	支付结果通知业务	是	影响用户支付订单状态	
PubPayment	支付中心	tangpeng	TpaymentResultRedoNotify-A	支付中心	tangpeng	SubPayment	TpaymentResultRedoNotify-A	支付结果重试通知业务	支付结果重试通知业务	是	影响用户支付订单状态	支付结果重试通知业务	是	影响用户支付订单状态	
Pub103	服务请求	xuag	T103DataSynCRMA-A	服务请求	xuag	Sub103DataSyn	T103DataSynCRMADest-A	extra数据同步到CRM库，自产自销         	订处-16	是	影响客户费用	订处-16	是	影响客户费用	
Pub103	服务请求	xuag	T103DataSynCRMB-A	服务请求	xuag	Sub103DataSyn	T103DataSynCRMBDest-A	extra数据同步到CRM库，自产自销         	订处-16	是	影响客户费用	订处-16	是	影响客户费用	
Pub103	服务请求	xuag	T103DataSynCRMC-A	服务请求	xuag	Sub103DataSyn	T103DataSynCRMCDest-A	extra数据同步到CRM库，自产自销         	订处-16	是	影响客户费用	订处-16	是	影响客户费用	
Pub103	服务请求	xuag	T103DataSynBOSSA-A	账务管理	xuag	Sub109DataSyn	T103DataSynBOSSADest-A	extra数据同步到BOSS库         	订处-16	是	影响客户费用	crm库与boss库间数据工单同步	是	用户费用错误，业务办理失败	
Pub103	服务请求	xuag	T103DataSynBOSSB-A	账务管理	xuag	Sub109DataSyn	T103DataSynBOSSBDest-A	extra数据同步到BOSS库         	订处-16	是	影响客户费用	crm库与boss库间数据工单同步	是	用户费用错误，业务办理失败	
Pub103	服务请求	xuag	T103DataSynBOSSC-A	账务管理	xuag	Sub109DataSyn	T103DataSynBOSSCDest-A	extra数据同步到BOSS库         	订处-16	是	影响客户费用	crm库与boss库间数据工单同步	是	用户费用错误，业务办理失败	
Pub103	服务请求	xuag	T103DataSynCEN-A	基础域	xuag	Sub107DataSyn	T103DataSynCENDest-A	extra数据同步到中心库         	订处-16	是	影响客户费用	订处-16	是	影响客户费用	
Pub103	服务请求	xuag	T103DataSynREPORT-A	台账报表	xuag	Sub111DataSyn	T103DataSynREPORTDest-A	extra数据同步到报表库         	订处-16	是	影响客户费用	订处-16	是	影响客户费用	
Pub103	服务请求	xuag	T103DataSynRES-A	资源管理	xuag	Sub105DataSyn	T103DataSynRESDest-A	extra数据同步到资源库         	订处-16	否	影响批量订单的处理效率	订处-16	否	影响批量订单的处理效率	
Pub101	服务请求	xuag	T101OrderCapse-A	服务请求	xuag	Sub103OrderCapse	T101OrderCapseDest-A	Capse指标	订处-19	否	影响订单的归档效率和在途订单	订处-19	否	影响订单的归档效率和在途订单	
Pub101	订单处理	xuag	T101SmsSend-A	服务请求	xuag	Sub103SmsSend	T101SmsSendDest-A	订单中心短信发送	订单监控	否	订单中心短信发送(目前是监控再用)orderApp->Extra	订单监控	否	订单中心短信发送(目前是监控再用)orderApp->Extra	
Pub101	订单处理	xuag	T101BillPrint2HBase-A	服务请求	xuag	Sub103BillPrint2HBase	T101BillPrint2HBaseDest-A	票据归档写HBase	票据打印	否	票据归档写Hbase-电子发票、合打、分打	票据打印	否	票据归档写Hbase-电子发票、合打、分打	
Pub101	订单处理	xuag	T101UniOrd2HBase-A	服务请求	xuag	Sub103UniOrd2HBase	T101UniOrd2HBaseDest-A	统一订单归档写HBase	统一订单	否	统一订单归档写Hbase（二阶段未启用）	统一订单	否	统一订单归档写Hbase（二阶段未启用）	
Pub101	订单处理	xuag	T101Cart2HBase-A	服务请求	xuag	Sub103Cart2HBase	T101Cart2HBaseDest-A	购物车归档写HBase	购物车	否	影响不大	购物车	否	影响不大	
Pub101	订单处理	xuag	T101Order2HBase-A	服务请求	xuag	Sub103Order2HBase	T101Order2HBaseDest-A	订单归档写HBase	订处-19	否	影响不大	订处-19	否	影响不大	
Pub103	服务请求	xuag	T103BillPrint2HBase-A	订单处理	xuag	Sub101BillPrint2HBase	T103BillPrint2HBaseDest-A	票据归档写HBase（extra通知orderApp删内库数据）	票据打印	否	orderApp通知orderApp删内库数据--票据	票据打印	否	orderApp通知orderApp删内库数据--票据	
Pub103	服务请求	xuag	T103UniOrd2HBase-A	订单处理	xuag	Sub101UniOrd2HBase	T103UniOrd2HBaseDest-A	统一订单归档写HBase（extra通知orderApp删内库数据）	统一订单	否	删内库统一订单数据（二阶段未启用）	统一订单	否	删内库统一订单数据（二阶段未启用）	
Pub103	服务请求	xuag	T103Cart2HBase-A	订单处理	xuag	Sub101Cart2HBase	T103Cart2HBaseDest-A	购物车归档写HBase（extra通知orderApp删内库数据）	购物车	否	影响不大	购物车	否	影响不大	
Pub103	服务请求	xuag	T103Order2HBase-A	订单处理	xuag	Sub101Order2HBase	T103Order2HBaseDest-A	订单归档写Hbase（extra通知orderApp删内库数据）	订处-19	否	影响不大	订处-19	否	影响不大	
Pub103	服务请求	xuag	T103DataSynBatchCRMA-A	账务管理	xuag	Sub103DataSyn	T103DataSynBatchCRMADest-A	extra数据同步到BOSS库-批量通道	订处-16	否	影响批量订单的处理效率	订处-16	否	影响批量订单的处理效率	
Pub103	服务请求	xuag	T103DataSynBatchCRMB-A	账务管理	xuag	Sub103DataSyn	T103DataSynBatchCRMBDest-A	extra数据同步到BOSS库-批量通道	订处-16	否	影响批量订单的处理效率	订处-16	否	影响批量订单的处理效率	
Pub103	服务请求	xuag	T103DataSynBatchCRMC-A	账务管理	xuag	Sub103DataSyn	T103DataSynBatchCRMCDest-A	extra数据同步到BOSS库-批量通道	订处-16	否	影响批量订单的处理效率	订处-16	否	影响批量订单的处理效率	
Pub103	服务请求	xuag	T103DataSynBatchBOSSA-A	服务请求	xuag	Sub109DataSyn	T103DataSynBatchBOSSADest-A	extra数据同步到CRM库-批量通道	订处-16	否	影响批量订单的处理效率	crm库与boss库间数据工单同步批量通道	是	用户费用错误，业务办理失败	
Pub103	服务请求	xuag	T103DataSynBatchBOSSB-A	服务请求	xuag	Sub109DataSyn	T103DataSynBatchBOSSBDest-A	extra数据同步到CRM库-批量通道	订处-16	否	影响批量订单的处理效率	crm库与boss库间数据工单同步批量通道	是	用户费用错误，业务办理失败	
Pub103	服务请求	xuag	T103DataSynBatchBOSSC-A	服务请求	xuag	Sub109DataSyn	T103DataSynBatchBOSSCDest-A	extra数据同步到CRM库-批量通道	订处-16	否	影响批量订单的处理效率	crm库与boss库间数据工单同步批量通道	是	用户费用错误，业务办理失败	
Pub103	服务请求	xuag	T103DataSynBatchCEN-A	基础域	xuag	Sub107DataSyn	T103DataSynBatchCENDest-A	extra数据同步到中心库-批量通道	订处-16	否	影响批量订单的处理效率	订处-16	否	影响批量订单的处理效率	
Pub107	基础域	xuag	T107DataSyn-A	服务请求	xuag	Sub103DataSyn	T107DataSynDest-A	基础域数据同步->extra	未启用-xuag						
Pub102	订单受理	xuag	T102DataSynDirect-A	服务请求	xuag	Sub103DataSyn	T102DataSynDirectDest-A	订单受理不走订单的数据同步->extra				绿色-数同	是	影响客户费用	
Pub104	产品管理	xuag	T104DataSynDirect-A	服务请求	xuag	Sub103DataSyn	T104DataSynDirectDest-A	产品管理不走订单的数据同步->extra				绿色-数同	是	影响客户费用	
Pub119	客户交互中心	lixao	TRecEndCntt-A	客户交互中心	lixao	Sub119Opr	TEndCnttDest-A	结束接触记录消息	结束接触记录	是	影响客户首页	结束接触记录	是	影响客户首页	
Pub119	客户交互中心	lixao	TRecBeginCntt-A	客户交互中心	lixao	Sub119Opr	TBeginCnttDest-A	开始接触记录消息	开始接触记录	是	影响打开客户首页	开始接触记录	是	影响打开客户首页	
Pub119	客户交互中心	lixao	TRecOnceCntt-A	客户交互中心	lixao	Sub119Opr	TOnceCnttDest-A	一次性接触记录消息	一次性接触记录	是	影响客户首页	一次性接触记录	是	影响客户首页	
Pub104	产品管理	yangzc	T104DataSynBasemng-A	基础域	lixiao	Sub107Smsp	T104DataSynBasemngDest-A	产品管理->基础域数据同步							
Pub104	产品管理	yangzc	TRecQryCntt-A	服务请求	lixiao	Sub119Opr	TRecQryCnttDest-A	查询接触记录消息							
Pub104	产品管理	yangzc	T104SpmsDirect-A	服务请求	xuag	Sub103Sreq	T104SpmsDirectDest-A	产品管理不走订单的服务开通预处理->extra				绿色-服开	是	影响指令	
Pub104	产商品中心	yangzc	T104DataSyn-A	服务开通	xuag	Sub113DataSyn	T104DataSynDest-A	黑龙江移动SP服务同步							
Pub103	服务请求	fengxb	T103SpmsBatch-A	服务请求	zhaowr	Sub113Order	T103SpmsBatchDest-A	服务请求(extra)->服务开通（批量业务）	订处-13	否	影响批量订单的处理效率	批量业务通道	是	影响走批量开通通道业务的正常开通	
Pub106	客户中心	lixiao	TRecOprCntt-A	客户交付中心	lixiao	Sub119Opr	TRecOprCnttDest-A	受理接触记录消息	记录操作轨迹表	否		记录操作轨迹表	否		
Pub106	客户中心	lixiao	TRecQryCntt-A	客户交付中心	lixiao	Sub119Opr	TRecQryCnttDest-A	查询接触记录消息	查询类，操作记录表	否		查询类，操作记录表	否		
Pub107	基础中心	lixiao	TRecQryCntt-A	客户交付中心	lixiao	Sub119Opr	TRecQryCnttDest-A	查询接触记录消息				未启用-jianglh			
Pub107	基础中心	lixiao	TRecOprCntt-A	客户交付中心	lixiao	Sub119Opr	TRecOprCnttDest-A	受理接触记录消息	记录操作轨迹表	否		记录操作轨迹表	否		
Pub109	账务管理	lixiao	TRecQryCntt-A	客户交付中心	lixiao	Sub119Opr	TRecQryCnttDest-A	查询接触记录消息	未启用-wenjie			查询接触	否		
Pub103	服务请求	lixiao	TRecQryCntt-A	客户交付中心	lixiao	Sub119Opr	TRecQryCnttDest-A	查询接触记录消息				查询接触	否		
Pub103	服务请求	lixiao	TRecOprCntt-A	客户交付中心	lixiao	Sub119Opr	TRecOprCnttDest-A	受理接触记录消息				受理类接触信息记录	是	影响冲正、报表等	
Pub101	订单处理 	lixiao	TRecOprCntt-A	客户交付中心	lixiao	Sub119Opr	TRecOprCnttDest-A	受理接触记录消息				受理类接触信息记录	是	影响冲正、报表等	
Pub125	积分管理	lixiao	TRecQryCntt-A	客户交付中心	lixiao	Sub119Opr	TRecQryCnttDest-A	查询接触记录消息				查询接触	否		
Pub125	积分管理	lixiao	TRecOprCntt-A	客户交付中心	lixiao	Sub119Opr	TRecOprCnttDest-A	受理接触记录消息				受理类接触信息记录	是	影响冲正、报表等	
Pub101	订单处理	jiaoaj	T101Order2Prm-A	渠道管理	maoping	Sub117Prm	T101Order2PrmDest-A	订单中心同步订单数据到PRM	订处-19	否	影响订单的归档效率和在途订单				
Pub101	订单处理	jiaoaj	T101CashExcp2Prm-A	渠道管理	maoping	Sub117Prm	T101CashExcp2PrmDest-A	订单中心同步营业厅资金管理异常数据到PRM	订单监控	否	影响不大，订单中心同步营业厅资金管理异常数据到PRM				
Pub113	服务开通	zhaowr	T113SpmsBroadband-A	服务请求	fengxb	Sub103Spms	T113SpmsBroadbandDest-A	宽带报竣反馈给extra	宽带业务	是	影响宽带用户的业务订单的正常归档计费	订处-13	否	宽带报竣反馈给extra	
Pub101	订单中心	xuag	T101BusiPacket-A	产商品中心	yangzc	Sub104	T101BusiPacketDest-A	订单中心通知产商品中心删除业务包数据	购物车	否	订单中心通知产商品中心删除业务包数据				
Pub101	订单中心	xuag	T101SMS-A	服务请求	fengxb	Sub103SMS	T101SMSDest-A	订单中心发送短信给extra，extra调用服务发短信	订单监控	否	订单中心发送短信给extra，extra调用服务发短信	订单监控	否	订单中心发送短信给extra，extra调用服务发短信	
Pub105	资源管理	liuzd	T105DataBatchSyn-A	服务开通	wangxg	Sub113DataBatchSyn	T105DataBatchSynDest-A	批量开指令				批量开卡	否	影响零售库存中心的批量开卡	
Pub101	订单中心	xuag	T101OrderStateSyn-A	服务请求	fengxb	Sub103	T101OrderStateSynDest-A	订单中心同步订单状态给extra，extra写业务侧订单同步表	订处-1391	否	影响订单的处理效率和在途订单	订处-1391	否	影响订单的处理效率和在途订单	
Pub101	订单中心	liuzd	T101DataBatchSyn-A	服务开通	wangxg	Sub113DataBatchSyn	T105DataBatchSynDest-A	批量开指令				集团销户业务	否	影响集团销户业务的正常处理	
Pub103	服务请求	yangzc	T103BatchOrder	订单处理	xuag	Sub101Batch	T103BatchOrderDest	服务请求->订单中心（批量订单）				批量订单	否	服务请求->订单中心（批量订单）	
Pub101	订单处理	xuag	TBatchOrderBack	产商品中心	yangzc	Sub103Batch	TBatchOrderBackDest	订单中心->服务请求（批量订单反馈）	批量订单	否	订单中心->服务请求（批量订单反馈）	批量订单	否	订单中心->服务请求（批量订单反馈）	
Pub109	账务管理	wenjie	T109BusiOrderOffOnA	产商品中心	liff	Sub104	T109BusiOrderOffOnADest	OffOn业务工单同步BOSS-CRM	用户状态变更同步到crm库	是	crm库和boss库资料不一致				
Pub109	账务管理	wenjie	T109BusiOrderOffOnB	产商品中心	liff	Sub104	T109BusiOrderOffOnBDest	OffOn业务工单同步BOSS-CRM	用户状态变更同步到crm库	是	crm库和boss库资料不一致				
Pub109	账务管理	wenjie	T109BusiOrderOffOnC	产商品中心	liff	Sub104	T109BusiOrderOffOnCDest	OffOn业务工单同步BOSS-CRM	用户状态变更同步到crm库	是	crm库和boss库资料不一致				
Pub109	账务管理	wenjie	T109BusiOrderDeadA	产商品中心	liff	Sub104	T109BusiOrderDeadADest	Dead业务工单同步BOSS-CRM	欠费销户/局拆同步到crm库	是	crm库和boss库资料不一致				
Pub109	账务管理	wenjie	T109BusiOrderDeadB	产商品中心	liff	Sub104	T109BusiOrderDeadBDest	Dead业务工单同步BOSS-CRM	欠费销户/局拆同步到crm库	是	crm库和boss库资料不一致				
Pub109	账务管理	wenjie	T109BusiOrderDeadC	产商品中心	liff	Sub104	T109BusiOrderDeadCDest	Dead业务工单同步BOSS-CRM	欠费销户/局拆同步到crm库	是	crm库和boss库资料不一致				
Pub109	账务管理	wenjie	T109BusiOrderA	产商品中心	liff	Sub104	T109BusiOrderADest	业务工单同步BOSS-CRM	boss库到crm库的业务工单同步	是	业务办理失败				
Pub109	账务管理	wenjie	T109BusiOrderB	产商品中心	liff	Sub104	T109BusiOrderBDest	业务工单同步BOSS-CRM	boss库到crm库的业务工单同步	是	业务办理失败				
Pub109	账务管理	wenjie	T109BusiOrderC	产商品中心	liff	Sub104	T109BusiOrderCDest	业务工单同步BOSS-CRM	boss库到crm库的业务工单同步	是	业务办理失败				
Pub104	产商品中心	liff	T104BusiOrderA	账务管理	wenjie	Sub109Busi	T104BusiOrderADest	业务工单同步CRM-BOSS				crm到boss库的业务工单同步	是	业务办理失败	
Pub104	产商品中心	liff	T104BusiOrderB	账务管理	wenjie	Sub109Busi	T104BusiOrderBDest	业务工单同步CRM-BOSS				crm到boss库的业务工单同步	是	业务办理失败	
Pub104	产商品中心	liff	T104BusiOrderC	账务管理	wenjie	Sub109Busi	T104BusiOrderCDest	业务工单同步CRM-BOSS				crm到boss库的业务工单同步	是	业务办理失败	
Pub104	产商品中心	yangzc	T104DataBatchSyn	服务开通	wangxg	Sub113DataBatchSyn	T105DataBatchSynDest	产商品批开指令				产商品发起的批开业务	是	影响批开业务的正常开通处理	
"""
