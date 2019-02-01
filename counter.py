import os
import struct
import time


WAIT_NSTART = 2
WAIT_START = 3
NWAIT_NSTART = 0


def open_counter(dwell, sweep):
    count_fd = open('/dev/xillybus_photoncount', 'r')
    control_fd = os.open('/dev/xillybus_timeout_control', os.O_WRONLY)
    status_fd = open('/dev/xillybus_status', 'r')
    if(control_fd>0):
        os.lseek(control_fd, 4, os.SEEK_SET)
        byte_dwell= struct.pack('<I', dwell)
        os.write(control_fd, byte_dwell)
        byte_sweep = struct.pack('<I', sweep)
        os.write(control_fd, byte_sweep)
        change_ctrl(control_fd, WAIT_NSTART)
    
    return count_fd, control_fd, status_fd


def change_ctrl(control_fd, ctrl_val):
    os.lseek(control_fd, 0, os.SEEK_SET)
    os.write(control_fd, chr(ctrl_val))

    
def count(control_fd, count_fd, status_fd, dwell, sweep):
    change_ctrl(control_fd, WAIT_NSTART)
    change_ctrl(control_fd, WAIT_START)
    done = 0
    while (done==0):
        wait_time = (float(sweep))/1000000
        time.sleep(wait_time)
        status_fd.seek(0)
        done, = struct.unpack('<I', status_fd.read(4))
        
    change_ctrl(control_fd, WAIT_NSTART)
    count_list = []
    length = sweep/dwell
    count_fd.seek(0)
    while(len(count_list)<length):    
        count, = struct.unpack('<I', count_fd.read(4))
        count_list.append(count)

    change_ctrl(control_fd, NWAIT_NSTART)

    return count_list

def close(control_fd, count_fd, status_fd):
    os.close(control_fd)
    count_fd.close()
    status_fd.close()

    
def get_count(dwell=100, sweep=1000):
    count_fd, control_fd = open_counter(dwell, sweep)
    counts = count(control_fd, count_fd, status_fd, sweep)
    close(control_fd, count_fd, status_fd)
    if counts!=None:
        return counts
    else:
        return get_count(dwell, sweep)

