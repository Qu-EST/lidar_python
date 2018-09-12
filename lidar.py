import argparse
from Gpib import *
import mirror as mems
import counter
import time


parser = argparse.ArgumentParser()
parser.add_argument("-x","--xmin", type=float, help="X min value", default=-0.1)
parser.add_argument("-X", "--xmax", type=float, help="X max value", default =0.1)
parser.add_argument("-y", "--ymin", type=float, help="Y min value", default=-0.3)
parser.add_argument("-Y", "--ymax", type=float, help="Y max value", default=0.1)
parser.add_argument("-z", "--zmin", type=float, help="Z min value", default=-50)
parser.add_argument("-Z", "--zmax", type=float, help="Z max value", default=150)
parser.add_argument('-s', '--xstep', type=float, help='x step size', default=0.04)
parser.add_argument('-u', '--ystep', type=float, help='y stepsize', default=0.04)
parser.add_argument('-m', '--zmicro', type=float, help='z micro step size', default=2)
parser.add_argument('-M', '--zmacro', type=float, help='z Macro step size', default=20)
parser.add_argument('-f', '--filename', type=str, help='filename to save the data', default='lidar.csv')
parser.add_argument('-t', '--tdc', type=int, help='tdc integration time', default=10)
parser.add_argument('-p', '--peakcheck', type=float, help='peak check', default=10)
parser.add_argument('-l', '--lidar', help='doing a normal lidar', action='store_true')
parser.add_argument('-v', '--verbose', help='print the verbose', action='store_true')


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

    
#count_fd, control_fd = counter.open_counter(args.tdc)

fds['save_fd'] = open(args.filename, 'w+')
fds['save_fd'].write('delay,y,x,counts\n')



# fds.count_fd=None
# fds.control_fd=None

# if(count_fd<0):
#     print "unable to connect to the counter"
#     mems.close_mirror(mirror_fd)
#     exit()

# if(control_fd<0):
#     print "unable to connect to the counter controller"
#     mems.close_mirror(mirror_fd)
#     exit()

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

    L = [None] * count

    L[0] = end
    for i in (xrange(1,count)):
        L[i] = L[i-1] + inc
    return L

def count_helper(fds):
    fds['count_fd'], fds['control_fd'] = counter.open_counter(args.tdc)
    count = counter.count(fds['control_fd'], fds['count_fd'], args.tdc)
    #time.sleep(10.0/1000)
    counter.close(fds['control_fd'], fds['count_fd'])
    if count!=None:
        return count
    else:
        return count_helper(fds)
def scan(args, fds, zlist, x, y):

    for z in zlist:
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        #time.sleep(50.0/1000)
        if(z==args.zmin):
            time.sleep(1)
            count = count_helper(fds)
            # out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
            # fds['save_fd'].write(out+'\n')
            # if(args.verbose):
            #    print out
            time.sleep(250.0/1000)
            
        
            
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out

            



def lidar(args, fds):

    zlist=[]
    for z in frange(args.zmin, args.zmax, args.zmicro):
        zlist.append(z)
    for x in frange(args.xmin, args.xmax, args.xstep):
        for y in frange(args.ymin, args.ymax, args.ystep):
            mems.set_pos(fds['mirror_fd'], x, y)
            scan(args, fds, zlist, x, y)
           # zlist.reverse()


            

def get_peak(fds, zlist):
    '''return a adaptive'''
    adaptive = {}
    zmax_count = zlist[0]
    for z in zlist:
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        count = count_helper(fds)
        adaptive[z] = count
        if(adaptive[zmax_count]<count):
            zmax_count = z
    return zmax_count

def fine_scan(args, fds, x, y , fzmin, fzmax):
    '''do a fine scan, return a adaptive value'''
    zmax_counts_pos = 0
    delay_counts=[]
    zlist = [z for z in frange(fzmin, fzmax, args.zmicro)]
    for z in zlist:
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
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
    while(zmax_counts_pos==len(delay_counts)-1):
        last_pos=True
        z = delay_counts[len(delay_counts)-1][0]+args.zmicro
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out

        delay_counts.append([z, count])
        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = len(delay_counts) -1
    if(last_pos):
        z = delay_counts[len(delay_counts)-1][0]+args.zmicro
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out

        delay_counts.append([z, count])
        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = len(delay_counts) -1

    while(zmax_counts_pos==0):
        init_pos = True
        z = delay_counts[0][0]-args.zmicro
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        if(args.verbose):
            print out

        delay_counts.insert(0,[z, count])
        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = 0
        else:
            zmax_counts_pos+=zmax_counts_pos
    if(init_pos):
        z = delay_counts[0][0]-args.zmicro
        fds['delay_fd'].write('DLY {:.3f}'.format(z))
        count = count_helper(fds)
        out = '{:.3f}, {:.3f}, {:.3f}, {}'.format(z, y, x, count)
        fds['save_fd'].write(out+'\n')
        delay_counts.insert(0,[z, count])
        if(args.verbose):
            print out

        if(delay_counts[zmax_counts_pos][1]<count):
            zmax_counts_pos = 0
        else:
            zmax_counts_pos+=zmax_counts_pos
    checkone = delay_counts[zmax_counts_pos-1][1]-delay_counts[zmax_counts_pos-2][1]
    checktwo = delay_counts[zmax_counts_pos+1][1]-delay_counts[zmax_counts_pos+2][1]
    if (checkone>0 and checktwo>0):
        return delay_counts[zmax_counts_pos][0]
    else:
        return None
            
            

def adaptive_lidar(args, fds):
    adaptive = None
    for x in frange(args.xmin, args.xmax, args.xstep):
        for y in frange(args.ymin, args.ymax, args.ystep):
            mems.set_pos(fds['mirror_fd'], x, y)
            
            if(adaptive):
                adpative = fine_scan(args, fds, x, y, adaptive-2*args.zmicro, adaptive+2*args.zmicro)
                pass
            if(adaptive==None):
                if(args.verbose):
                    print "Doing a macro scan"
                zlist = []
                for z in frange(args.zmin, args.zmax, args.zmacro):
                    zlist.append(z)
                peak = get_peak(fds, zlist)
                adaptive = fine_scan(args, fds, x, y, peak-15, peak+15)
                #adaptive = do adaptive scan
    



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




