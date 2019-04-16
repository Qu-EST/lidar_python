import mirror as m
from Gpib import *
import argparse
import counter as c
import time

DLY_START = -150
DLY_END = 150
DLY_INC = 2
TDC = 100000


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--itrno', type=str, help='itr no of the file to save the data', default='1')
args = parser.parse_args()



mems = m.open_mirror()
m.set_pos(mems,-0.03 , -0.03)

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

X = []
Y = []
save_file = open("nlos_met6.csv","w")
for i in range(0, 5 ):
    max_count = 0;
    MLV = 400;
    #ave_file = open("{}NoHPlate{}.csv".format(args.itrno,i), 'w')
    dly.write("DLY {:.3f}".format(DLY_START))
    time.sleep(600/1000)
    for dly_data in frange(DLY_START, DLY_END, DLY_INC):
        dly.write("DLY {:.3f}".format(dly_data))
        time.sleep(300/1000)
        count = c.get_count(TDC)
        data = "{:.3f},{}\n".format(dly_data, count)
        print("{} {}".format(args.itrno,data))
        save_file.write(data)
        if(count > max_count):
            max_count = count;
            MLV = dly_data
    print("HEY{} {} {}".format(MLV,max_count,i))
    X.append(MLV)
    Y.append(max_count)
   #save_file.close()

    data = "{:.3f},{}\n".format(MLV, max_count)
    #ave_file.write(data)

print(X)
print(Y)
save_file.close


m.close_mirror(mems)
dly.write('dly 0')
