import argparse
from Gpib import *
import mirror as mems
import counter
import time
from collections import defaultdict



parser = argparse.ArgumentParser()
parser.add_argument("-x","--xmin", type=float, help="X min value", default=-0.1)
parser.add_argument("-X", "--xmax", type=float, help="X max value", default =0.1)
parser.add_argument("-y", "--ymin", type=float, help="Y min value", default=-0.1)
parser.add_argument("-Y", "--ymax", type=float, help="Y max value", default=0.1)
parser.add_argument("-z", "--zmin", type=float, help="Z min value", default=-50)
parser.add_argument("-Z", "--zmax", type=float, help="Z max value", default=150)
parser.add_argument('-s', '--xstep', type=float, help='x step size', default=0.02)
parser.add_argument('-u', '--ystep', type=float, help='y stepsize', default=0.02)
parser.add_argument('-m', '--zmicro', type=float, help='z micro step size', default=2)
parser.add_argument('-M', '--zmacro', type=float, help='z Macro step size', default=20)
parser.add_argument('-f', '--filename', type=str, help='filename to save the data', default='lidar.csv')
parser.add_argument('-t', '--tdc', type=int, help='tdc integration time', default=10)
parser.add_argument('-p', '--peakcheck', type=float, help='peak check', default=10)
parser.add_argument('-l', '--lidar', help='doing a normal lidar', action='store_true')
parser.add_argument('-v', '--verbose', help='print the verbose', action='store_true')
parser.add_argument('--zlast', help='zlast or the initial position of the delay', default=0) 


args = parser.parse_args()

fds = {'delay_fd':None, 'mirror_fd':None, 'save_fd':None, 'count_fd':None, 'control_fd':None}

fds['delay_fd'] = Gpib(name=0, pad=5)

if(fds['delay_fd']<0):
    print "unable to connect to delay"
    exit()

fds['mirror_fd'] = mems.open_mirror()
if(fds['mirror_fd']<0):
    print "unable to connect to mirror"
    exit()

fds['save_fd'] = open(args.filename, 'w+')
fds['save_fd'].write('delay,y,x,counts\n')


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
    return round(L, 3)

def count_helper(fds):
    fds['count_fd'], fds['control_fd'] = counter.open_counter(args.tdc)
    count = counter.count(fds['control_fd'], fds['count_fd'], args.tdc)
    counter.close(fds['control_fd'], fds['count_fd'])
    time.sleep(args.tdc/1000000)
    if count!=None:
        return count
    else:
        return count_helper(fds)
def scan(zmin,zmax,step,zlast, fds, x, y):
    zlist = [z for z in frange(zmin,zmax,step)]
    z_max_pos = -100000
    max_counts = 0
    delay_counts = []
    for z in zlist:
        
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        wait_time = abs(z - zlast)*20
        ######ADDITIONAL WAIT TIME FOR SUB_PICO STEPS
        wait_time += 30
        #print wait_time
        time.sleep(wait_time/1000)
        zlast = z
        count = count_helper(fds)
        delay_counts.append([z,count])
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out
        if (count > max_counts):
            max_counts = count
            z_max_pos = z
    return z_max_pos
def test_peak (delay_counts, zmax_counts_pos):
     checkone = delay_counts[zmax_counts_pos-1][1]-delay_counts[zmax_counts_pos-2][1]
     checktwo = delay_counts[zmax_counts_pos+1][1]-delay_counts[zmax_counts_pos+2][1]
   
     if (checkone>0 and checktwo>0):
        return 1
     else:
        return 0
def test_scan(zmin,zmax,step,zlast, fds, x, y):
    zlist = [z for z in frange(zmin,zmax,step)]
    print "Doing Fine Scan"
    zmax_counts_pos = 0
    delay_counts=[]
    
   
    for z in zlist:
        
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        wait_time = abs(z - zlast)*20 + 30
        #print wait_time
        #time.sleep(wait_time/1000)
        zlast = z
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out
        delay_counts.append([z, count])
        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = len(delay_counts) -1
    last_pos=False
    init_pos=False
    zwait = 0 ######################################################
    while(zmax_counts_pos>=len(delay_counts)-1 or zmax_counts_pos==len(delay_counts)-2 ):
       
        #last_pos=True
        z = delay_counts[len(delay_counts)-1][0]+step
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        wait_time = abs(z - zlast)*20
    
        time.sleep(wait_time/1000)
        zlast = z
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out
        delay_counts.append([z, count])
        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = len(delay_counts) -1
   
    
    while(zmax_counts_pos==0 or zmax_counts_pos ==1):
        #init_pos = True
       
    
        z = delay_counts[0][0]-step
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        wait_time = abs(z - zlast)*20
        #print wait_time
        time.sleep(wait_time/1000)
        zlast = z
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out
        delay_counts.insert(0,[z, count])
        zmax_counts_pos += 1
        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = 0
       
    #return [delay_counts[zmax_counts_pos][0],zlast,delay_counts[zmax_counts_pos][1]]
    if(test_peak(delay_counts,zmax_counts_pos) == 1):
        return [delay_counts[zmax_counts_pos][0],zlast,delay_counts[zmax_counts_pos][1]]
    else:
        return [-1111,zlast,delay_counts[zmax_counts_pos][1]]
def mirrorScan(xlist, ylist,zlist):
    for z in zlist:
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        time.sleep(1000/1000)
        for x in xlist:
            for y in ylist:
                mems.set_pos(fds['mirror_fd'], x, y)
                time.sleep(100/1000)
                count = count_helper(fds)
                out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
                fds['save_fd'].write(out+'\n')
                if(args.verbose ):
                    print out
    

    
    
def lidar(args, fds):
    #zlist = [z for z in frange(fzmin, fzmax, args.zmicro)]
    zmin = args.zmin
    zmax = args.zmax
    step = args.zmicro
    macro_step = args.zmacro
    zlast = 0
    prev_peak = -1111
    xlist = [x for x in frange(args.xmin, args.xmax, args.xstep)]
    ylist = [y for y in frange(args.ymin, args.ymax, args.ystep)]
    zlist = [z for z in frange(zmin,zmax,step)]
    data_dict = defaultdict(dict)
    for x in xlist:
        for y in ylist:
            data_dict[x][y] = [0,0]
        
    
    for z in zlist:
        
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        time.sleep(0.1)
        for x in xlist:
            wait_mirror = 0
            for y in ylist:
                mems.set_pos(fds['mirror_fd'], x, y)
                time.sleep(4) #wait time to follow beam
                if (wait_mirror == 0):
                    time.sleep(0.005)
                    wait_mirror = 1

                    # merge issue correct the code as desired
                    
# 
#                 count = 0 # count_helper(fds)
#                 out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
#                 fds['save_fd'].write(out+'\n')
#                 if(args.verbose ):
#                     print out

# 
                count = count_helper(fds)
                if count>data_dict[x][y][1]:
                    data_dict[x][y] =[z, count]
#                out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
#                fds['save_fd'].write(out+'\n')
#                if(args.verbose ):
#                    print out
    for x in xlist:
        for y in ylist:
            out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(data_dict[x][y][0], y, x,data_dict[x][y][1])
            fds['save_fd'].write(out+'\n')
# 

start = time.clock()
if(args.verbose):
    print "Starting at time {}".format(start)
    
if(args.lidar):
    lidar(args, fds)
else:
    adaptive_lidar(args, fds)
if(args.verbose):
    end = time.clock()
    print "Ending at time {}".format(end)
    print "Time taken {}".format(end-start)

mems.close_mirror(fds['mirror_fd'])
fds['delay_fd'].write('dly 0')
