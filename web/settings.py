
host_list__si = [
 {"ipaddr":"172.21.0.46", "user":"crmpdscm", "diskpath":["/crmpdscm", "/crmpdscmweb"], "deploypath":["/crmpdscm/idmm3/broker0"], "lsof":"/usr/sbin/lsof"},
 {"ipaddr":"172.21.11.131", "user":"idmm", "diskpath":["/idmm" ], "deploypath":["/idmm/idmm3/broker0"], "lsof":"/idmm/lsof"}
]

host_list = [
 {"ipaddr":"10.113.182.96", "user":"idmm", "diskpath":["/idmm"], "deploypath":["/idmm/idmm3/idmm-broker%d"%i for i in (1,2,3,4)], "lsof":"/usr/sbin/lsof"},
 {"ipaddr":"10.113.182.97", "user":"idmm", "diskpath":["/idmm"], "deploypath":["/idmm/idmm3/idmm-broker%d"%i for i in (1,2,3)], "lsof":"/usr/sbin/lsof"},
 {"ipaddr": "10.113.182.98", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
 {"ipaddr": "10.113.182.99", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
 {"ipaddr": "10.113.182.100", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
 {"ipaddr": "10.113.182.101", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
]

host_list__fq = [
 {"ipaddr":"10.113.181.86", "user":"idmm", "diskpath":["/idmm"], "deploypath":["/idmm/idmm3/idmm-broker%d"%i for i in (1,2,3,4)], "lsof":"/usr/sbin/lsof"},
 {"ipaddr":"10.113.181.87", "user":"idmm", "diskpath":["/idmm"], "deploypath":["/idmm/idmm3/idmm-broker%d"%i for i in (1,2,3)], "lsof":"/usr/sbin/lsof"},
 {"ipaddr": "10.113.181.88", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
 {"ipaddr": "10.113.181.89", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
 {"ipaddr": "10.113.181.90", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
 {"ipaddr": "10.113.181.91", "user": "idmm", "diskpath": ["/idmm"],
  "deploypath": ["/idmm/idmm3/idmm-broker%d" % i for i in (1, 2, 3)], "lsof": "/usr/sbin/lsof"},
]

zookeeper = "10.113.172.56:8671,10.113.172.57:8671,10.113.172.58:8671,10.112.185.2:8671,10.112.185.3:8671"
zookeeper__fq = "10.113.161.103:8671,10.113.161.104:8671,10.113.161.105:8671,10.105.92.50:8671,10.105.92.51:8671"
zookeeper__si = "172.21.0.46:3181"
index_table_count = 200
minutes_data_dir = "minutes"
statics_data_dir = "statics"
log_timeout_dir = "timeoutlog"

database_tbs_file = "/idmm/idmm3/log/tbs.log"

