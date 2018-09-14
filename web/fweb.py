#coding=utf-8

import os
import json
from multiprocessing import Pool
from cStringIO import StringIO

from flask import Flask

import pagegen as pg
import rsh
import zk

app=Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/exit")
def exit():
    print("exit from web!!!!!!")
    os._exit(0)

def _proc1(args):
    return rsh.proc_info(*args)

def _proc2(args):
    return rsh.hostinfo(*args)

@app.route("/proc")
def proc():
    r = StringIO()
    pg.page_head("IDMM 进程信息", r)

    conf = json.load(open("conf.json"))

    args = [ (h['ipaddr'], h['user'], h['diskpath']) for h in conf['host-list']]
    if len(args) > 1:
        pool = Pool(processes=len(args))
        hinfos = pool.map(_proc2, args)
        pool.close()
    else:
        hinfos = [_proc2(args[0]),]

    pg.gentable("主机信息",
                ["hostname", "ipaddr", "cpu-idle", "disks</br>(path free used)", "mem-free-kb", "mem-used", "swap-free-kb", "swap-used"],
                [(h['hostname'], h['host'], h['cpu-idle'] + " %",
                  "<br>".join(["%s %s %s %%" % (d['path'], d['available'], d['percent']) for d in h["disks"]]),
                  h['mem-free-kb'], "%.2f %%" % ((h['mem-total-kb'] - h['mem-free-kb']) * 100.0 / h['mem-total-kb']),
                  h['swap-free-kb'],
                  "%.2f %%" % ((h['swap-total-kb'] - h['swap-free-kb']) * 100.0 / h['swap-total-kb'])) for h in hinfos],
                r)

    ble_jmx, broker_jmx = zk.get_jmxaddr(conf['zookeeper'])
    broker_jmx.extend(ble_jmx)
    jmx_ports = {}
    for a in broker_jmx:
        a = a[1]
        host, port = a.split(":")
        if jmx_ports.has_key(host):
            p = jmx_ports[host]
            p.append(port)
        else:
            jmx_ports[host] = [port]
    for k in jmx_ports.keys():
        jmx_ports[k] = set(jmx_ports[k])

    procinfo = []
    # _ = [ procinfo.extend(rsh.proc_info(h['ipaddr'], h['user'], h['deploypath'], h['lsof'], jmx_ports.get(h['ipaddr'], None)) )
    #       for h in conf['host-list'] ]
    args = [ (h['ipaddr'], h['user'], h['deploypath'], h['lsof'], jmx_ports.get(h['ipaddr'], None) )
          for h in conf['host-list'] ]
    if len(args) > 1:
        pool = Pool(processes=len(args))
        ret = pool.map(_proc1, args)
        pool.close()
    else:
        ret = [_proc1(args[0]),]
    for v in ret: procinfo.extend(v)

    for p in procinfo:
        jmxaddr="%s:%s"%(p['host'], p['jmxport'])
        for v in ble_jmx:
            if v[1] == jmxaddr:
                p['ble-id'] = v[0]

    pg.gentable("进程信息",
                ["host", "pid", "cwd</br>ble-id", "start-time", "proc-type", "listen-ports", "jmxport", "tcp-in", "tcp-out", "datasource</br>active/idle/max"],
                [(p['host'], p['pid'], p['cwd']+"</br>"+p.get("ble-id", ""), p['start-time'], p['proc-type'], p['listen-ports'], p['jmxport'],
                  len(p['tcp-in']), len(p['tcp-out']),
                   "</br>".join(["%s: %s/%s/%s"%(v['name'], v["active"], v["idle"], v["maxActive"])
                                 for v in p['datasource']])) for p in procinfo],
                r)

    r.write("</br><div><a href='/killall' target='_blank'>shutdown all processes</a></div>")
    r.write("</br><div><a href='/startall' target='_blank'>startup all processes</a></div>")
    pg.page_tail(r)
    return r.getvalue()

@app.route("/killall")
def killall():
    r = StringIO()
    conf = json.load(open("conf.json"))
    for h in conf['host-list']:
        r.write("---host: %s path: %s\n"%(h['ipaddr'], h['deploypath']))
        r.write(rsh.shutdown_all(h['ipaddr'], h['user'], h['deploypath']))
        r.write("\n")
    return r.getvalue()

@app.route("/startall")
def startall():
    r = StringIO()
    conf = json.load(open("conf.json"))
    for h in conf['host-list']:
        r.write("---host: %s path: %s\n" % (h['ipaddr'], h['deploypath']))
        r.write(rsh.startup_all(h['ipaddr'], h['user'], h['deploypath']))
        r.write("\n")
    return r.getvalue()

@app.route("/qinfo")
def qinfo():
    import ble
    import operator
    import time
    conf = json.load(open("conf.json"))
    zkaddr = conf['zookeeper']
    qlist = ble.listQ(zkaddr)
    succ_count, err_count, sz,sending, topic_count = 0, 0, 0,0, 0
    bleids, bleaddr, blecounts = {}, {}, {}
    for q in qlist:
        succ_count += q.total
        err_count += q.err
        sz += q.size
        sending += q.sending
        bleids[q.bleid] = bleids.get(q.bleid, 0) + 1
        blecounts[q.bleid] = blecounts.get(q.bleid, 0) + q.total
        if not bleaddr.has_key(q.addr):
            bleaddr[q.bleid] = q.addr
    qlist = sorted(qlist, key=operator.attrgetter('size', 'err', 'total'), reverse=True)

    r = StringIO()
    pg.page_head("IDMM 队列积压监控, 采集时间 %s"%(time.strftime("%Y-%m-%d-%H:%M:%S")), r)

    pg.gentable("IDMM 队列积压监控, 采集时间 %s"%(time.strftime("%Y-%m-%d-%H:%M:%S")),
                "BLE-ID 消息主题 消费者ID 总量 积压 失败 在途 status".split(),
                [(q.bleid, q.topic, q.client, q.total, q.size, q.err, q.sending, q.status) for q in qlist],
                r)

    pg.page_tail(r)
    return r.getvalue()

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8183)
