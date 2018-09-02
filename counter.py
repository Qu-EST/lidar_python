import os
import struct
import time


WAIT_NSTART = 2
WAIT_START = 3
NWAIT_NSTART = 0


def open_counter(int_time):
    count_fd = open('/dev/xillybus_status_photoncount', 'r')
    control_fd = os.open('/dev/xillybus_timeout_control', os.O_WRONLY)
    if(control_fd>0):
        os.write(control_fd, chr(int_time))
    
    return count_fd, control_fd

def get_count(count_fd, control_fd, int_time):
    count_fd.seek(0)
    done, = struct.unpack('<I', count_fd.read(4))
    if(done==1):
        os.write(control_fd, chr(WAIT_NSTART))
        count, = struct.unpack('<I', count_fd.read(4))
        return count
    else:
        time.sleep(int_time/1000)
        return get_count(count_fd, control_fd, int_time)

def change_ctrl(control_fd, ctrl_val):
    os.lseek(control_fd, 1, os.SEEK_SET)
    os.write(control_fd, chr(ctrl_val))

    
def count(control_fd, count_fd, int_time):
    change_ctrl(control_fd, WAIT_NSTART)
    change_ctrl(control_fd, WAIT_START)
    cnt = get_count(count_fd, control_fd, int_time)
    change_ctrl(control_fd, NWAIT_NSTART)
    return cnt
    

