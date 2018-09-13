#coding=utf-8


import subprocess as sb
import re
import urllib2
import json

def rexec(host, user, cmd):
    output = sb.check_output(["ssh", "%s@%s"%(user, host), cmd])
    return output

# 获取主机的基本信息
def hostinfo(host, user, dfs):
    out = rexec(host, user, "export TERM=vt100; echo '====='; df -k %s; echo; echo; top -b -n 1|head -15"%(" ".join(dfs)))
    hinfo = {}

    dinfo = []
    for dk in dfs:
        # 1K-blocks      Used Available Use% Mounted on
        df = re.compile(r"(\d+) +(\d+) +(\d+) +(\d+)%% +(%s)"%dk)
        r = df.search(out)
        if r is not None:
            dinfo.append({"path":dk, "total-kb":r.group(1), "available":r.group(2), "percent":r.group(4)})
    hinfo["disks"] = dinfo
    cpu = re.compile(r"Cpu\(s\): .+ ([\d\.]+)%id,")
    r = cpu.search(out)
    if r is not None:
        hinfo['cpu-idle'] = r.group(1)

    mem = re.compile(r"Mem: +(\d+)k +total, +(\d+)k +used, +(\d+)k +free")
    r = mem.search(out)
    if r is not None:
        hinfo['mem-total-kb'] = r.group(1)
        hinfo['mem-free-kb'] = r.group(3)
    swap = re.compile(r"Swap: +(\d+)k +total, +(\d+)k +used, +(\d+)k +free")
    r = mem.search(out)
    if r is not None:
        hinfo['swap-total-kb'] = r.group(1)
        hinfo['swap-free-kb'] = r.group(3)

    print repr(hinfo)

'''
	   listenport=`grep netty.listen.port $$cwd/config/ble/*.properties|awk -F "=" '{print $$NF}'`;
	   echo "#%CWD: $$pid $$cwd $$class $$jmxport $$listenport";
	   echo "#%LSOF:"; ${lsof} -p $$pid -P|grep TCP|awk '{print $$(NF-1), $$NF}';
	   echo "#%MEM:"; curl "http://localhost:$$jmxport/jolokia/read/java.lang:type=Memory" 2>/dev/null; echo "";
	   echo "#%DATASOURCE:"; curl "http://localhost:$$jmxport/jolokia/exec/com.sitech.crmpd.idmm:name=dsMon/dsinfo" 2>/dev/null; echo "";
'''
# 获取IDMM ble broker进程信息
def proc_info(host, user, paths, lsof):
    cmd = """cat %s %s|while read pid; do echo "##PS:";
	   ls -l /proc/$pid/cwd;
	   %s -p $pid -P|grep TCP|awk '{print $(NF-1), $(NF)}';
	   done""" % (" ".join(["%s/log/ble.pid"%p for p in paths ]),
                  " ".join(["%s/log/broker.pid"%p for p in paths ]),
                  lsof)
    out = rexec(host, user, cmd)
    procs = []
    for s in out.split("##PS:")[1:]:
        proc = {}
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
        if len(listen_ports) > 2:
            proc['proc-type'] = "Broker"
        else:
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

        # 测试寻找jmx端口, 然后向jmx端口查询其它的参数
        for port in ports:
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
                for k, v in o['value']:   # idle: Int, active: Int, maxActive: Int, className: String, props: String
                    v['name'] = k
                    ds.append(v)
                break
            except:
                pass

    print procs

def main():
    host, user = "172.21.0.46", "crmpdscm"
    #print rexec("172.21.0.46", "crmpdscm", "export TERM=vt100; echo '====='; df -k /crmpdscm ; echo; echo; top -b -n 1|head -15")
    #hostinfo("172.21.0.46", "crmpdscm", ["/crmpdscm", "/crmpdscmweb"])
    proc_info(host, user, ['/crmpdscm/idmm3/broker0'], "/usr/sbin/lsof")

if __name__ == '__main__':
    main()
