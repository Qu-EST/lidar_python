import mirror as m
from Gpib import *
import argparse
import counter as c
import time

DLY_START = 20
DLY_END = 60
DLY_INC = 2
TDC = 500
ymin = 0.5
ymax = 0.76
ystep = 0.05


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--itrno', type=str, help='itr no of the file to save the data', default='1')
args = parser.parse_args()



mems = m.open_mirror()
m.set_pos(mems, -0.02, 0.1)

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
ylist = [y for y in frange(ymin,ymax,ystep)]

#save_file = open("fogIndTest4.csv",'w')
for y in ylist:
    m.set_pos(mems, 0.03, y)
    print(y)
    
    peaks = []
    counts = []
    dataset = []
    
        
    for i in range(0, 5):
        max_count = 0;
        MLV = 400;
        #ave_file = open("{}NoHPlate{}.csv".format(args.itrno,i), 'w')
        dly.write("DLY {:.3f}".format(DLY_START))
        time.sleep(600/1000)
        for dly_data in frange(DLY_START, DLY_END, DLY_INC):
            dly.write("DLY {:.3f}".format(dly_data))
            time.sleep(150/1000)
            count = c.get_count(TDC)
            data = "{:.3f},{}\n".format(dly_data, count)
            #print("{} {}".format(args.itrno,data))
            #ave_file.write(data)
            if(count > max_count):
                max_count = count;
                MLV = dly_data
        #print("HEY{} {}".format(MLV,max_count))
        peaks.append(MLV)
        counts.append(max_count)
                #save_file.close()

        data = "{:.3f},{},{:0.3f}\n".format(MLV, max_count,y)
        #print(data)
               #save_file.write(data)

    print(peaks)
    print(counts)
    test = [peaks ,counts]
    #print(test)
#save_file.close





m.close_mirror(mems)
