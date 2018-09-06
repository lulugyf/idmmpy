
import matplotlib.pyplot as plt
import numpy as np

# def get_feature_importance(list_of_features):
#     n_estimators =10000
#     random_state =0
#     n_jobs =4
#     x_train =data_frame[list_of_features]
#     y_train =data_frame.iloc[: ,-1]
#     feat_labels= data_frame.columns[1:]
#     forest = BaggingRegressor(n_estimators=n_estimators ,random_state=random_state ,n_jobs=n_jobs)
#     forest.fit(x_train ,y_train)
#     importances =forest.feature_importances_
#     indices = np.argsort(importances)[::-1]
#
#
#     for f in range(x_train.shape[1]):
#         print("%2d) %-*s %f" % ( f +1 ,30 ,feat_labels[indices[f]],
#                                 importances[indices[f]]))
#
#
#     plt.title("Feature Importance")
#     plt.bar(range(x_train.shape[1]) ,importances[indices] ,color='lightblue' ,align='center')
#     plt.xticks(range(x_train.shape[1]) ,feat_labels[indices] ,rotation=90)
#     plt.xlim([-1 ,x_train.shape[1]])
#     plt.tight_layout()
#     plt.show()

def plot_bar_chart(label_to_value, title, x_label, y_label):
    """
    Plots a bar chart from a dict.

    Args:
        label_to_value: A dict mapping ints or strings to numerical values (int
            or float).
        title: A string representing the title of the graph.
        x_label: A string representing the label for the x-axis.
        y_label: A string representing the label for the y-axis.
    """
    n = len(label_to_value)
    labels = sorted(label_to_value.keys())
    values = [label_to_value[label] for label in labels]
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    #plt.bar(range(n), values, align='center')
    plt.plot(range(n), values)
    plt.grid()
    nn = range(0, n, 30)
    ll = [labels[i] for i in nn]
    #plt.xticks(range(n), labels, rotation='vertical', fontsize='7')
    plt.xticks(nn, ll, rotation='vertical', fontsize='7')
    plt.gcf().subplots_adjust(bottom=0.2) # make room for x-axis labels
    plt.show()

import time
def tmstr(s):
    if s.find(':') > 0:
        return time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S")) * 1000
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(s) / 1000))
def main():
    cc = {}  #
    fname = "e:/worksrc/idmm/idmmpy/9.5"
    for l in open(fname):
        n = l.strip().split()
        if len(n ) != 2: continue
        # t = tmstr(str(int(n[0])*60000))
        # c = int(n[1])*200
        # cc[t[11:16]] = c
        cc[n[0]] = int(n[1])
    plot_bar_chart(cc, 'date: '+fname[fname.rindex('/')+1:], "time", "message count per min")

def main1():
    #  grep "timeout warning" ble.debug.20180904|awk '{print substr($2,6,5)}'|sort|uniq -c|awk '{print $2, $1}' >44
    # grep "timeout warning" ble.debug|awk '{print substr($2,6,5)}'|sort|uniq -c|awk '{print $2, $1}' >55
    # grep "timeout warning" ble.debug.20180903|awk '{print substr($2,6,5)}'|sort|uniq -c|awk '{print $2, $1}' >66

    for i in range(1,6):
        f = "e:/worksrc/idmm/idmmpy/e9.%d"%i
        cc = {}
        total = 0
        for l in open(f):
            n = l.strip().split()
            if len(n ) != 2: continue

            cc[n[0]] = int(n[1])
            total += int(n[1])
        plot_bar_chart(cc, "date 9.%d  warning count, total: %d"%(i, total), "time", "message count per min")

if __name__ == '__main__':
    main1()
    #main()
