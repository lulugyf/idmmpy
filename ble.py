#!/bin/env python
# -*- coding: utf-8 -*-

import zk
import urllib2
import json
import sys
import os
import time

# 消息中间件BLE队列监控

class qinfo:
    def __init__(self, jobj, bleid, addr):
        self.topic = jobj['target_topic_id']
        self.client = jobj['target_client_id']
        self.total = jobj['total']
        self.size = jobj['size']
        self.sending = jobj['sending']
        self.err = jobj['err']
        self.bleid = bleid
        self.addr = addr
        self.status = jobj['status']
        self.m5_prod = 0
        self.m5_cons = 0

def get_jmxaddr(zkaddr, ble_only=False):
    z = zk.ZKCli(zkaddr)
    z.start()
    z.wait()

    ble_ports = []
    base = '/idmm/ble'
    for p in z.list(base):
        if not p.startswith('id.') or len(p) < 11:
            continue
        data = z.get(base + '/' + p)
        data1 = data[0]
        #print '/idmm/ble', p, data1
        bleid = p[p.find('.') + 1:]
        jmxaddr = data1[0:data1.split()[0].rfind(':')] + data1[data1.rfind(':'):]
        ble_ports.append((bleid, jmxaddr))
    if ble_only:
        z.close()
        return ble_ports
    broker_ports = []
    base = '/idmm/broker'
    for p in z.list(base):
        data = z.get(base + '/' + p)
        data1 = data[0]
        data1 = data1[7:data1.find('/',8)]
        broker_ports.append((p, data1))  # http://???:??/jolokia
    z.close()
    return ble_ports, broker_ports

def listQ(zkaddr):
    q = []
    #addrs = get_jmxaddr(zkaddr, ble_only=True)
    # print repr(addrs)
    for bleid, jmxaddr in get_jmxaddr(zkaddr, ble_only=True):
        url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/info' % jmxaddr
        s = urllib2.urlopen(url)
        o = json.load(s)
        o1 = json.loads(o['value'])
        for o in o1:
            q.append(qinfo(o, bleid, ""))  #data_addr
    return q

# if __name__ == '__main__':
#     listQ("172.21.0.46:3181")
#     os._exit(0)

# 获取节点信息， 从zk中同步获取
def getnodeinfo(zkaddr):
    info = {}
    z = zk.ZKCli(zkaddr)
    z.start()
    ble = []
    base = '/idmm/ble'
    for p in z.list(base):
        if not p.startswith('id.') or len(p) < 11:
            continue
        data = z.get(base + '/' + p)
        data1 = data[0]
        bleid = p[p.find('.') + 1:]
        jmxaddr = jmxaddr = data1[0:data1.split()[0].rfind(':')] + data1[data1.rfind(':'):]
        dataaddr = data1.split()[0]
        ble.append('%s %s %s\n' % (bleid, jmxaddr, dataaddr))
    info['ble'] = ble

    httpbroker = []
    for p in z.list('/idmm/httpbroker'):
        httpbroker.append(p)
    info['httpbroker'] = httpbroker

    broker = []
    for p in z.list('idmm/broker'):
        broker.append(p)
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
        s = "%s\t\t%s\t\t%d\t%d\t%d\t%d\t%s"%(
            o['target_topic_id'], o['target_client_id'], o['total'], o['size'], o['sending'], o['err'],o['status'])
        if o['size'] > 0:
            m.append(bleid + '\t' + s)
        stat[0] += o['total']
        stat[1] += o['size']
        stat[2] += o['sending']
        last_topic, last_client = o['target_topic_id'], o['target_client_id']
        print s

    # 获取dboper 的积压
    '''url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/lockdetail/%s/%s'%(
        jmxaddr, last_client, last_topic)
    s = urllib2.urlopen(url)
    o = json.load(s)
    print o
    o1 = json.loads(o['value'])
    dboper_block = o1['global']['blocking_db_oper']
    print '    >>DBOper_Blocking %s'%bleid, dboper_block '''
    #print json.dumps(o1, indent=4)

def qmon(zkaddr):
    m = []
    
    stat = [0, 0, 0]
    for bleid, jmxaddr in get_jmxaddr(zkaddr, True):
        getinfo(bleid, jmxaddr, m, stat)
    #if True: return
    print '\n--------size > 0:'
    print 'BLEID  TOPIC_ID   CLIENT_ID  total   size   sending  err  status'
    print '----------------------------------------------------------------'
    for s in m:
        print '====', s
        
    print '\n=====total====='
    print '--total--size--sending'
    print '%d\t%d\t%d'%(stat[0], stat[1], stat[2])



def mem(zkaddr):
    ble_ports, broker_ports = get_jmxaddr(zkaddr)
    ble_ports.extend(broker_ports)
    print "---HeapMemoryUsage:"
    for id, jmxaddr in ble_ports:
        #print '--- jmxaddr:', jmxaddr
        url = "http://%s/jolokia/read/java.lang:type=Memory" % jmxaddr
        s = urllib2.urlopen(url)
        o = json.load(s)
        o1 = o[u'value']['HeapMemoryUsage']
        print id, '\t', "{0:.3f} MB/{1:.3f} MB {2:.2f} %".format(o1['used']/1024.0/1024,
                                    o1['max']/1024.0/1024, o1['used']*100.0/o1['max'])


if __name__ == '__main__':
    zkaddr = '172.18.231.6:7181'
    #from local_db import conf_zk_addr
    #zkaddr = conf_zk_addr()
    qmon(zkaddr)
    mem(zkaddr)
