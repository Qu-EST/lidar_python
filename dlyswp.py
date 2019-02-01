import mirror as m
from Gpib import *
import argparse
import counter as c
import time

DLY_START = -10
DLY_END = 120
DLY_INC = 2.5
TDC = 100000


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--itrno', type=str, help='itr no of the file to save the data', default='1')
args = parser.parse_args()



mems = m.open_mirror()
m.set_pos(mems, 0.01, 0.3)

dly = Gpib(name =0, pad =5)



def frange(end,start=0,inc=0,precision=1):
    """A range function that accepts float increments."""
    import math

    if not start:
        start = end + 0.0
        end = 0.0
    else: end += 0.0
    
    if not inc:
        inc = 1.0
    count = int(math.ceil((start - end) / inc))

   # L = [None] * count
    L = []
    L.append(float(end))
   # L.append(end)
    for i in (xrange(1,count)):
        L.append(L[i-1] + inc)
    return L


for i in range(0, 20):
    save_file = open("{}varAtnModule{}.csv".format(args.itrno,i), 'w')
    dly.write("DLY {:.3f}".format(DLY_START))
    time.sleep(200/1000)
    for dly_data in frange(DLY_START, DLY_END, DLY_INC):
        dly.write("DLY {:.3f}".format(dly_data))
        time.sleep(150/1000)
        count = c.get_count(TDC)
        data = "{:.3f},{}\n".format(dly_data, count)
        print("{} {}".format(args.itrno,data))
        save_file.write(data)
    save_file.close()





m.close_mirror(mems)
