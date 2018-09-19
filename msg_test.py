from idmm import DMMClient
import random
import time


def send(c, topic, cli, n=10):
    for i in range(n):
        msgid = c.send(topic, cli, u'after', random.randint(4, 9), "group-%d"%random.randint(1, 4))
        if msgid is None:
            return False
        #print 'send return message id=%s' %msgid
        c.send_commit(topic, cli, msgid)

def fetch(c, topic, cli):
    n = 0
    while True:
        msgid, content = c.fetch(topic, cli)
        if msgid == 0:
            #print 'no more message'
            break
        elif msgid is not None:
            #print '======got', msgid, content
            c.fetch_commit(topic, cli, msgid)
            n += 1
        else:
            #print 'failed'
            break
    return n

from zk import get_rand_httpaddr
from local_db import conf_zk_addr

if __name__ == '__main__':
    broker_addr = get_rand_httpaddr(conf_zk_addr())
    c = DMMClient(broker_addr)

    pubt,pubid,subt,subid = 'Test01-A', 'Pubtest', 'Test01Dest-A', 'Subtest'
    test_time = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        n = 10
        t1 = time.time()
        send(c, pubt, pubid, n)
        t2 = time.time()
        n2 = fetch(c, subt, subid)
        t3 = time.time()
        print "== %s\t%d\t%.3f\t%d\t%.3f" %(test_time, n, (t2-t1)/n, n2, (t3-t2)/n2)
    except Exception,x:
        print "== %s\t FAIL: %s" % (test_time, repr(x))
