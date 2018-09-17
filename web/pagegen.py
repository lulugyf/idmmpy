#coding=utf-8

# 产生html page的页面

import time

# 产生table
def gentable(title, header, rows, out):
    out.write("<h1> &sect; %s </h1>\n"%title)
    out.write("<table>\n")
    if type(header) == str:
        out.write(header)
    else:
        out.write("<tr>")
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
    out.write('<a href="/">返回首页</a></br>\n')

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

def loginpage():
    return """<html><head><meta charset=\"utf-8\"><title>kill proc confirm</title></head><body>
    <form method="POST" name="auth" action="/killall" >
    pass code: <input type="password" name="pass" /> </br>
    <input type="submit" value="submit" />
    </form>
    </body></html>"""

def getmsgpage():
    return """<html><head><meta charset=\"utf-8\"><title>input some properties</title></head><body>
    <h1>提取消息内容数据:</h1>
    <form method="POST" name="getmsg" action="/getmsg" target="_blank" >
    <table>
    <tr><td>目标主题: </td><td><input name="topic" size="60"/> </td></tr>
    <tr><td>消费者id: </td><td><input name="client" size="40" /> </br></td></tr>
    <tr><td>开始时间: </td><td><input name="begin_time" value="{0}" /> or 最近<input name="recent_min" size="6" />分钟 
       </br> <font color="red">格式: yyyy-mm-dd HH:MM:SS</font></br></td></tr>
    <tr><td>结束时间: </td><td><input name="end_time" /> <font color="red">留空为到当前时间, 格式同上</font> </br></td></tr>
    <tr><td>消息状态: </td><td><select name="msgstatus">
    <option value="2">未消费</option><option value="1">全部</option><option value="3">已消费</option></select> </br></td></tr>
    <tr><td>号码正则表达式: </td><td><textarea name="patterns" cols="40" rows="5">,\"PHONE_NO\":\"([\\d]+)\",
,\"ServiceNo\":\"([\\d]+)\",</textarea>
      </br><font color="red">在消息content中提取号码的正则表达式, </br>
      每行一个, 依次尝试</font> </br></td></tr>

    <tr><td colspan="2"><input type="submit" value="submit" /></td></tr>
    </table>
    </form>
    </body></html>""".format(time.strftime("%Y-%m-%d %H:%M:%S"), )

def qryid_form():
    return '''<h1>&sect; 消息查询：</h1> </br>
        <form method="POST" name="query">
        <label>消息ID: </label> <input type="text" name="id" size="70" /> <br />
        <input type="submit" value="查询" />
        </form>'''