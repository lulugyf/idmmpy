#coding=utf-8

# 端到端 监控采集， 监控两个主题的积压数量：
#    T109SmspGWDest   宽带局拆业务
#    T109SmspDest     信控停开机和局拆业务
# 5分钟采集一次
# p2pmon.sh
# . ${HOME}/.bash_profile
# cd ${HOME}/idmm3/py
# python p2pmon.py >>../log/p2pmon.log 2>&1 &
#
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * sh /idmm/idmm3/py/p2pmon.sh >/idmm/idmm3/log/p2pmon_cron.log 2>&1

import ble

def mon():
    from local_db import conf_zk_addr, conndb
    #zkaddr = '172.21.0.46:3181'
    zkaddr = conf_zk_addr()
    qlist = ble.listQ(zkaddr)
    db, cur = conndb("ibnms/ykRwj!b6@yfsdb")
    try:
        for q in qlist:
            if ( q.topic.startswith("T109SmspGWDest") or q.topic.startswith("T109SmspDest") ) and q.total>0:
                cur.execute("insert into overstock_moni(data_time, point_name, overstock_num) values(sysdate, :v1, :v2)",
                            ("IDMM-%s"%q.topic, q.size))
                db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    mon()
