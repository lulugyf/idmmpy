#coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter, MaxNLocator



#20180823011001
#TBS_IDMMDB_IDX	5.898%	780518MB	829440MB
#TBS_IDMMDB_DATA	28.255%	749366MB	1044480MB
def db_tbs(logfile="e:/tmp/tbs_fq.log", getdata=True):
    labels = []
    tbs_free = []
    for line in open(logfile):
        if line.startswith("2018"):
            # s = line.strip()[4:-2]
            # label = s[:2]+"-"+s[2:4] + " " + s[4:6] + ":"+s[6:]
            # labels.append( s )
            labels.append(line.strip())
        elif line.startswith("TBS_IDMMDB_DATA"):
            tbs_free.append(int(line.split()[2][:-2]))
    if getdata:
        return labels, tbs_free

    fig = plt.figure()
    ax = fig.add_subplot(111)
    xs = range(len(tbs_free))
    def format_fn(tick_val, tick_pos):
        if int(tick_val) in xs:
            return labels[int(tick_val)]
        else:
            return ''
    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    #plt.plot(xs, tbs_free)
    plt.scatter(xs, tbs_free, color='blue')
    ##plt.xticks(xs, labels, rotation='vertical')
    plt.show()

    f = open("e:/tmp/tbs_fq1.log", "w")
    f.write('x,y\n')
    for i in range(len(tbs_free)):
        f.write("%d,%d\n"%(i, tbs_free[i]))
    f.close()

# 使用线性回归预测表空间剩余
from datetime import date, datetime, timedelta
def x_date(n, datestr):
    # 20180817121001
    d = datetime.strptime(datestr, '%Y%m%d%H%M%S')
    delta = timedelta(hours=1)
    xlb = []
    for i in range(n):
        xlb.append(d.strftime("%m%d%H%M"))
        d = d + delta
    return xlb

import pandas as pd
from sklearn import linear_model
def lnreg():
    # http://www.cnblogs.com/hhh5460/p/5786115.html
    # df = pd.read_csv('e:/tmp/tbs_fq1.log')
    # start_hour = '20180817121001'
    # end_hour = '20180903101001'
    labels, ys = db_tbs("e:/tmp/tbs_xq.log")
    xs = range(len(ys))
    start_hour = labels[0]
    end_hour = '20180903101001'

    #print(dir(df))
    # 20180823081001   20180828081001
    d1 = datetime.strptime(start_hour, '%Y%m%d%H%M%S')
    d2 = datetime.strptime(end_hour, '%Y%m%d%H%M%S')
    t = d2 - d1
    target = t.days * 24 + t.seconds/3600  # 要预测的日期距离小时数

    regr = linear_model.LinearRegression()
    # 拟合
    #regr.fit(df['x'].values.reshape(-1, 1), df['y'])  # 注意此处.reshape(-1, 1)，因为X是一维的！
    regr.fit(np.matrix(xs).reshape(-1, 1), ys)
    # 不难得到直线的斜率、截距
    a, b = regr.coef_, regr.intercept_
    print(a * target + b)

    y = regr.predict(target)

    labels = x_date(target, start_hour)
    def format_fn(tick_val, tick_pos):
        j = int(tick_val)
        if j < 0 or j >= len(labels): return tick_val
        return labels[j]
    box = dict(facecolor='yellow', pad=5, alpha=0.2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    # 1.真实的点
    #plt.scatter(df['x'], df['y'], color='blue')
    plt.scatter(xs, ys, color='blue')
    # 2 拟合直线
    plt.plot(range(target), regr.predict(np.matrix(range(target)).reshape(-1, 1)), color="red")

    for tdate in ('20180828101001', '20180903101001'):
        d2 = datetime.strptime(tdate, '%Y%m%d%H%M%S')
        t = d2 - d1
        x = t.days * 24 + t.seconds / 3600
        y = regr.predict(x)
        # 3. 预测点的值画点
        plt.scatter(x, y, color="green")
        plt.annotate(
            '%s\n%d'%(tdate, y),
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    ax.set_ylabel('free tablespace in MB', bbox=box)
    plt.show()

def test1():
    box = dict(facecolor='yellow', pad=5, alpha=0.2)

    fig = plt.figure()
    fig.subplots_adjust(left=0.2, wspace=0.6)

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    ax1 = fig.add_subplot(221)
    ax1.plot(2000 * np.random.rand(10))
    ax1.set_title('ylabels not aligned')
    ax1.set_ylabel('misaligned 1', bbox=box)
    ax1.set_ylim(0, 2000)
    ax3 = fig.add_subplot(223)
    ax3.set_ylabel('misaligned 2', bbox=box)
    ax3.plot(np.random.rand(10))

    labelx = -0.3  # axes coords

    ax2 = fig.add_subplot(222)
    ax2.set_title('ylabels aligned')
    ax2.plot(2000 * np.random.rand(10))
    ax2.set_ylabel('aligned 1', bbox=box)
    ax2.yaxis.set_label_coords(labelx, 0.5)
    ax2.set_ylim(0, 2000)

    ax4 = fig.add_subplot(224)
    ax4.plot(np.random.rand(10))
    ax4.set_ylabel('aligned 2', bbox=box)
    ax4.yaxis.set_label_coords(labelx, 0.5)

    plt.show()


def test2():
    np.random.seed(19680801)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(100 * np.random.rand(20))

    formatter = ticker.FormatStrFormatter('$%1.2f')  # '$%1.2f'
    ax.xaxis.set_major_formatter(formatter)

    for tick in ax.xaxis.get_major_ticks():
        tick.label1On = True
        tick.label2On = False
        tick.label1.set_color('green')

    plt.show()

if __name__ == '__main__':
    #db_tbs(logfile="e:/tmp/tbs_fq.log", getdata=False)
    lnreg()
    #test2()


