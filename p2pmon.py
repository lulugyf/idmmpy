#coding=utf-8

# 端到端 监控采集， 监控两个主题的积压数量：
#    T109SmspGWDest   宽带局拆业务
#    T109SmspDest     信控停开机和局拆业务
# 5分钟采集一次
# p2pmon.sh
# . ${HOME}/.bash_profile
# cd ${HOME}/idmm3/py
# python p2pmon.py >>../log/p2pmon.log 2>&1 &
#
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * sh /idmm/idmm3/py/p2pmon.sh >/idmm/idmm3/log/p2pmon_cron.log 2>&1

import sys
import subprocess as sb
import re

def shell_exec(cmd):
    try:
        p = sb.Popen(cmd, stdout=sb.PIPE, stderr=sb.PIPE, shell=True)
        sout = p.stdout.read()
        serr = p.stderr.read()
        p.terminate()
        return sout, serr, None
    except sb.CalledProcessError, x:
        sys.stderr.write("failed!  return code=%s" % x.returncode)
        return None, x.returncode, x.output

'''
/idmm/idmm3/mon/qmon_fq_2018-09-26-1526:[T109SmspGWDest-A]              Sub113Credit           7960    0       0       7
/idmm/idmm3/mon/qmon_fq_2018-09-26-1526:[T109SmspDest-A]                Sub113Credit           5614419 1       0       4
/idmm/idmm3/mon/qmon_xq_2018-09-26-1526:[T109SmspGWDest-B]              Sub113Credit           2349    0       0       0
/idmm/idmm3/mon/qmon_xq_2018-09-26-1526:[T109SmspDest-B]                Sub113Credit           8312400 3       0       0

T109SmspGWDest   宽带局拆业务
T109SmspDest     信控停开机和局拆业务
'''
def mon():
    qdict = {
        'T109SmspGWDest-A': "消息中间件_宽带局拆业务", 'T109SmspGWDest-B': "消息中间件_宽带局拆业务",
        'T109SmspDest-A': "消息中间件_信控停开机和局拆业务", 'T109SmspDest-B': "消息中间件_信控停开机和局拆业务",
    }
    cmdstr = "grep -e T109SmspGWDest -e T109SmspDest /idmm/idmm3/mon/qmon*"
    sout, serr, x = shell_exec(cmdstr)
    result = {}
    rr = re.compile(r"[xf]q_([-\d]+):\[([^\]]+)\]\t\t([^\t]+)\t\t(\d+)\t(\d+)")
    pos = 0
    timestr = None
    while True:
        r = rr.search(sout, pos)
        if r is None: break
        pos = r.end(2)
        timestr = r.group(1)
        topic = r.group(2)
        sz = r.group(5)
        k = qdict.get(topic, topic)
        result[k] = result.get(k, 0) + int(sz)

    from local_db import conndb
    db, cur = conndb("ibnms/ykRwj!b6@yfsdb")
    try:
        for k, v in result.items():
            cur.execute("insert into overstock_moni(data_time, point_name, overstock_num) values(to_date(:v0, 'YYYY-MM-DD-HH24MI'), :v1, :v2)",
                            (timestr, k.decode('utf-8').encode("GBK"), v))
            db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    mon()
