# coding=utf-8

# 按主题 采集最近5分钟生产和消费的消息数量
# 实现方式:  1. 启动线程, 每10秒采集一次队列数据, 保存到文件中
#            2. 展示的时候, 找最新的和最接近 5分钟前保存的数据, 按主题相减得到结果

import threading
import time
import datetime
import json
import os
import operator

import ble

__interval = 10  #  seconds
__timedelta = datetime.timedelta(seconds=5*60)  # 5 minutes ago

__file_mod = []  # 按修改时间排序的文件列表, item format: (fname, st_mtime)

def ftime(ago=False):
    t = datetime.datetime.now()
    if ago:
        t = t - __timedelta
    return "%02d.%d" % (t.minute, t.second / __interval)

def __list_file(data_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    else:
        for fname in os.listdir(data_dir):
            if fname[0] == '.': continue
            fname = "%s/%s"%(data_dir, fname)
            __file_mod.append((fname, os.stat(fname).st_mtime))
        __file_mod.sort(key=operator.itemgetter(1))

# 文件名: min.(sec/10)
def mon_thread(zkaddr, data_dir):
    __list_file(data_dir)
    while True:
        time.sleep(__interval)
        try:
            qlist = ble.listQ(zkaddr)
            qdict = {"%s,%s"%(q.topic, q.client) : (q.total, q.size) for q in qlist}
            fname = "%s/%s" % (data_dir, ftime())
            f = open(fname, "w")
            json.dump(qdict, f)
            f.close()
            __file_mod.append((fname, os.stat(fname).st_mtime))

            if len(__file_mod) > __timedelta.seconds/__interval:
                del __file_mod[0]
        except Exception,e:
            print(e)

#反向寻找更新时间的文件， 寻找最接近且小于 __timedelta 的文件
def find_last():
    tmin = time.time() - __timedelta.seconds
    fname = None
    #print '=== ', len(__file_mod)
    for i in range(len(__file_mod)-1, 0, -1):
        fm = __file_mod[i]
        #print '----', fm[0], fm[1], tmin, fm[1]-tmin, __timedelta.seconds
        if fm[1] < tmin:
            break
        fname = fm[0]
    return fname

def start_mon(zkaddr, data_dir):
    th = threading.Thread(target=mon_thread, args=(zkaddr, data_dir))
    th.daemon = True
    th.start()

# return { "topic,client": (produce, consume), ...}
def get_mon(qlist):
    #print("-------get_mon")
    fname = find_last()
    if fname is None:
        print("find_last() return None")
        return
    with open(fname) as f:
        q1 = json.load(f)
    # print("size of q1 = ", len(q1), len(qlist), repr(q1))
    for q in qlist:
        # if q.topic != "TDst2":
        #     continue
        # q.status="hahah "+q.status
        k = "%s,%s" % (q.topic, q.client)
        #print(k)
        if not q1.has_key(k):
            print("not found %s" % k)
            # print(repr(q1))
            continue
        t = q1[k]
        q.m5_prod = q.total - t[0]
        q.m5_cons = q.m5_prod - (q.size-t[1])
        #print q.total, t[0], q.size, t[1]

if __name__ == '__main__':
    qlist = ble.listQ("172.21.0.46:3181")
    __list_file("minutes")
    get_mon(qlist)
