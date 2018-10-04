#coding=utf-8


import subprocess as sb
import re
import urllib2
import json
import sys
import os

sys.path.append('..')
import tm

def rexec(host, user, cmd):
    try:
        output = sb.check_output(["ssh", "%s@%s"%(user, host), cmd], shell=False)
        return output
    except sb.CalledProcessError, x:
        sys.stderr.write("failed!  return code=%s" % x.returncode)
        return x.output

def lexec(cmd, shell=False):
    try:
        output = sb.check_output(cmd, shell=shell)
        return output, None
    except sb.CalledProcessError, x:
        sys.stderr.write("failed!  return code=%s" % x.returncode)
        return None, x.output


# 获取主机的基本信息
def hostinfo(host, user, dfs):
    out = rexec(host, user, "export TERM=vt100; echo '==>'`hostname`; df -k %s; echo; echo; top -b -n 1|head -15"%(" ".join(dfs)))
    hinfo = {'hostname':"", 'cpu-idle':"", "disks":[], 'mem-free-kb':0, 'mem-total-kb':1, 'swap-total-kb':1, 'swap-free-kb':0}

    dinfo = []
    for dk in dfs:
        # 1K-blocks      Used Available Use% Mounted on
        df = re.compile(r"(\d+) +(\d+) +(\d+) +(\d+)%% +(%s)"%dk)
        r = df.search(out)
        if r is not None:
            dinfo.append({"path":dk, "total-kb":r.group(1), "available":r.group(2), "percent":r.group(4)})
    hinfo["disks"] = dinfo
    hinfo['host'] = host
    hinfo['hostname'] = re.compile(r'==>([^\n]+)\n').search(out).group(1)
    cpu = re.compile(r"Cpu\(s\): .+ ([\d\.]+)%id,")
    r = cpu.search(out)
    if r is not None:
        hinfo['cpu-idle'] = r.group(1)

    mem = re.compile(r"Mem: +(\d+)k +total, +(\d+)k +used, +(\d+)k +free")
    r = mem.search(out)
    if r is not None:
        hinfo['mem-total-kb'] = int(r.group(1))
        hinfo['mem-free-kb'] = int(r.group(3))
    swap = re.compile(r"Swap: +(\d+)k +total, +(\d+)k +used, +(\d+)k +free")
    r = swap.search(out)
    if r is not None:
        hinfo['swap-total-kb'] = int(r.group(1))
        hinfo['swap-free-kb'] = int(r.group(3))

    return hinfo

