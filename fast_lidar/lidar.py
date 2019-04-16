import argparse
from LidarData import LidarData
#from Gpib import *
from ReaderThread import ReaderThread
from WriterThread import WriterThread

import os
import struct
import sys

#constants to control the frame start
WAIT_NSTART = 2
WAIT_START = 3
NWAIT_NSTART = 0



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




def change_ctrl(control_fd, ctrl_val):
    '''function to change the control of the frame start'''
    os.lseek(control_fd, 0, os.SEEK_SET)
    os.write(control_fd, bytes([ctrl_val]))


#open the control file

control_fd = os.open(data.control_file, os.O_WRONLY)

# change the dual_time and the pixel count
if(control_fd>0):
    os.lseek(control_fd, 1, os.SEEK_SET)
    dual_time = struct.pack('<I', args.dual_time)
    os.write(control_fd, dual_time);
    pixel_count = struct.pack('<I', args.pixel_count)
    os.write(control_fd, pixel_count)
    change_ctrl(control_fd, WAIT_NSTART)
else:
    print('unable to open the control file')
    sys.exit(-1)

    


# start the writerthread
writer_thread = WriterThread()
writer_thread.start()

# start the reader thread
reader_thread = ReaderThread()
reader_thread.start()

zlist = [z for z in frange(args.zmin,args.zmax,args.zmacro)]

#testing for 1 frame
zlist =(1)                      # comment when not testing

for z in zlist:
    # move the delay line
    
    #send a start pulse

    change_ctrl(control_fd, WAIT_NSTART)
    change_ctrl(control_fd, WAIT_START)
    
    
    # wait for the writer to complete the frame
    data.frame_done.wait()
    change_ctrl(control_fd, WAIT_NSTART)
    change_ctrl(control_fd, NWAIT_NSTART)
    pass


#send signals to close the thread
reader_thread.off()
writer_thread.off()


#wait for the threads to complete i,e call join()
reader_thread.join()
writer_thread.join()


#exit




