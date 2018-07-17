#-*- coding: utf-8 -*-
#[xqidmm1]/idmm/idmm3/monitor>cat mon1.py

import string
import os,sys
import time
import datetime
import commands
import json
import operator

print("--- file path: ", os.path.abspath(__name__))
sys.path.insert(0, os.getcwd())
import ble


'''
date_time = '15.09.2017 20:05:02'
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime(time.strptime(date_time, pattern)))
print epoch*1000


wangbin@si-tech.com.cn

SELECT TO_NUMBER(TO_DATE('2017-09-16 00:00:00', 'YYYY-MM-DD HH24:MI:SS') - TO_DATE('1970-01-01 8:0:0', 'YYYY-MM-DD HH24:MI:SS')) * 24 * 60 * 60 * 1000 FROM DUAL;
'''

def conndb(sysuser=False):
    import cx_Oracle
    #sys.path.insert(0, '/idmm/idmm3/monitor')
    #import data_decrypt
    #if sysuser:
    #    db = cx_Oracle.connect('tempuser/abcd1234@momdb')
    #else:
    #    passwd = data_decrypt.decryptData_auth()
    #    db = cx_Oracle.connect('dbidmmopr', passwd, 'momdb')
    db = cx_Oracle.connect('idmmopr', 'ykRwj_b6', 'idmmdb2')
    cur = db.cursor()
    return db, cur

class SuperFormatter(string.Formatter):
    def format_field(self, value, spec):
        if spec == 'call':
            return value()
        elif spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(item=item) for item in value])
        elif spec.startswith('if'):
            return (value and spec.partition(':')[-1]) or ''
        else:
            return super(SuperFormatter, self).format_field(value, spec)
html_head='''
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>idmm检查</title>
    <style>
        table
        {
            border-collapse: collapse;
            border-spacing: 0;
            border-left: 1px solid #252388;
            border-top: 1px solid #252388;
            background: #FFFFFF;
            margin-left: 20px;
            margin-top: 5px;
            margin-bottom: 20px;
        }

        th, td
        {
            border-right: 1px solid #252388;
            border-bottom: 1px solid #252388;
            padding: 5px 15px;
        }

        th
        {
            font-weight: bold;
            background: #DCF4EF;
            column-width: 60px;
        }

        .td
        {
            align-content: center;
        }
    </style>
</head>
<body>
'''

#遍历主机列表逐个远程执行命令并输出结果到dict中， host 为key
def cmds(cmd):
    result = {}
    for host in file('host.txt'):
        host = host.strip()
        if host.startswith('#'):
            result[host[1:]] = commands.getoutput(cmd)
        else:
            result[host] = commands.getoutput('ssh %s %s' % (host, cmd))
    return result

#远程执行主机信息采集脚本， 输出html
def hostinfo(fn):
    check_date = time.strftime('%Y%m%d')
    basedir = '/idmm/idmm3/monitor/hstate'
    # 主机资源信息
    fn.write( '''
            <label for="male">&sect;主机资源信息：</label>
            <table>
                    <tr>
                        <th style="width: 60px;"><span>省分</span></th>
                        <th style="width: 100px;"><span>主机ip</span></th>
                        <th style="width: 100px;"><span>内存使用率</span></th>
                        <th style="width: 100px;"><span>CPU使用率</span></th>
                        <th style="width: 100px;"><span>磁盘使用率</span></th>
                        <th style="width: 60px;"><span>连接数</span></th>
                        <th style="width: 60px;"><span>进程</span></th>
                        <th style="width: 60px;"><span>采集时间</span></th>
                    </tr>
            ''')
    info = cmds("PYTHONPATH=/idmm/idmm3/monitor/pylib/lib64/python2.6/site-packages /usr/bin/python /idmm/idmm3/monitor/host_day_check.py")
    for ip, ii in info.items():
        o = json.loads(ii, encoding='iso8859-1')
        if o['warn_flag'] == 1:
            warn_td_content = u'''<td><span style="color: red">异常 </span></td>'''
        else:
            warn_td_content = u'''<td><span>正常 </span></td>'''

        s = u'''<tr><td>四川移动</td>
                <td> %s </td><td> %s %%</td><td> %s %%</td><td> %s %%</td><td> %s </td>
                <td>%s</td>
                <td><span> %s </span></td>
            </tr>
        '''
        s = s % (ip, o['mem_rate'], o['cpu_rate'], o['io_rate'], o['host_conns'], o['processes'], o['check_time'])
        fn.write(s.encode('utf-8'))
    fn.write("</table>\n")

