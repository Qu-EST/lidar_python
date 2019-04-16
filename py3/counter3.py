import os
import struct
import time


WAIT_NSTART = 2
WAIT_START = 3
NWAIT_NSTART = 0


def open_counter(int_time):
    count_fd = open('/dev/xillybus_status_photoncount', 'br')
    control_fd = os.open('/dev/xillybus_timeout_control', os.O_WRONLY)
    if(control_fd>0):
        os.lseek(control_fd, 1, os.SEEK_SET)
        byte_time= struct.pack('<I', int_time)
        os.write(control_fd, byte_time)
        change_ctrl(control_fd, WAIT_NSTART)
    
    return count_fd, control_fd


def change_ctrl(control_fd, ctrl_val):
    os.lseek(control_fd, 0, os.SEEK_SET)
    os.write(control_fd, bytes([ctrl_val]))

    
def count(control_fd, count_fd, int_time):
    change_ctrl(control_fd, WAIT_NSTART)
    change_ctrl(control_fd, WAIT_START)
    wait_time = (float(int_time))/1000000
    time.sleep(wait_time)
    count_fd.seek(0)
    done, = struct.unpack('<I', count_fd.read(4))
    change_ctrl(control_fd, WAIT_NSTART)
    count, = struct.unpack('<I', count_fd.read(4))
    change_ctrl(control_fd, NWAIT_NSTART)
    return count

def close(control_fd, count_fd):
    os.close(control_fd)
    count_fd.close()
    
def get_count(tdc=10):
    count_fd, control_fd = open_counter(tdc)
    counts = count(control_fd, count_fd, tdc)
    close(control_fd, count_fd)
    if counts!=None:
        return counts
    else:
        return get_count(tdc)

