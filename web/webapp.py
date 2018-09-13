#coding=utf-8

import bobo
import webob
import os
import sys
sys.path.insert(0, os.getcwd())
print("--cwd: %s"%os.getcwd())
import pagegen as pg
import json
import rsh

def genResp():
    r = webob.Response()
    r.content_type = "text/html; charset=utf-8"
    return r

@bobo.query("/")
def root():
    return "hello world!"

@bobo.query("/proc")
def proc(bobo_request):
    r = genResp()
    pg.page_head("IDMM 进程信息", r)

    conf = json.load(open("conf.json"))
    hinfos = [  rsh.hostinfo(h['ipaddr'], h['user'], h['diskpath']) for h in conf ]
    pg.gentable("主机信息", ["hostname", "ipaddr", "cpu-idle", "mem-free-kb", "swap-free-kb"],
                [(h['hostname'], h['host'], h['cpu-idle'], h['mem-free-kb'], h['swap-free-kb']) for h in hinfos], r)


    pg.page_tail(r)
    return r