'''
	   listenport=`grep netty.listen.port $$cwd/config/ble/*.properties|awk -F "=" '{print $$NF}'`;
	   echo "#%CWD: $$pid $$cwd $$class $$jmxport $$listenport";
	   echo "#%LSOF:"; ${lsof} -p $$pid -P|grep TCP|awk '{print $$(NF-1), $$NF}';
	   echo "#%MEM:"; curl "http://localhost:$$jmxport/jolokia/read/java.lang:type=Memory" 2>/dev/null; echo "";
	   echo "#%DATASOURCE:"; curl "http://localhost:$$jmxport/jolokia/exec/com.sitech.crmpd.idmm:name=dsMon/dsinfo" 2>/dev/null; echo "";
'''
# 获取IDMM ble broker进程信息
def proc_info(host, user, paths, lsof, jmx_ports=None):
    cmd = """cat %s %s|while read pid; do echo "##PS:";
	   ls -l /proc/$pid/cwd;
	   %s -p $pid -P|grep TCP|awk '{print $(NF-1), $(NF)}';
	   done""" % (" ".join(["%s/log/ble.pid"%p for p in paths ]),
                  " ".join(["%s/log/broker.pid"%p for p in paths ]),
                  lsof)
    out = rexec(host, user, cmd)
    procs = []
    for s in out.split("##PS:")[1:]:
        proc = {"host":"", "pid":"[not exists]", "cwd":"", "start-time":"", "proc-type":"", "listen-ports":"", "jmxport":"", "tcp-in":[], "tcp-out":[], "datasource":[]}
        procs.append(proc)
        s = s.strip()
        #lines = s.split("\n")
        #l0 = lines[0]   #  lrwxrwxrwx 1 crmpdscm CRM_PD 0 Sep 12 09:44 /proc/7240/cwd -> /crmpdscm/idmm3/broker0
        r = re.compile(r" /proc/(\d+)/cwd +-> +([^ \r\n]+)").search(s)
        if r is not None:
            proc['pid'] = r.group(1)
            proc['cwd'] = r.group(2)
        proc['start-time'] = " ".join(s[:s.find('\n')].split()[5:8])
        pos = 0
        rr = re.compile(r":(\d+) +\(LISTEN\)")
        listen_ports = []
        while True:
            r = rr.search(s, pos)
            if r is None: break
            pos = r.end()
            listen_ports.append(r.group(1))
        if len(listen_ports) >= 3:
            proc['proc-type'] = "Broker"
        elif len(listen_ports) == 2:
            proc['proc-type'] = "BLE"
        proc['listen-ports'] = listen_ports

        # 解析 TCP 连接   zntd1:35770->172.21.0.67:3307 (ESTABLISHED)
        ports = set(listen_ports)
        tcp_in = []
        tcp_out = []
        rr = re.compile(r'\n[^:]+:(\d+)->([^:]+):(\d+) +\(ESTABLISHED\)')
        pos = 0
        while True:
            r = rr.search(s, pos)
            if r is None: break
            pos = r.end()
            lport, rhost, rport = r.group(1), r.group(2), r.group(3)
            if lport in ports:
                tcp_in.append((lport, rhost, rport))
            else:
                tcp_out.append((lport, rhost, rport))
        proc['tcp-in'] = tcp_in
        proc['tcp-out'] = tcp_out
        proc['host'] = host

        # 测试寻找jmx端口, 然后向jmx端口查询其它的参数
        if jmx_ports is not None:
            _ports = [p for p in ports if p in jmx_ports]
        if len(_ports) < 1:
            _ports = ports
        for port in _ports:
            try:
                url = 'http://%s:%s/jolokia/read/java.lang:type=Memory'%(host, port)
                s = urllib2.urlopen(url)
                o = json.load(s)
                o1 = o['value']['HeapMemoryUsage']
                proc['heap-memory'] = "{0:.3f} MB/{1:.3f} MB {2:.2f} %".format(o1['used'] / 1024.0 / 1024,
                                                                         o1['max'] / 1024.0 / 1024,
                                                                         o1['used'] * 100.0 / o1['max'])
                proc['jmxport'] = port
                url1 = 'http://%s:%s/jolokia/exec/com.sitech.crmpd.idmm:name=dsMon/dsinfo'%(host, port)
                s = urllib2.urlopen(url1)
                o = json.load(s)
                ds = []
                proc['datasource'] = ds
                for k, v in o['value'].items():   # idle: Int, active: Int, maxActive: Int, className: String, props: String
                    d = {"name":k, "idle":v["idle"], "active":v["active"], "maxActive":v["maxActive"]}
                    ds.append(d)
                break
            except:
                pass

    #print(procs)
    return procs

def shutdown_all(host, user, paths):
    scripts = ["%s/bin/broker/shutdown.sh"%p for p in paths ]
    scripts.extend(["%s/bin/ble/shutdown.sh"%p for p in paths])
    cmd = ";\n".join( scripts )
    return rexec(host, user, cmd)

def startup_all(host, user, paths):
    scripts = ["%s/bin/broker/startup.sh" % p for p in paths]
    scripts.extend(["%s/bin/ble/startup.sh" % p for p in paths])
    cmd = ";\n".join( scripts )
    return rexec(host, user, cmd)


