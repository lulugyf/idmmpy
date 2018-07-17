import pycurl
from cStringIO import StringIO
import json
import random

class DMMClient:
    def __init__(self, addr):
        self.c = pycurl.Curl()
        self.send_url = 'http://%s/SEND'%addr
        self.send_commit_url = 'http://%s/SEND_COMMIT'%addr
        self.fetch_url = 'http://%s/PULL'%addr
        self.tenant_id = 'gyf'
    
    def post(self, url, data, headers=None):
        c = self.c
        storage = StringIO()
        c.setopt(pycurl.URL, url)
        if headers is not None:
            c.setopt(pycurl.HTTPHEADER, headers)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, json.dumps(data))
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        j = json.loads(storage.getvalue())
        storage.close()
        return j
    
    def send(self, topic, client, content, priority=None, group=None, props={}):
        data = {"topic":topic,"client-id":client,"content":content, 'tenant-id':self.tenant_id,}
        for k, v in props.items():
            data[k] = v
        if priority is not None:
            data['priority'] = priority
        if group is not None:
            data['group'] = group
        j = self.post(self.send_url, data, ['Content-Type: text/plain; charset=GBK'])
        if j['result-code'] != 'OK':
            print 'send failed', j['result-code']
            return None
        #print j['message-id'] , content
        return j['message-id']
        
    def send_commit(self, topic, client, messageid):
        data = {"topic":topic,"client-id":client, 'tenant-id':self.tenant_id, "message-id":messageid,
                "custom.msg_route":"2", "consumer-retry": 3}
        j = self.post(self.send_commit_url, data)
        if j['result-code'] != 'OK':
            print 'send failed', j['result-code']
            return
        print 'send commit return', j['result-code']
    
    def fetch(self, topic, client, process_time=10):
        data = {'target-topic':topic,
                'client-id':client, 'tenant-id':self.tenant_id,
                'processing-time':process_time}
        j = self.post(self.fetch_url, data)
        #print '====', repr(j)
        if j['result-code'] != 'OK':
            print 'fetch failed', j['result-code']
            if j['result-code'] == 'NO_MORE_MESSAGE':
                return 0, ''
            return None, 'failed'
        msgid = j['message-id']
        content = j['content']
        print j
        return msgid, content

    def fetch_props(self, topic, client, process_time=60):
        data = {'target-topic':topic,
                'client-id':client,'tenant-id':self.tenant_id,
                'processing-time':process_time}
        j = self.post(self.fetch_url, data)
        #print '====', repr(j)
        if j['result-code'] != 'OK':
            print 'fetch failed', j['result-code']
            if j['result-code'] == 'NO_MORE_MESSAGE':
                return 0, ''
            return None, 'failed'
        #msgid = j['message-id']
        #content = j['content']
        return j


    def fetch_commit(self, topic, client, msgid, desc=None, replyto=None):
        data = {'target-topic': topic, 'client-id': client, 'tenant-id':self.tenant_id,
                'message-id': msgid,
                'pull-code': 'COMMIT'}
        if desc is not None:
            data['code-description'] = desc
        if replyto is not None:
            data['reply-to'] = replyto

        j = self.post(self.fetch_url, data)
        # print 'pull commit return', j['result-code']

    def pull(self, topic, client, process_time=60,
             msgid=None, pull_code=None, desc=None):
        data = {'target-topic':topic,
                'client-id':client, 'tenant-id':self.tenant_id,
                'processing-time':process_time}
        if msgid is not None:
            data['message-id'] = msgid
            if pull_code is None:
                pull_code = 'COMMIT_AND_NEXT'
        if pull_code in ('COMMIT', 'COMMIT_AND_NEXT',
                         'ROLLBACK', 'ROLLBACK_AND_NEXT', 'ROLLBACK_BUT_RETRY'):
            data['pull-code'] = pull_code
            if pull_code == 'ROLLBACK_BUT_RETRY':
                data['retry-after'] = '60' # after 60s and retry  
        if desc is not None:
            data['code-description'] = desc
        
        j = self.post(self.fetch_url, data)
        '''if j['result-code'] != 'OK':
            print 'fetch failed', j['result-code']
            if j['result-code'] == 'NO_MORE_MESSAGE':
                return 0, ''
            return None, 'failed'
        msgid = j['message-id']
        content = j['content']
        print j
        return msgid, content'''
        return j



def send(c, topic, cli):
    #c = DMMClient('10.149.85.32:44200')
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

def main_test():
    #s_topic, s_cli, d_topic, d_cli = "TSrc1", "Pub000", "TDst1", "Sub000"
    #c = DMMClient('172.21.0.46:3101')
    s_topic, s_cli, d_topic, d_cli = "TSrc2", "Pub2", "TDst2", "Sub2"
    c = DMMClient('172.21.0.46:1142')

    import time
    random.seed(time.time())

    for i in range(100):
        msgid = c.send(s_topic, s_cli, u'stop 13900', 100, "group%d"%random.randint(1, 20))
        if msgid is None:
            return False
        print 'send return message id=%s' %msgid
        c.send_commit(s_topic, s_cli, msgid)

    # consume
    while True:
        msgid, content = c.fetch(d_topic, d_cli)
        if msgid == 0:
            print 'no more message'
            return True
        elif msgid is not None:
            print '======got', msgid, content
            c.fetch_commit(d_topic, d_cli, msgid)
        else:
            print 'failed'
            return False


import sys
if __name__ == '__main__':
    main_test()
    # d2 = None
    # if len(sys.argv) > 1 and sys.argv[1] == '1':
    #     c = DMMClient('10.149.85.32:44100')
    #     s_topic, s_cli, d_topic, d_cli = "Topictest0", "Pub_test",  "TopictestDest0", "Sub_test0" #10000001
    # elif len(sys.argv) > 1 and sys.argv[1] == '2':
    #     c = DMMClient('10.149.85.32:44200')
    #     s_topic, s_cli, d_topic, d_cli = "TSrcTest1", "pubTest1",  "TDstTest1", "subTest1" # 10000002
    #     d2, c2 = 'TDstTest2', 'subTest2'
    # else:
    #     print "nothing"
    #     sys.exit(0)
    # s_topic, s_cli, d_topic, d_cli = "TSrcTest2", "pubTest2",  "TDstTest2", "subTest2"

    #c = DMMClient('10.113.181.86:12311')
    #s_topic, s_cli, d_topic, d_cli = "TSrcTest1", "pubTest1", "TDstTest1", "subTest1"
    #fetch(c, d_topic, d_cli)
