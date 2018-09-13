#coding=utf-8

# 产生html page的页面

# 产生table
def gentable(title, header, rows, out):
    out.write("<h1> &sect; %s </h1>\n"%title)
    out.write("<table><tr>\n")
    for h in header: out.write(" <th>%s</th>"%h)
    out.write("</tr>\n")
    for r in rows:
        out.write(" <tr>")
        for f in r:
            out.write(" <td>%s</td>"%f)
        out.write(" </tr>\n")
    out.write("</table>")

def page_head(title, out):
    out.write("<html><header><meta charset=\"utf-8\"><title>%s</title>"%title)
    out.write("""    <style>
        table
        {
            border-collapse: collapse;
            border-spacing: 0;
            border-left: 1px solid #252388;
            border-top: 1px solid #252388;
            background: #FFFFFF;
            margin-left: 20px;
            margin-top: 5px;
            margin-bottom: 20px;
        }

        th, td
        {
            border-right: 1px solid #252388;
            border-bottom: 1px solid #252388;
            padding: 5px 15px;
        }

        th
        {
            font-weight: bold;
            background: #DCF4EF;
            column-width: 60px;
        }

        .td
        {
            align-content: center;
        }
    </style>""")
    out.write("</head><body>\n")

def page_tail(out):
    out.write("\n</body></html>")

'''
# 生成统计数据的html页面  python -c "import pagegen as g; g.mon_page('aa.html')"
from local_db import conf_zk_addr
from db import stastics, getTopicsConf
from zk import ZKCli
import os
def mon_page(fname):
    os.putenv('NLS_LANG', 'American_America.zhs16gbk')
    zcli = ZKCli(conf_zk_addr())
    zcli.start()
    # zcli.wait()
    ver_node = zcli.get('/idmm/configServer/version')
    zcli.close()
    ver = str(ver_node[0])
    print "conf version", ver, repr(ver_node)
    topics = getTopicsConf(ver)

    # 调用统计sql
    title, st_date, header, rows = stastics(-1, topics)

    # 统计按bleid的消息总量
    blecounts = {}
    for r in rows:
        bleid, count = r[-2], r[1]
        blecounts[bleid] = blecounts.get(bleid, 0) + count

    f = open(fname, "w")
    page_head("IDMM日统计", f)
    gentable(title, header, rows, f)

    gentable("按bleid的消息量统计", ["bleid", "count"], [(k, v) for k, v in blecounts.items()], f)
    page_tail(f)
    f.close()
'''