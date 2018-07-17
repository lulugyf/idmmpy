#!/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import sys
import os
import time

# 消息中间件BLE队列监控

class qinfo:
    def __init__(self, jobj, bleid, addr, jmxaddr=None):
        self.topic = jobj['target_topic_id']
        self.client = jobj['target_client_id']
        self.total = jobj['total']
        self.size = jobj['size']
        self.sending = jobj['sending']
        self.err = jobj['err']
        self.bleid = bleid
        self.addr = addr
        self.jmxaddr = jmxaddr

def listQ(zkaddr):
    addrfile = getpath('.ble.list')
    getaddrs(zkaddr)

    q = []
    for line in file(addrfile):
        d = line.strip().split()
        if len(d) < 3:
            continue
        bleid, jmxaddr, dataaddr = d
        url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/info' % jmxaddr
        s = urllib2.urlopen(url)
        o = json.load(s)
        o1 = json.loads(o['value'])
        for o in o1:
            q.append(qinfo(o, bleid, dataaddr, jmxaddr))
    return q

# 获取节点信息， 从zk中同步获取
def getnodeinfo(zkaddr):
    info = {}
    import zk
    z = zk.ZKCli(zkaddr)
    z.start()
    ble = []
    base = '/idmm/ble'
    for p in z.list(base):
        data = z.get(base + '/' + p)
        data1 = data[0]
        nodeinfo = data[1]
        create_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(nodeinfo.ctime/1000))
        bleid = p[p.find('.') + 1:]
        jmxaddr = data1[0:data1.find(':')] + data1[data1.rfind(':'):]
        dataaddr = data1.split()[0]
        ble.append('%s %s %s,%s\n' % (bleid, jmxaddr, dataaddr, create_time))
    info['ble'] = ble

    httpbroker = []
    for p in z.list('/idmm/httpbroker'):
        httpbroker.append(p)
    info['httpbroker'] = httpbroker

    broker = []
    base = "/idmm/broker"
    for p in z.list(base):
        d, i = z.get(base + "/" + p)
        create_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(i.ctime/1000))
        broker.append("%s,%s--%s"%(p, create_time,d))
    info['broker'] = broker

    z.close()
    return info

def getinfo(bleid, jmxaddr, m, stat):
    url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/info'%jmxaddr
    s = urllib2.urlopen(url)
    o = json.load(s)
    o1 = json.loads(o['value'])
    print '====(%s)'%jmxaddr, bleid
    last_topic, last_client = "", ""
    for o in o1:
        s = "%s\t\t%s\t\t%d\t%d\t%d\t%d"%(
            o['target_topic_id'], o['target_client_id'], o['total'], o['size'], o['sending'], o['err'])
        if o['size'] > 0:
            m.append(bleid + '\t' + s)
        stat[0] += o['total']
        stat[1] += o['size']
        stat[2] += o['sending']
        last_topic, last_client = o['target_topic_id'], o['target_client_id']
        print s

    # 获取dboper 的积压
    url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/lockdetail/%s/%s'%(
        jmxaddr, last_client, last_topic)
    s = urllib2.urlopen(url)
    o = json.load(s)
    o1 = json.loads(o['value'])
    dboper_block = o1['global']['blocking_db_oper']
    print '    >>DBOper_Blocking %s'%bleid, dboper_block
    #print json.dumps(o1, indent=4)

def getaddrs(zkaddr):
    import zk
    z = zk.ZKCli(zkaddr)
    z.start()
    z.wait()

    f = file(getpath('.ble.list'), 'w')
    base = '/idmm/ble'
    for p in z.list(base):
        data = z.get(base+'/'+p)
        data1 = data[0]
        bleid = p[p.find('.')+1:]
        jmxaddr = data1[0:data1.find(':')] + data1[data1.rfind(':'):]
        dataaddr = data1.split()[0]
        f.write('%s %s %s\n'%(bleid, jmxaddr, dataaddr))
    f.close()

    f = file(getpath('.httpbroker.list'), 'w')
    for p in z.list('/idmm/httpbroker'):
        f.write(p)
        f.write('\n')
    f.close()

    f = file(getpath('.broker.list'), 'w')
    for p in z.list('idmm/broker'):
        f.write(p)
        f.write('\n')
    f.close()
    
    z.close()

def getpath(f):
    p = os.path.abspath(sys.argv[0])
    #print p
    p = p[:p.rfind(os.path.sep)+1]
    return p + f

def qmon(zkaddr):
    addrfile = getpath('.ble.list')
    need_refresh_addrlist = True
    # try:
    #     st = os.stat(addrfile)
    #     if time.time() - st.st_mtime > 3600.0:
    #         need_refresh_addrlist = True
    # except:
    #     need_refresh_addrlist = True
    if need_refresh_addrlist:
        getaddrs(zkaddr)
    m = []
    
    stat = [0, 0, 0]
    for line in file(addrfile):
        d = line.strip().split()
        if len(d) < 2:
            continue
        getinfo(d[0], d[1], m, stat)
    if True: return 
    print '\n--------size > 0:'
    print 'BLEID  TOPIC_ID   CLIENT_ID  total   size   sending  err'
    print '--------------------------------------------------------'
    for s in m:
        print '====', s
        
    print '\n=====total====='
    print '--total--size--sending'
    print '%d\t%d\t%d'%(stat[0], stat[1], stat[2])

# 列出全部total数量>0的队列， 并使用clear 的jmx端口清空内存队列
def clear_all_queue(zkaddr):
    qlist = listQ(zkaddr)
    for q in qlist:
        if q.total > 0:
            print "clear ", q.client, q.topic
            url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/clear/%s/%s' %(
                q.jmxaddr, q.client, q.topic)
            s = urllib2.urlopen(url)
            s.read()
    print "done"

if __name__ == '__main__':
    #zkaddr = '10.113.161.103:8611,10.113.161.104:8611,10.113.161.105:8611'
    #zkaddr = '10.149.85.32:2185,10.149.85.33:2185,10.149.85.34:2185'
    zkaddr='172.21.0.46:3181'
    #zkaddr='172.21.11.63:21810,172.21.11.64:21810,172.21.11.65:21810'
    print 'zkaddr', zkaddr
    qmon(zkaddr)
