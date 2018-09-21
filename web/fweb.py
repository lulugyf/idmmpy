#coding=utf-8

import os
import sys
sys.path.append('..')
# import json
from multiprocessing import Pool
from cStringIO import StringIO
import time
from functools import wraps
import cPickle as pickle

from flask import Flask, request

import pagegen as pg
import rsh
import zk
import settings as conf
from db import stastics, getTopicsConf, table_part_list
import tm

#app.config['DEBUG'] = True

def pagehandle(title, css=None):
    def tags_decorator(func):
        @wraps(func)
        def decorator():
            r = StringIO()
            if css is None:
                pg.page_head(title, r)
            else:
                pg.page_head_css(title, r, css)
            func(r)
            pg.page_tail(r)
            return r.getvalue()
        return decorator
    return tags_decorator

app=Flask(__name__, static_url_path='/static')

@app.route('/')
def rootpage():
    return """
    <h1> IDMM 运维功能列表 </h1> <br/>
    &sect; <a href="/qinfo"><b>队列积压监控  </b></a><br/><br/>
    &sect; <a href="/proc"><b>主机和进程情况  </b></a><br/><br/>
    &sect; <a href="/qryid"><b>查询消息id (分区表模式)  </b></a><br/><br/>
    &sect; <a href="/getmsg"><b>提取消息内容  </b></a><br/><br/>
    &sect; <a href="/tbs"><b>表空间使用情况  </b></a><br/><br/>
    &sect; <a href="/log_timeouts"><b>数据库超时情况统计 </b></a><br/><br/>
    &sect; <a href="/yesterday_stastics"><b>昨日消息消费情况统计(分区表模式)  </b></a><br/><br/>
    &sect; <a href="/part_list"><b>表分区数据量估计(分区表模式)  </b></a><br/><br/>
    &sect; <a href="/msg_test"><b>消息收发探测采集  </b></a><br/><br/>
    &sect; <a href=""><b>  <br/></a><br/><br/>
    """

@app.route('/msg_test')
@pagehandle("消息收发探测采集")
def msg_test(out):
    header, rows = rsh.read_msg_test_log(conf.msg_test_log_file, 144)
    pg.gentable("消息收发探测采集记录", header, rows, out)

@app.route('/part_list')
@pagehandle("表分区数据量估计(分区表模式)")
def part_list(out):
    header, rows = table_part_list()
    pg.gentable("表分区记录数估计", header, rows, out)

@app.route('/log_timeouts')
@pagehandle("数据库超时告警日志统计", css='<link href="/static/c3.min.css" rel="stylesheet">')
def log_timeouts(out):
    outstr = rsh.scp_log_files(conf.host_list, conf.log_timeout_dir)
    xa =[]
    ya =[]
    rows = []
    for l in outstr.split('\n'):
        l = l.strip().split()
        if len(l) != 2: continue
        ya.append(l[0])
        xa.append("'%s'" % l[1])
        rows.append(l)


    out.write("<br /> 表格绘制< br />")
    x = ",".join(xa)
    y = ",".join(ya)
    out.write("""
    <script src="/static/c3.min.js"></script>
    <script src="/static/d3-5.4.0.min.js"></script>
<div id="chart"></div>
<script>
var chart = c3.generate({
    bindto: '#chart',
    data: {
        columns: [
            ['data1', %s]
        ],
        types: {
          data1: 'bar'
        }
    },
    axis: {
        y: {
         label: {
          text: 'SQL 超过 500ms 告警次数',
          position: 'outer-middle'
         }
        },
        x: {
            label: { text: '时间（当日）', position: 'outer-middle' },
            type: 'category',
            categories: [ %s ]
        }
    }
});
</script>
    """ % (y, x) )
    pg.gentable("按分钟统计的超时数量", "次数 时间".split(), rows, out)



