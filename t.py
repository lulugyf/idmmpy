from idmm import DMMClient
import random
import time


def send(c, topic, cli):
    for i in range(10):
        msgid = c.send(topic, cli, u'after', random.randint(4, 9), "group-%d"%random.randint(1, 4))
        if msgid is None:
            return False
        print 'send return message id=%s' %msgid
        c.send_commit(topic, cli, msgid)

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

if __name__ == '__main__':
    #c = DMMClient('10.113.182.100:22313')
    c = DMMClient('10.113.182.99:9924')
    #pubt,pubid,subt,subid = 'TSrc2', 'Pub2', 'TDst2', 'Sub2'
    #pubt,pubid,subt,subid = 'Test02-A', 'Pubtest', 'Test02Dest-A', 'Subtest'
    #pubt,pubid,subt,subid = 'T105DataBatchSyn-A', 'Pub105', 'T105DataBatchSynDest-A', 'Sub113DataBatchSyn'
    pubt,pubid,subt,subid = 'T109BusiOrderDeadC-B', 'Pub109', 'T109BusiOrderDeadCDest-B', 'Sub104'
    send(c, pubt, pubid)
    fetch(c, subt, subid)
    #for line in open("m1"):
    #    v = line.split()
    #    msgid = v[0]
    #    c.send_commit(pubt, pubid, msgid)