# 消息主题信息， 生成html
def qinfo(fn, zkaddr):
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

    fn.write( '''
        <label for="male">&sect;消息数量统计：</label> </br>
        ''')
    fn.write('''<table><tr>
                        <th style="width: 130px;"><span>BLE-ID </span></th>
                        <th style="width: 130px;"><span>地址 </span></th>
                        <th style="width: 130px;"><span>主题数量 </span></th>
                        <th style="width: 130px;"><span>处理消息数量 </span></th>
            </tr>''')
    for i, c in bleids.items():
        fn.write(" <tr><td> %s</td><td>%s</td> <td> %d </td> <td> %d </td> </tr>" %(i, bleaddr[i], c, blecounts[i]) )
        topic_count += c
    fn.write('</table>')

    topics = {}
    for l in file('topics.txt'):
        t = l.strip().split('\t')
        topics[t[0]] = t[1]
    clients = {}
    for l in file('clients.txt'):
        t = l.strip().split('\t')
        clients[t[0]] = t[1]
    # 消息数量信息
    fn.write('''
        <table>
                <tr>
                    <th style="width: 130px;"><span>BLE-ID </span></th>
                    <th style="width: 130px;"><span>消息主题 </span></th>
                    <th style="width: 130px;"><span>消费者ID </span></th>
                    <th style="width: 110px;"><span>成功量 </span></th>
                    <th style="width: 40px;"><span>积压 </span></th>
                    <th style="width: 40px;"><span>失败 </span></th>
                    <th style="width: 40px;"><span>在途 </span></th>
                    <th style="width: 130px;"><span>子系统 </span></th>
                </tr>
        ''')

    fn.write('''
                <tr>
                    <td><span style="color: blue">共计</span></td>
                    <td><span style="color: blue">''' + str(topic_count) + ''' </span></td>
                    <td><span style="color: blue">/</span></td>
                    <td><span style="color: blue">''' + str(succ_count) + '''</span></td>
                    <td><span style="color: blue">''' + str(sz) + '''</span></td>
                    <td><span style="color: red">''' + str(err_count) + '''</span></td>
                    <td><span style="color: blue">''' + str(sending) + '''</span></td>
                    <td><span style="color: blue">/</span></td>
                </tr>
        ''')

    for q in qlist:
        client = clients.get(q.client, " unknown" )
        topic = topics.get(q.topic, "unknown")
        s = u'''
                <tr>
                    <td>%s</td><td>%s(%s)</td> <td>%s</td><td>%s</td><td>%s</td>
                    <td><span style="color: red">%s</span></td><td>%s</td> <td>%s</td>
                </tr>
            ''' %(q.bleid, q.topic, topic.decode('utf-8'), q.client, q.total, q.size, q.err,q.sending, client.decode('utf-8'))
        fn.write(s.encode('utf-8'))

    fn.write('</table>\n')

def nodeinfo(fn, zkaddr):
    fn.write( '''
        <label for="male">&sect;IDMM节点信息：</label> </br>
        ''')
    fn.write('''<table><tr>
                <th style="width: 100px;"><span>类别</span></th>
                <th style="width: 200px;"><span>地址 </span></th>
                <th style="width: 200px;"><span>启动时间</span></th>
            </tr>''')
    info = ble.getnodeinfo(zkaddr)
    for i in info['ble']:
        v = i.split(",")
        fn.write(" <tr><td>BLE</td><td>%s</td> <td>%s</td> </tr>" %(v[0], v[1]) )
    for i in info['broker']:
        v = i.split(",")
        fn.write(" <tr><td>broker</td><td>%s</td> <td>%s</td></tr>" %(v[0], v[1]) )
    for i in info['httpbroker']:
        fn.write(" <tr><td>httpbroker</td><td>%s</td> <td> </td> </tr>" %(i, ) )
    fn.write('</table>')