def tail(f, n, offset=0):
    """Reads a n lines from f with an offset of offset lines."""
    avg_line_length = 74
    to_read = n + offset
    while 1:
        try:
            f.seek(-(avg_line_length * to_read), 2)
        except IOError:
            # woops.  apparently file is smaller than what we want
            # to step back, go to the beginning instead
            f.seek(0)
        pos = f.tell()
        lines = f.read().splitlines()
        if len(lines) >= to_read or pos == 0:
            return lines[-to_read:offset and -offset or None]
        avg_line_length *= 1.3

# 表空间采集日志读取，  采集方法： db.tablespace_mon(),  间隔: 1hour
# 返回
# 20180823011001
# TBS_IDMMDB_IDX	5.898%	780518MB	829440MB
# TBS_IDMMDB_DATA	28.255%	749366MB	1044480MB
def read_tbs_log(fpath, tbs_names, count=24):
    with open(fpath) as f:
        lines = tail(f, count*3)
    rows = []
    flds = None
    rr = re.compile(r"[^\t]+\t([\d\.]+)\%\t(\d+)GB\t(\d+)GB")  # print "{0}\t{1:.3f}%\t{2:.0f}MB\t{3:.0f}MB".format(*r)
    for line in lines:
        if line.startswith("2"):
            if flds is not None:
                rows.append(flds)
            flds = [line.strip()]
            flds.extend([None for i in range(len(tbs_names))])
        else:
            for i in range(len(tbs_names)):
                tn = tbs_names[i]
                if line.startswith(tn):
                    if flds is None: break
                    r = rr.search(line)
                    if r is not None:
                        f = r.groups()
                        flds[i+1] = [f[0], int(f[1]), int(f[2])-int(f[1])]
                    break
    if flds is not None:
        rows.append(flds)
    return rows

def read_msg_test_log(fpath, count=144):
    with open(fpath) as f:
        lines = tail(f, count)
    header = "探测时间 发送消息数 平均响应时间 接收消息数 平均响应时间".split()
    rows = []
    for line in lines:
        if not line.startswith("== "):
            continue
        r = line.split("\t")
        if len(r) < 5:
            rows.append([r[0][3:], r[1], 0, 0, 0])
        else:
            rows.append([r[0][3:], r[1], r[2], r[3], r[4]])
    return header, rows