@app.route('/yesterday_stastics')
@pagehandle("IDMM日统计-昨日消息消费情况统计")
def yesterday_stastics(out):
    out.write(pg.stactics_form(7))
    ndays = request.args.get('ndays', "-1")
    print "----", ndays
    days_n = int(ndays)
    st_date = tm.datedelta(days_n)
    fname = "%s/%s"%(conf.statics_data_dir, st_date)
    if not os.path.exists(fname):
        zcli = zk.ZKCli(conf.zookeeper)
        zcli.start()
        ver_node = zcli.get('/idmm/configServer/version')
        zcli.close()
        ver = str(ver_node[0])
        #print "conf version", ver, repr(ver_node)
        topics = getTopicsConf(ver)

        # 调用统计sql
        title, st_date, header, rows = stastics(days_n, topics)
        with open(fname, "wb") as f:
            pickle.dump({"title":title, "st_date":st_date, "header":header, "rows":rows}, f)
    else:
        with open(fname, "rb") as f:
            dd = pickle.load(f)
            title, st_date, header, rows = dd["title"], dd['st_date'], dd['header'], dd['rows']

    # 统计按bleid的消息总量
    blecounts = {}
    for r in rows:
        bleid, count = r[-2], r[1]
        blecounts[bleid] = blecounts.get(bleid, 0) + count

    pg.gentable(title, header, rows, out)
    pg.gentable("按bleid的消息量统计", ["bleid", "count"], [(k, v) for k, v in blecounts.items()], out)

@app.route('/tbs')
@pagehandle("IDMMDB 表空间使用情况")
def tbs(out):
    tbs_names = ("TBS_IDMMDB_IDX", "TBS_IDMMDB_DATA")
    rows = rsh.read_tbs_log(conf.database_tbs_file, tbs_names, 24*15)
    rows_16 = [r for r in rows if r[0][8:10]=='16'] # hour=16
    # header_cols = "time,tbs,used(%),free(MB),total(MB),tbs,used(%),free(MB),used(MB)".split(",")
    rows_show = []
    # 把最后一条先展示出来
    row = rows[-1]
    r = [row[0]]
    for n in range(len(tbs_names)):
        tb = row[n + 1]
        r.extend(tb)
        r.append("")
    rows_show.append(r)
    rows_show.append(["&nbsp;" for i in range(len(tbs_names)*4+1)])

    last_xx = [0 for i in range(len(tbs_names))]
    for r in rows_16:   # 计算比前一条记录的差值
        row = [r[0],]
        for n in range(len(tbs_names)):
            tb = r[n+1]
            if last_xx[n] == 0:
                last_xx[n] = tb[-1]
                row.extend(tb)
                row.append(0)
            else:
                cost = tb[-1]-last_xx[n]
                last_xx[n] = tb[-1]
                row.extend(tb)
                row.append(cost)
        rows_show.append(row)

    header = """<tr><th rowspan=2>time</th>{0}</tr>
    <tr>{1}</tr>""".format(
        "".join(["<th colspan=4>%s</th>"%n for n in tbs_names]),
        "<th>used(%)</th><th>free(GB)</th><th>used(GB)</th><th>used-daily(GB)</th>" * len(tbs_names)
    )
    pg.gentable("IDMMDB 表空间使用情况(每小时采样)",
                header,
                rows_show, out)

@app.route('/qryid', methods=["POST", "GET"])
def qryid():
    import selid1
    r = StringIO()
    pg.page_head("IDMM 消息查询", r)
    r.write(pg.qryid_form())
    if request.method == 'POST':
        id = request.form['id']
        if id is not None:
            id = id.strip()
            selid1.qryid_web(id, r)
    pg.page_tail(r)
    return r.getvalue()

