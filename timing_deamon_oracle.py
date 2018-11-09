#-*- coding: utf-8 -*-

import cx_Oracle
from time import strftime,localtime
import os, string, time, datetime
import json
import urllib
import random
import ConfigParser
from kazoo import client

'''
    定时消息守护进程。从timing_message表中获取消息，后台发送至ble
'''

cfile = "/idmm/idmm3/idmm-manager/config/Config-oracle.cfg"

def readStrValue(configFile,section,key):
    cf=ConfigParser.ConfigParser()
    cf.read(configFile)
    return str(cf.get(section, key))


def getBleAddrById(bleid): 
    addr=''
    
    try:
        zkUrl=readStrValue(cfile,'zk','url')
        zkPath=readStrValue(cfile,'zk','blePath')      
        zk = client.KazooClient(hosts='%s' %zkUrl)
        zk.start()
        zk_list = zk.get_children('%s' %zkPath)
        if len(zk_list) > 0:
            blePath = zkPath + '/id.'+ bleid
            data,stat = zk.get('%s' %blePath)
            ip=data.split(" ")[0].split(":")[0]
            port=data.split(" ")[1].split(":")[1]
            addr="%s:%s"%(ip,port)
            
        zk.stop()
        return addr
    except Exception,e:
        print 'getBleList Error: %s' %(e)


def sendtoBLE(addr, msgid, subid, topic, groupid, priority):  
    url='http://%s/jolokia/exec/com.sitech.crmpd.idmm.ble.RunTime:name=runTime/send/%s/%s/%s/%s/%s' %(addr, msgid, subid, topic, groupid, priority)
    url_rtn=urllib.urlopen(url)
    if url_rtn.getcode()!=200:
        print 'resend error!'
        return -1
    else:
        print 'resend %s succ!' %msgid
        return 0

if __name__ == '__main__':
    try:
        db=cx_Oracle.connect('idmmopr','ykRwj_b6','10.113.181.128:1521/idmmdb')
        cur=db.cursor()
        
        #计算昨天0时0分毫秒数
        #yesterday=datetime.date.today() - datetime.timedelta(days=1)
        #datefmt='%s 00:00:00' %yesterday
        #begin=time.mktime(time.strptime(datefmt,'%Y-%m-%d %H:%M:%S') ) 

        while True:            
            #计算当前毫秒数
            now=datetime.datetime.now()
            nowfmt=now.strftime('%Y-%m-%d %H:%M:%S')
            nowms=time.mktime(time.strptime(nowfmt,'%Y-%m-%d %H:%M:%S'))*1000
            
            sql="select idmm_msg_id from timing_message where create_time+req_time*1000<=%ld and status='0' and  rownum <= 100  order by create_time " %nowms
            print 'sql[%s]' %sql
            cur.execute(sql)
            for msgid in cur.fetchall():
                print msgid[0]
                store=str(msgid[0]).split('::')[-1]
                idx=str(msgid[0]).split('::')[-2]
                
                storetable='messagestore_%s' %(store)
                sql="select properties from %s where id='%s'" %(storetable, str(msgid[0]))
                cur.execute(sql)
                properties=cur.fetchone()
                #print 'properties=%s' %properties
                dict_p = json.loads(properties[0])
                
                msgid = dict_p['message-id']
                src_topic = dict_p['topic']
                
                #根据topic查目标主题，BLE_ID
                sql="select dest_topic_id,BLE_id from ble_dest_topic_rel_1 where dest_topic_id in (select dest_topic_id from topic_mapping_rel_1 where src_topic_id='%s')" %src_topic
                cur.execute(sql)
                for result in cur.fetchall():
                    dest_topic_id=result[0]
                    bleid=result[1]
                    #根据bleid查询zk上对应ble地址
                    addr=getBleAddrById(bleid)
                    #根据topic查订阅关系
                    sql="select client_id from topic_subscribe_rel_1 where dest_topic_id='%s'" %dest_topic_id
                    cur.execute(sql)
                    for client in cur.fetchall():
                        subid=client[0]
                        ret=sendtoBLE(addr, msgid, subid, dest_topic_id, random.randint(1,100), 10)
                        if ret<0:
                            break
                    if ret==0:
                        sql="update timing_message set status='1' where idmm_msg_id='%s'" %(msgid)
                        cur.execute(sql)
                        conn.commit()
                    else:
                        conn.rollback()
                        break
            time.sleep(1)
        
        cur.close()
        conn.close()
    except Exception,e:
        print 'oracle Error: %s' %(e)



