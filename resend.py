from idmm import DMMClient
if __name__ == '__main__':
	c = DMMClient('10.113.181.91:9124')
	for line in open("b.txt"):
		v = line.strip().split()
		msgid,pubid,pubtopic,groupid = v[0],v[1],v[2],v[3]
		c.send_commit(pubtopic,pubid,msgid)

# coding=utf-8

'''
功能：根据设定的<主题+起始时间>，自动批量重发错误消息脚本
'''

import urllib
from time import strftime, localtime
import time
import json
import sys, os
import random
import string
import MySQLdb
import ConfigParser
from kazoo import client

# 发送前需修改起始时间
begin_t = '2018-10-12 00:00:00'
dest_topic_id = 'TSOSEND'

cfile = "/idmm/idmm2-manager/config/Config.cfg"


def readStrValue(configFile, section, key):
	cf = ConfigParser.ConfigParser()
	cf.read(configFile)
	return str(cf.get(section, key))


def getBleList(bleid):
	addr = ''

	try:
		zkUrl = readStrValue(cfile, 'zk', 'url')
		zkPath = readStrValue(cfile, 'zk', 'blePath')
		zk = client.KazooClient(hosts='%s' % zkUrl)
		zk.start()
		zk_list = zk.get_children('%s' % zkPath)
		if len(zk_list) > 0:
			blePath = zkPath + '/id.' + bleid
			data, stat = zk.get('%s' % blePath)
			ip = data.split(" ")[0].split(":")[0]
			port = data.split(" ")[1].split(":")[1]
			addr = "%s:%s" % (ip, port)

		zk.stop()
		return addr
	except Exception, e:
		print 'getBleList Error: %s' % (e)


def start():
	dd = strftime("%Y%m%d", localtime())
	fname = 'err_bak_%s_%s.txt' % (dest_topic_id, dd)
	fn = open(fname, 'a')

	start_t = strftime("%Y-%m-%d %H:%M:%S", localtime())
	# 重发起始时间
	t = 1000 * time.mktime(time.strptime(begin_t, '%Y-%m-%d %H:%M:%S'))

	try:
		conn = MySQLdb.connect(host='10.243.7.89', user='inform', passwd='informdb!@#2016', db='informdb',
							   charset='utf8', port=8066)
		cur = conn.cursor()
		cur1 = conn.cursor()

		sql = "select ble_id from ble_dest_topic_rel_8 where dest_topic_id='%s' " % dest_topic_id
		cur.execute(sql)
		ble_id = cur.fetchone()[0]
		print 'ble_id:%s' % ble_id

		# 查询zk上该bleid对应的属主ip
		ble_addr = getBleList(str(ble_id))
		print 'ble_addr:%s' % ble_addr
		if ble_addr == None or ble_addr == '':
			print 'ble_addr is null,please check it!!'
			return

		# 查询该bleid下的所有主题，依次进行重发
		while True:
			print 'dest_topic_id:%s' % dest_topic_id
			sql = "select idmm_msg_id,dst_cli_id from msgidx_part_err where commit_time>=%ld and dst_topic_id ='%s' limit 100" % (
			t, dest_topic_id)
			num = cur1.execute(sql)
			if num == 0:
				print 'no more message'
				sys.exit()
			for errmsg in cur1.fetchall():
				print errmsg[0], errmsg[1]
				msgid = errmsg[0].rstrip()
				dst_cli_id = errmsg[1].rstrip()
				url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm2.ble.RunTime:name=runTime/send/%s/%s/%s/%d/10' % (
				ble_addr, msgid, dst_cli_id, dest_topic_id, random.randint(1, 1000))
				print 'url=%s' % url
				url_rtn = urllib.urlopen(url)
				if url_rtn.getcode() != 200:
					print 'resend error!'
					return
				else:
					print 'resend %s succ!' % msgid
					# 重发成功，先记入备份文件，再删除err表里记录
					fn.write(dest_topic_id + ',' + dst_cli_id + ',' + msgid + '\n')
					dsql = "delete from msgidx_part_err where idmm_msg_id='%s'" % (msgid)
					cur1.execute(dsql)
			conn.commit()
			cur1.close()
			cur1 = conn.cursor()
			time.sleep(0.2)
		fn.close()
		conn.commit()
		cur.close()
		cur1.close()
		conn.close()
	except MySQLdb.Error, e:
		print 'MySQLdb Error, %s' % e

	end_t = strftime("%Y-%m-%d %H:%M:%S", localtime())
	print 'begin time:%s' % start_t
	print '  end time:%s' % end_t


if __name__ == '__main__':
	start()