import time
import sys
from datetime import datetime, timedelta

def _print_tmstr(t):
    print "  %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)/1000))

def _print_tm(s):
    print " %d" % (time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S"))*1000, )


def tmstr(s):
    if s.find(':') > 0:
        return time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S"))*1000
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(s) / 1000))

# python -c "import tm; print tm.datedelta(-14)"
def datedelta(n_days):
    t = datetime.now()
    delta = timedelta(days=n_days)
    t1 = t + delta
    return t1.strftime("%Y-%m-%d")

def time_offset(n_seconds):
    t = datetime.now()
    t = t + timedelta(seconds=n_seconds)
    return t.strftime("%Y-%m-%d %H:%M:%S")

def __tbs_log():
    with open("tbs.log1", "w") as f:
        with open("tbs.log") as f1:
            for line in f1:
                if line.startswith("2"):
                    f.write(line)
                else:
                    l = line.strip().split('\t')
                    if l[3].endswith("MB"):
                        l[3] = l[3][:-5]+"GB"
                    if l[2].endswith("MB"):
                        l[2] = l[2][:-5]+"GB"
                    f.write("%s\n"%"\t".join(l))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "give me a time, time format: %Y-%m-%d %H:%M:%S"
    else:
        s = sys.argv[1]
        if s.find(':') > 0:
            _print_tm(s)
        else:
            _print_tmstr(s)