def scp_log_files(host_list, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    sh_file = "%s/scp_get.sh" % out_dir
    with open(sh_file, "w") as f:
        for h in host_list:
            dps = h['deploypath']
            for i in range(len(dps)):
                deploy_path = dps[i]
                f.write( "scp -p %s@%s:%s/log/ble.debug %s/%s-%s-ble.debug\n"%(
                    h['user'], h['ipaddr'], deploy_path, out_dir, h['ipaddr'], i+1
                    ) )
                f.write( "scp -p %s@%s:%s/log/broker.debug %s/%s-%s-broker.debug\n" % (
                    h['user'], h['ipaddr'], deploy_path, out_dir, h['ipaddr'], i + 1
                    ) )

    sout, serr = lexec(["sh", sh_file])
    if serr is not None:
        sys.stderr.write("failed!  return code= %s" % (serr) )
        return None
    print sout

    today_str = tm.datedelta(0)[8:10]
    #print "today_str", today_str
    for f in os.listdir(out_dir): # 先检查文件修改时间， 如果非当天的， 则删除
        if f.find(".debug") < 0: continue
        fpath = "%s/%s"%(out_dir, f)
        st = os.stat(fpath)
        fdate = tm.tmstr(str(int(st.st_mtime)*1000))
        print 'fdate', fdate, fpath
        fdate = fdate[8:10]
        if today_str != fdate:
            print "debug modified not today", fpath, today_str, fdate
            os.remove(fpath)
            continue
    # 分时段统计
    sh = "cd %s && grep cost *broker*|awk '{if($(NF-1)>499) print substr($2,6,5)}' >min && grep timeout *ble*|awk '{print substr($2,6,5)}' >>min && cat min|sort|uniq -c" % (
        out_dir )
    sout, serr = lexec([sh,], shell=True)
    print '[sout]', sout
    print '[serr]', serr
    if serr is not None:
        return serr
    else:
        return sout

# qmon脚本每5分钟采集的队列积压数据, 统计按主题和时间的生产/消费数量表格
def stastic_5m_all(fpath='/idmm/idmm3/mon/_bak'):
    if not os.path.exists(fpath):
        return [],[],[]
    dic = {}
    def one_file(f):
        total = 0
        size = 0
        for line in open(f):
            ff = line.split()
            if len(ff) != 6:
                continue
            total += int(ff[2])
            size += int(ff[3])
        return total, size
    for f in os.listdir(fpath):
        # fname:  qmon_fq_2018-05-08-0105
        if not f.startswith('qmon'):
            continue
        dd = f[8:]
        ret = one_file(fpath+"/"+f)
        if dic.has_key(dd):
            v = dic[dd]
            dic[dd] = (v[0]+ret[0], v[1]+ret[1])
        else:
            dic[dd] = ret

    lst = [(k, v[0], v[1]) for k, v in dic.items()]
    lst = sorted(lst, key=lambda v: v[0])

    x = []
    y1 = []
    y2 = []
    vl = lst[0]
    for v in lst:
        #print v[0], v[1]-vl[1], v[1]-vl[1]-(v[2]-vl[2])
        x.append(v[0])
        y1.append(v[1]-vl[1])
        y2.append(v[1]-vl[1]-(v[2]-vl[2]))
        vl = v
    return ",".join(["'%s'"%i[11:] for i in x]), ",".join(["%d"%i for i in y1]), ",".join(["%d"%i for i in y2])

# qmon脚本每5分钟采集的队列积压数据, 统计按主题和时间的生产/消费数量表格
# python -c "import rsh; rsh.stastic_5m('../local/mon')"
def stastic_5m(fpath='/idmm/idmm3/mon/_bak'):
    if not os.path.exists(fpath):
        return '',''
    ys = {}
    def _one_file(f):
        for line in open(f):
            ff = line.split()
            if len(ff) != 6:
                continue
            total, size = int(ff[2]), int(ff[3])
            k = "%s,%s"%(ff[0][1:-1], ff[1])
            #print '    ', k, total, size
            if ys.has_key(k):
                v = ys[k]
                v.append((total, size))
            else:
                ys[k] = [(total, size),]

    xs = []
    flist = sorted([f for f in os.listdir(fpath) if f.startswith("qmon_xq")] )
    for f in flist:
        # fname:  qmon_fq_2018-05-08-0105
        xs.append(f[13:])
        #print f
        _one_file(fpath+"/"+f)
    lines = []
    for k, v in ys.items():
        p = "['%s', %s]"%(k+"-P", ",".join(["%d"%(v[i][0]-v[i-1][0], ) for i in range(1,len(v))]) )
        c = "['%s', %s]" % (k + "-C", ",".join(["%d" % (v[i][0]-v[i-1][0]-(v[i][1] - v[i-1][1]),) for i in range(1, len(v))]))
        lines.append(p)
        #lines.append(c)

    return ",".join(["'%s'"%i[11:] for i in xs]), ",\n".join(lines[:12])


def main():
    host, user = "172.21.0.46", "crmpdscm"
    #print rexec("172.21.0.46", "crmpdscm", "export TERM=vt100; echo '====='; df -k /crmpdscm ; echo; echo; top -b -n 1|head -15")
    #hostinfo("172.21.0.46", "crmpdscm", ["/crmpdscm", "/crmpdscmweb"])
    proc_info(host, user, ['/crmpdscm/idmm3/broker0'], "/usr/sbin/lsof")

if __name__ == '__main__':
    main()
