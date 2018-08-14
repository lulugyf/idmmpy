import time
from idmm import DMMClient

def fetch_limit(c, topic, cli, n=-1):
    print "  === fetch_limit", topic, cli, n
    #while True:
    for i in range(n):
        msgid, content = c.fetch(topic, cli)
        if msgid == 0:
            print 'no more message'
            break
        elif msgid is not None:
            #print '======got', msgid,   # content
            c.fetch_commit(topic, cli, msgid)
            #c.fetch_commit(topic, cli, msgid)
        else:
            print 'failed'
            time.sleep(0.04)
            #break

def fetch(c, topic, cli):
    while True:
        msgid, content = c.fetch(topic, cli)
        if msgid == 0:
            print 'no more message'
            break
        elif msgid is not None:
            print '======got', msgid, content
            c.fetch_commit(topic, cli, msgid)
            #c.fetch_commit(topic, cli, msgid)
        else:
            print 'failed'
            break

def consume_all(c, fname):
    for l in open(fname, "r"):
        k = l.split()
        if len(k) < 5: continue
        topic = k[0][1:-1]
        cli = k[1].strip()
        fetch(c, topic, cli)

from zk import get_rand_httpaddr
from local_db import conf_zk_addr

# python ble.py |awk '{if($4>0)print $0}'

if __name__ == '__main__':
    broker_addr = get_rand_httpaddr(conf_zk_addr())
    print "----httpbroker:", broker_addr
    n = 208344
    c = DMMClient(broker_addr)
    #fetch_limit(c, 'TRecQryCnttDest-B', 'Sub111Cntt', n)
    #fetch_limit(c, 'TRecQryCnttDest-B', 'Sub119', n)
    #fetch_limit(c, 'T101OrderStateSynDest-B', 'Sub103', n)
    #fetch_limit(c, 'TRecOprCnttDest-A', 'Sub119Opr', n)

    fetch_limit(c, 'T101OrderStateSynDest-A', 'Sub103', n)
    print "done!"
