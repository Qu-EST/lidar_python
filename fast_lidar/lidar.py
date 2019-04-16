import argparse
from LidarData import LidarData
#from Gpib import *
from ReaderThread import ReaderThread
from WriterThread import WriterThread



data = LidarData()


#get the inputs from the cmd

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dual_time', type=int, help='dual time to count the photons', default=100)
parser.add_argument('-p', '--pixel_count', type=int, help='number of pixels in a frame', default=1000)
parser.add_argument('-f', '--file_name', type=str, help='filename ot save the data', default='lidar.csv')
parser.add_argument('-z', 'zmin', type=float, help='Minimum delay value in pico seconds', default=0)
parser.add_argument('Z', 'zmax', type=float, help='Maximum delay value in pico seconds', default=50)
parser.add_argument('-m', '--zmicro', type=float, help='z micro step size', default=2)
parser.add_argument('-M', '--zmacro', type=float, help='z Macro step size', default=10)



args = parser.parse_args()
data.args = args


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



# start the writerthread
writer_thread = WriterThread()
writer_thread.start()

# start the reader thread
reader_thread = ReaderThread()
reader_thread.start()

zlist = [z for z in frange(args.zmin,args.zmax,args.zmacro)]


for z in zlist:
    # move the delay line
    
    #send a start pulse

    # wait for the writer to complete the frame
    data.frame_done.wait()
    pass


#send signals to close the thread
reader_thread.off()
writer_thread.off()


#wait for the threads to complete i,e call join()
reader_thread.join()
writer_thread.join()


#exit




