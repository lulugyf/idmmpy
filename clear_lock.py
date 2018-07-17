

import json
import urllib2
import time
from idmm import DMMClient


def timetostamp(a):
    a = '2018-04-18 12:00:00'
    print time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S'))

    1524024000

def filter_no():
    nos = { ph.strip():1 for ph in open('1') }
    f = open('2', 'w')
    for l in open('201803.txt'):
        v = l.split('|')
        if len(v) <10: continue
        if nos.has_key(v[1]): f.write(l)
    f.close()

def getids():
    jmxaddr = '10.113.182.96:21151'
    client_id = 'Sub103Sreq'
    topic_id = 'T101SreqDest-B'
    url = 'http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/lockdetail/%s/%s'%(
        jmxaddr, client_id, topic_id)
    #url = 'http://10.113.182.96:21151/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/lockdetail/Sub103Sreq/T101SreqDest-B'
    s = urllib2.urlopen(url)
    o = json.load(s)
    o1 = json.loads(o['value'])
    return [ v['msgid'] for v in  o1['messages'] ]

def commit__(c, topic, cli, msgids):
    for msgid in msgids:
        print 'commit', msgid
        print c.fetch_commit(topic, cli, msgid)

if __name__ == '__main__':
    c = DMMClient('10.113.182.98:22311')
    s_topic, s_cli, d_topic, d_cli = "TrechargeBusiness-A", "PubPayment", "T101SreqDest-B", "Sub103Sreq"
    t1 = time.time()
    #send(c, s_topic, s_cli)

    while True:
        ids = getids()
        if len(ids) > 0:
            commit__(c, d_topic, d_cli, ids)
        else:
            print "nothing todo"
            time.sleep(1.0)

if __name__ == '__main__':
    getids()

