#coding=utf-8

import httplib
#from urllib.parse import urlparse
from urlparse import urlparse
import Queue
import copy
import threading
import os
import operator
import time

class MDown:
    def __init__(self, url, outfile, blocks=6, blocksize=4*1024*1024, proxy=None):
        self.url = url
        self.outfile = outfile
        self.tmpfile = outfile+".rng"  #用于保存下载状态, 文件格式：第一行整个文件的大小， 以后每一行是一个已经下载完成块的起止字节位置， 恢复的话， 需要先拼接成块， 找空缺和尾上未完成的
        self.blocks = blocks # 最大并发下载线程数
        self.blocksize = blocksize  #每一块的大小
        self.proxy = proxy
        headers = {}
        headers['Accept-Language'] = 'en-GB,en-US,en'
        headers['Accept-Encoding'] = 'gzip,deflate,sdch'
        headers['Accept-Charset'] = 'max-age=0'
        headers['Cache-Control'] = 'ISO-8859-1,utf-8,*'
        headers['Cache-Control'] = 'max-age=0'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1)'
        headers['Connection'] = 'keep-alive'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml,*/*'
        self.headers = headers

        self.lock = threading.Lock()
        self.counter = 0

    def __mkconn(self):
        if self.proxy is None:
            pp = urlparse(self.url)
            if pp.scheme == 'http':
                conn = httplib.HTTPConnection(pp.netloc)
            elif pp.scheme == 'https':
                conn = httplib.HTTPSConnection(pp.netloc)
            return conn, pp.path
        else:
            conn = httplib.HTTPConnection(self.proxy)
            return conn, self.url

    def __add_counter(self, n):
        self.lock.acquire()
        self.counter += n
        self.lock.release()
    def __checksupport(self):
        # pp = urlparse(self.url)
        # if pp.scheme == 'http':
        #     conn = httplib.HTTPConnection(pp.netloc)
        # elif pp.scheme == 'https':
        #     conn = httplib.HTTPSConnection(pp.netloc)
        conn, path = self.__mkconn()
        headers = copy.deepcopy(self.headers)
        headers['Range'] = 'bytes=0-299'
        conn.request("GET", path, headers = headers)  # ={'Range': 'bytes=0-299'})  # <----
        resp = conn.getresponse()
        #print resp.status
        if resp.status == httplib.PARTIAL_CONTENT:
            # supported,   'bytes 0-299/612'
            crange = resp.getheader('content-range')
            print "supported", crange
            self.content_len = int(crange.split("/")[1])
            resp.read()
            conn.close()
            return 1
        elif resp.status == httplib.OK:
            print "not support bytes-range, but can download, down it all once..."
            with open(self.outfile, "wb") as fout:
                while True:
                    content = resp.read(4096)
                    if len(content) > 0:
                        fout.write(content)
                        self.__add_counter(len(content))
                    else:
                        break
            conn.close()
            return 0
        else:
            print "failed", resp.status
            return -1
    def __down_one(self, rangeQ, thid, tmpFileQ):
        headers = copy.deepcopy(self.headers)
        conn, path = self.__mkconn()
        while True:
            try:
                rng = rangeQ.get_nowait()
            except Queue.Empty,x:
                break
            rng_str = "%d-%d"%(rng[0], rng[1])
            tmpfile = "%s-%s"%(self.outfile, rng_str)
            openmod = "wb"
            try:
                st = os.stat(tmpfile)
                if st.st_size == rng[1]-rng[0]+1:
                    print "thread %s: file %s ok, skip"%(thid, tmpfile)
                    tmpFileQ.put(tmpfile)
                    continue
                else:
                    _rng = rng_str
                    rng_str = "%d-%d"%(rng[0]+st.st_size, rng[1])
                    openmod = "ab"
                    print "------ %s => %s" %( _rng, rng_str )
                self.__add_counter(st.st_size)
            except:
                pass
            headers['Range'] = 'bytes=%s'%rng_str
            print "thread %s begin %s"%(thid, rng_str)
            conn.request("GET", path, headers=headers)  # ={'Range': 'bytes=0-299'})  # <----
            resp = conn.getresponse()
            if resp.status == httplib.PARTIAL_CONTENT:
                with open(tmpfile, openmod) as fout:
                    while True:
                        content = resp.read(4096)
                        if len(content) > 0:
                            fout.write(content)
                            fout.flush()
                            self.__add_counter(len(content))
                        else:
                            break
                print "thread %s down %s done" % (thid, rng_str)
                tmpFileQ.put(tmpfile)
            else:
                print "thread %s failed %s"%(thid, resp.status)
        conn.close()
        print "----thread %s done!" % thid

    def __merge_parts(self, tmpFileQ):
        # 合并文件
        lst = [tmpFileQ.get() for i in range(tmpFileQ.qsize())]
        lst1 = [(i, int(i.split("-")[-2]) )for i in lst]
        lst1.sort(key=operator.itemgetter(1))
        with open(self.outfile, "wb") as fout:
            for tmpfile in lst1:
                with open(tmpfile[0], "rb") as fin:
                    while True:
                        c = fin.read(4096)
                        if c == '': break
                        fout.write(c)
                os.remove(tmpfile[0])
        print "merge file done!"

    def start(self):
        ret = self.__checksupport()
        if ret == 0:
            return  # download completed
        elif ret < 0:
            return # failed
        clen = self.content_len
        if clen <= 0:
            print "invalid content_len", clen
            return
        xe = 0
        blocksize = self.blocksize
        rangeQ = Queue.Queue()
        tmpFileQ = Queue.Queue()
        while xe < clen:
            if xe + blocksize + 1 >= clen:
                rangeQ.put( (xe, clen-1) )
                break
            else:
                rangeQ.put( (xe, xe+blocksize-1) )
                xe += blocksize
        pcount = self.blocks
        if pcount > rangeQ.qsize():
            pcount = rangeQ.qsize()
        ths = []
        for i in range(pcount):
            th = threading.Thread(target=self.__down_one, args=(rangeQ, str(i), tmpFileQ))
            th.setDaemon(True)
            th.start()
            ths.append(th)

        # print speed
        c = self.counter
        secs = 2.0
        while True:
            c1 = self.counter
            if c1 >= self.content_len:
                break
            s = (c1-c)/secs
            if s > 0:
                tm = (self.content_len-c1 )/s/60.0
            else:
                tm = -1.0
            print "\rspeed %.3f kb/s %.2f%% of %.3fMB need time: %.2f Min" %( s/1024,
                                        c1*100.0/self.content_len, self.content_len/1024.0/1024.0,
                            tm  )
            c = c1
            time.sleep(secs)
        for th in ths:
            th.join()
        print 'all parts downloads done!'
        self.__merge_parts(tmpFileQ)



def __test():
    # https://stackoverflow.com/questions/21775860/python-how-to-download-file-using-range-of-bytes
    url = "http://172.21.0.46:9191/v3.0.3/assembly/target/broker-201810160207-release.zip"
    headers = {}
    headers['Accept-Language'] = 'en-GB,en-US,en'
    headers['Accept-Encoding'] = 'gzip,deflate,sdch'
    headers['Accept-Charset'] = 'max-age=0'
    headers['Cache-Control'] = 'ISO-8859-1,utf-8,*'
    headers['Cache-Control'] = 'max-age=0'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1)'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml,*/*'
    headers['Range'] = 'bytes=0-299'

    pp = urlparse(url)
    if pp.scheme == 'http':
        conn = httplib.HTTPConnection(pp.netloc)
    elif pp.scheme == 'https':
        conn = httplib.HTTPSConnection(pp.netloc)
    conn.request("GET", pp.path, headers=headers) # ={'Range': 'bytes=0-299'})  # <----
    resp = conn.getresponse()
    print resp.status

    print resp.status == httplib.PARTIAL_CONTENT

    print resp.getheader('content-range') #  'bytes 0-299/612'
    content = resp.read()
    print len(content)

def __test1():
    url = "https://stanfordnlp.github.io/CoreNLP/download.html"
    conn = httplib.HTTPConnection("172.22.0.23:8989")
    conn.request("GET", url)
    resp = conn.getresponse()
    print resp.status
    with open("a.html", "wb") as f:
        f.write(resp.read())
    conn.close()

if __name__ == '__main__':
    # url = "http://172.21.0.46:9191/v3.0.3/assembly/target/broker-201810160207-release.zip"
    # m = MDown(url, "a.zip")
    # m.start()
    url = "https://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-10-05-models.jar"
    m = MDown(url, "a.jar", proxy="172.22.0.23:8989")
    m.start()

    #__test1()