def tsinfo(fn):
    fn.write( '''
        <label for="male">&sect;Oracle表空间统计：</label>
        ''')

    # 消息数量信息
    fn.write('''
        <table>
                <tr>
                    <th style="width: 110px;"><span>名称 </span></th>
                    <th style="width: 100px;"><span>使用率(%) </span></th>
                    <th style="width: 130px;"><span>可用空间(GB) </span></th>
                </tr>
        ''')
    c, cur = conndb(sysuser=True)
    cur.execute('''SELECT NVL(b.tablespace_name,nvl(a.tablespace_name,'UNKOWN')) name,
((kbytes_alloc-NVL(kbytes_free,0))/kbytes_alloc)*100   pct_used, Kbytes_free
FROM   ( SELECT   SUM(bytes)/1024 Kbytes_free
                , MAX(bytes)/1024 largest
                , tablespace_name
         FROM sys.dba_free_space
         GROUP BY tablespace_name
       ) a
     , ( SELECT   SUM(bytes)/1024 Kbytes_alloc
                , tablespace_name
         FROM sys.dba_data_files
         GROUP BY tablespace_name
       ) b
WHERE a.tablespace_name (+) = b.tablespace_name''')
    for r in cur.fetchall():
        s = u'''
                <tr>
                    <td>%s</td>
                    <td>%.02f</td><td>%.03f</td>
                </tr>
            ''' % (r[0], r[1], r[2]*1.0/1024.0/1024.0)
        fn.write(s.encode('utf-8'))
    fn.write('</table>\n')
    cur.close()
    c.close()

def logs(fn):
    stdout = sys.stdout
    sys.stdout = fn
    print( "<pre>" )
    files = cmds("ls -l /idmm/idmm3/idmm-broker[123]/log/*.debug")
    print ("\n\n======日志内容：")
    for host, line in cmds("grep -e WARN -e ERROR /idmm/idmm3/idmm-broker[123]/log/*.debug|grep -v 'try next'").items():
        print ("\n\n----%s\n" % host)
        print (files[host])
        print (line)

    print ("</pre>")
    sys.stdout = stdout

def qid(fn, id):
    stdout = sys.stdout
    sys.stdout = fn
    print( "<pre>" )

    db, cur=conndb()
    sys.stderr.write( '---%s\n' % id )
    ii = id.split("::")

    print( '--index:')
    sql="select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, commit_time-create_time, consumer_resend from msgidx_part_%s where idmm_msg_id=:v" %ii[-2]
    cur.execute(sql, (id, ))
    for row in cur.fetchall():
        print( row)

    print( '--error:')
    sql="select idmm_msg_id, dst_cli_id,dst_topic_id, create_time, consumer_resend from msgidx_part_err where idmm_msg_id=:v" 
    cur.execute(sql, (id, ))
    for     row in cur.fetchall():
        print( row)

    print( '--body:' )
    sql="select id, properties, content from messagestore_%s where id=:v" %ii[-1]
    cur.execute(sql, (id, ))
    row = cur.fetchone()
    if row is not None:
        prop = json.loads(row[1])
        content = row[2].read()
        if prop.has_key('compress'):
            file('content.gz', 'w').write(content)
            content = '[[compressed]] content.gz'
        print( row[0], row[1], content )

    db.close()
    print ("</pre>")
    sys.stdout = stdout

#从数据库获取消息积压数
def qinfo_db(fn):
    fn.write('''
           <label for="male">&sect;消息积压情况统计（来自数据库）：</label> </br>
           ''')
    db, cur = conndb()
    remains = {}
    for i in range(200):
        table = 'msgidx_part_%d' % i
        sql = "select dst_cli_id, dst_topic_id, count(*) from %s where commit_time=0 group by dst_cli_id, dst_topic_id" % ( table)
        #print (sql)
        cur.execute(sql)
        while True:
            r = cur.fetchone()
            if r is None:
                break
            tp = r[0] + '.' + r[1]
            remains[tp] = remains.get(tp, 0) + int(r[2])
    db.close()

    topics = {}
    for l in file('topics.txt'):
        t = l.strip().split('\t')
        topics[t[0]] = t[1]
    clients = {}
    for l in file('clients.txt'):
        t = l.strip().split('\t')
        clients[t[0]] = t[1]

    fn.write('''
        <table>
                <tr>
                    <th style="width: 300px;"><span>消息主题 </span></th>
                    <th style="width: 300px;"><span>消费者ID </span></th>
                    <th style="width: 40px;"><span>积压 </span></th>
                </tr>
        ''')
    for tp, ct in remains.items():
        cid, tid = tp.split(".")
        client = clients.get(cid, " unknown" )
        topic = topics.get(tid, "unknown")
        s = u'''
                <tr>
                    <td>%s(%s)</td><td>%s(%s)</td> <td>%d</td>
                </tr>
            ''' %(tid, topic.decode('utf-8'), cid, client.decode('utf-8'), ct)
        fn.write(s.encode('utf-8'))

    fn.write('</table>\n')

