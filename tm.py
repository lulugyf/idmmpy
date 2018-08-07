import time
import sys

def _print_tmstr(t):
    print "  %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)/1000))

def _print_tm(s):
    print " %d" % (time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S"))*1000, )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "give me a time"
    else:
        s = sys.argv[1]
        if s.find(':') > 0:
            _print_tm(s)
        else:
            _print_tmstr(s)
