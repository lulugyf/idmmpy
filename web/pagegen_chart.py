#coding=utf-8

def chart_head(title, out=None):
    s = '''<!DOCTYPE html>
<html>
  <head>
    <title>%s</title>
    <link rel="stylesheet" href="/static/bower_components/chartist/dist/chartist.min.css">
    <link rel="stylesheet" href="/static/bower_components/chartist-plugin-tooltip/dist/chartist-plugin-tooltip.css">
    <style>
svg.ct-chart-bar, svg.ct-chart-line{
    overflow: visible;
}
.ct-label.ct-label.ct-horizontal.ct-end {
  position: relative;
  justify-content: flex-end;
  text-align: right;
  transform-origin: 100%% 0;
  transform: translate(-100%%) rotate(-45deg);
  white-space:nowrap;
}
    </style>
    <link rel="stylesheet" href="/static/style.css" >
  </head>
  <body>
    <script src="/static/bower_components/chartist/dist/chartist.min.js"></script>
    <script src="/static/bower_components/chartist-plugin-tooltip/dist/chartist-plugin-tooltip.min.js"></script>
    <script src="/static/bower_components/chartist-plugin-pointlabels/dist/chartist-plugin-pointlabels.min.js"></script>
    <script src="/static/bower_components/chartist-plugin-axistitle-dist/chartist-plugin-axistitle.min.js"></script>
''' % title
    if out is not None and hasattr(out, 'write'):
        out.write(s)
    else:
        return s

def chart_tail(out=None):
    s = '''</body>
    </html>'''
    if out is not None and hasattr(out, 'write'):
        out.write(s)
    else:
        return s

def __shrink_one(l, c):
    if len(c) != len(l):
        return c
    for i in range(len(l)):
        if l[i] != c[i]:
            return '-'+c[i:]
    return "-"
# 压缩 label 的,   "2018-09-27 12:01", "2018-09-27 13:01" => "2018-09-27 12:01", "-13:01"
def label_shrink(ls):
    last_l = ""
    ret = []
    for l in ls:
        ret.append( __shrink_one(last_l, l) )
        last_l = l
    return ret