@app.route("/getmsg", methods=["POST", "GET"])
def getmsg():
    if request.method == 'POST':
        import selid1
        from tm import time_offset
        fm = request.form
        params = {k:v for k, v in fm.items()}
        recent = params.get("recent_min", "").strip()
        if recent != "":
            params['begin_time'] = time_offset(0-int(recent)*60)
        if len(params['end_time'].strip()) == 0:
            params['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        # def dumpTopcByTime(topic, client, tm_begin, tm_end, status, patterns, table_count):
        return "<pre>" + "\n".join(selid1.dumpTopcByTime(
            params['topic'], params['client'], params['begin_time'], params['end_time'],
            params['msgstatus'], params['patterns'], conf.index_table_count )
        ) + "</pre>"
    else:
        r = StringIO()
        pg.page_head("IDMM 消息内容提取", r)
        r.write( pg.getmsgpage() )
        pg.page_tail(r)
        return r.getvalue()

@app.route("/killall", methods=["POST", "GET"])
def killall(r):
    r = StringIO()
    pg.page_head("IDMM shutdown all", r)
    if request.method == 'POST':
        if request.form["pass"] != "123":
            return "!!! forbiden"
        r.write("<pre>")
        for h in conf.host_list:
            r.write("---host: %s path: %s\n"%(h['ipaddr'], h['deploypath']))
            r.write(rsh.shutdown_all(h['ipaddr'], h['user'], h['deploypath']))
            r.write("\n")
        r.write("</pre>")
    else:
        r.write(pg.loginpage() )
    pg.page_tail(r)
    return r.getvalue()

@app.route("/startall")
def startall():
    r = StringIO()
    r.write("<pre>")
    for h in conf.host_list:
        r.write("---host: %s path: %s\n" % (h['ipaddr'], h['deploypath']))
        r.write(rsh.startup_all(h['ipaddr'], h['user'], h['deploypath']))
        r.write("\n")
    r.write("</pre>")
    return r.getvalue()



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
    args = [ (h['ipaddr'], h['user'], h['diskpath']) for h in conf.host_list]
    if len(args) > 1:
        pool = Pool(processes=len(args))
        hinfos = pool.map(_proc2, args)
        pool.close()
    else:
        hinfos = [_proc2(args[0]),]

    pg.gentable("主机信息",
                ["hostname", "ipaddr", "cpu-idle", "disks<br/>(path free used)", "mem-free-kb", "mem-used", "swap-free-kb", "swap-used"],
                [(h['hostname'], h['host'], h['cpu-idle'] + " %",
                  "<br />".join(["%s %s %s %%" % (d['path'], d['available'], d['percent']) for d in h["disks"]]),
                  h['mem-free-kb'], "%.2f %%" % ((h['mem-total-kb'] - h['mem-free-kb']) * 100.0 / h['mem-total-kb']),
                  h['swap-free-kb'],
                  "%.2f %%" % ((h['swap-total-kb'] - h['swap-free-kb']) * 100.0 / h['swap-total-kb'])) for h in hinfos],
                r)

    ble_jmx, broker_jmx = zk.get_jmxaddr(conf.zookeeper)
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
          for h in conf.host_list ]
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
                ["host", "pid", "cwd<br/>ble-id", "start-time", "proc-type", "listen-ports", "jmxport", "tcp in/out", "datasource<br/>active/idle/max"],
                [(p['host'], p['pid'], p['cwd']+"<br/><b>"+p.get("ble-id", "")+"</b>", p['start-time'], p['proc-type'], p['listen-ports'], p['jmxport'],
                  "%d/%d"%(len(p['tcp-in']), len(p['tcp-out']) ),
                   "<br/>".join(["%s: %s/%s/%s"%(v['name'], v["active"], v["idle"], v["maxActive"])
                                 for v in p['datasource']])) for p in procinfo],
                r)

    r.write("<br/><div><a href='/killall' target='_blank'>shutdown all processes</a></div>")
    r.write("<br/><div><a href='/startall' target='_blank'>startup all processes</a></div>")
    pg.page_tail(r)
    return r.getvalue()


@app.route("/qinfo2")
def qinfo2():
    import ble
    import operator
    import time
    zkaddr = conf.zookeeper
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


import m5_mon as mon


@app.route("/qinfo")
def qinfo():
    import ble
    import operator
    import time

    #conf = json.load(open("conf.json"))
    zkaddr = conf.zookeeper
    qlist = ble.listQ(zkaddr)
    qlist = sorted(qlist, key=operator.attrgetter('size', 'err', 'total'), reverse=True)

    r = StringIO()
    title = "IDMM 队列积压监控, 采集时间 %s"%(time.strftime("%Y-%m-%d-%H:%M:%S"))
    pg.page_head(title, r)

    headers = "BLE-ID 消息主题 消费者ID 总量 积压 失败 在途 status 5m生产 5m消费".split()
    mon.get_mon(qlist)
    pg.gentable(title,
                headers,
                [(q.bleid, q.topic, q.client, q.total, q.size, q.err, q.sending, q.status, q.m5_prod, q.m5_cons) for q in qlist if q.total>0],  #if q.topic=='TDst2'
                r)
    pg.page_tail(r)
    return r.getvalue()

if __name__=='__main__':
    os.putenv('NLS_LANG', 'American_America.zhs16gbk')
    if not os.path.exists(conf.statics_data_dir):
        os.makedirs(conf.statics_data_dir)
    mon.start_mon(conf.zookeeper, conf.minutes_data_dir)
    app.run(host='0.0.0.0', port=8183, debug=False)
