import argparse
from Gpib import *
import mirror as mems
import counter 

parser = argparse.ArgumentParser()
parser.add_argument("-x","--xmin", type=float, help="X min value", default=0.5)
parser.add_argument("-X", "--xmax", type=float, help="X max value", default =1)
parser.add_argument("-y", "--ymin", type=float, help="Y min value", default=0.5)
parser.add_argument("-Y", "--ymax", type=float, help="Y max value", default=1)
parser.add_argument("-z", "--zmin", type=float, help="Z min value", default=0)
parser.add_argument("-Z", "--zmax", type=float, help="Z max value", default=200)
parser.add_argument('-s', '--xstep', type=float, help='x step size', default=0.1)
parser.add_argument('-u', '--ystep', type=float, help='y stepsize', default=0.1)
parser.add_argument('-m', '--zmicro', type=float, help='z micro step size', default=4)
parser.add_argument('-M', '--zmacro', type=float, help='z Macro step size', default=20)
parser.add_argument('-f', '--filename', type=str, help='filename to save the data', default='lidar.csv')
parser.add_argument('-t', '--tdc', type=int, help='tdc integration time', default=10)
parser.add_argument('-p', '--peakcheck', type=float, help='peak check', default=10)
parser.add_argument('-l', '--lidar', help='doing a normal lidar', action='store_true')
parser.add_argument('-v', '--verbose', help='print the verbose', action='store_true')


args = parser.parse_args()

delay_fd = Gpib(name=0, pad=5)
if(delay_fd<0):
    print "unable to connect to delay"
    exit()

mirror_fd = mems.open_mirror()
if(mirror_fd<0):
    print "unable to connect to mirror"
    exit()

    
count_fd, control_fd = counter.open_counter(args.tdc)

save_fd = open(args.filename, 'w+')





if(count_fd<0):
    print "unable to connect to the counter"
    mems.close_mirror(mirror_fd)
    exit()

if(control_fd<0):
    print "unable to connect to the counter controller"
    mems.close_mirror(mirror_fd)
    exit()

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


def lidar(args, delay_fd, mirror_fd, count_fd, control_fd, save_fd):

    for x in frange(args.xmin, args.xmax, args.xstep):
        for y in frange(args.ymin, args.ymax, args.ystep):
            mems.set_pos(mirror_fd, x, y)
            for z in frange(args.zmin, args.zmax, args.zmicro):
                delay_fd.write('DLY {:.3f}'.format(z))
                count = counter.count(control_fd, count_fd, args.tdc)
                out = x + " " + y + " " + z + " " + str(count)
                print out
                save_fd.write(out+'\n')   


def adaptive_lidar(args, delay_fd, mirror_fd, count_fd, control_fd, save_fd):
    pass



    
if(args.lidar):
    lidar(args, delay_fd, mirror_fd, count_fd, control_fd, save_fd)
else:
    adaptive_lidar(args, delay_fd, mirror_fd, count_fd, control_fd, save_fd)