def total(fn, qdate):
    db, cur = conndb()
    if qdate == 'today':
        qdate = time.strftime("%Y%m%d")

    btime = int(time.mktime(time.strptime(qdate + "000000", "%Y%m%d%H%M%S"))) * 1000
    etime = int(time.mktime(time.strptime(qdate + "235959", "%Y%m%d%H%M%S"))) * 1000

    ct = {}
    for i in range(200):
        sql="""select TO_CHAR(create_time / (1000 * 60 * 60 * 24) + TO_DATE('19700101080000', 'YYYYMMDDHH24MISS'), 'YYYYMMDDHH24') as ctime, count(*)
         from msgidx_part_%d m where m.create_time between :v1 and :v2
         group by TO_CHAR(create_time / (1000 * 60 * 60 * 24) + TO_DATE('19700101080000', 'YYYYMMDDHH24MISS'), 'YYYYMMDDHH24')""" %(i, )
        cur.execute(sql, (btime, etime ) )
        while True:
            row = cur.fetchone()
            if row is None:
                break
            hour, c = row[0], row[1]
            ct[hour] = ct.get(hour, 0) + c
    db.close()

    tt = [(h, c) for h, c in ct.items()]
    tt = sorted(tt, key=operator.itemgetter(0))
    fn.write("<pre>")
    for t in tt: fn.write( "%s\t%d\n" %(t[0], t[1]) )
    fn.write("</pre>")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'db': # 获取目标主题和消费者 id的字典
        db, cur = conndb()
        cur.execute("select CLIENT_ID, SUB_SYSTEM from CLIENT_BASE_INFO_4 where use_status='1'")
        f = file("clients.txt", 'w')
        while True:
            r = cur.fetchone()
            if r is None:
                break
            #print r[1].decode('gbk')
            s = '%s\t%s\n' % (r[0], r[1].decode("gbk"))
            f.write(s.encode('utf-8'))
        f.close()

        cur.execute("select dest_topic_id, dest_topic_desc from dest_topic_info_4 where use_status='1'")
        f = file("topics.txt", 'w')
        while True:
            r = cur.fetchone()
            if r is None:
                break
            #print r[1].decode('gbk')
            s = '%s\t%s\n' % (r[0], r[1].decode("gbk"))
            f.write(s.encode('utf-8'))
        f.close()

        db.close()

import bobo
from cStringIO import StringIO
@bobo.query('/')
def hello(name="qinfo", qdate='today', id=''):
    #zkaddr = '10.113.161.103:8671,10.113.161.104:8671,10.113.161.105:8671,10.105.92.50:8671,10.105.92.51:8671' # fuqing
    #zkaddr = '10.113.172.56:8671,10.113.172.57:8671,10.113.172.58:8671,10.112.185.2:8671,10.112.185.3:8671' # xiqu
    zkaddr = '172.21.0.46:3181'
    fn = StringIO()
    fn.write(html_head)
    if name == 'hostinfo':
        hostinfo(fn)
    elif name == 'qinfo':
        qinfo(fn, zkaddr)
    elif name == 'tsinfo':
        tsinfo(fn)
    elif name == 'nodeinfo':
        nodeinfo(fn, zkaddr)
    elif name == 'logs':
        logs(fn)
    elif name == 'qinfo_db':
        qinfo_db(fn)
    elif name == 'total':
        total(fn, qdate)
    elif name == 'qid':
        qid(fn, id)
    elif name == 'all':
        hostinfo(fn)
        tsinfo(fn)
        qinfo(fn, zkaddr)
    fn.write('</body></html>')
    return fn.getvalue()

if __name__ == '__main__':
    main()
