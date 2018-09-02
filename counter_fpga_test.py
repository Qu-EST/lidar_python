import os
import struct

INT_TIME = 10
WAIT_NSTART = 2
WAIT_START = 3
NWAIT_NSTART = 0

count_fd = open('/dev/xillybus_status_photoncount', 'r')
control_fd = os.open('/dev/xillybus_timeout_control', os.O_WRONLY)
save = open('count.csv', 'w+')

def save_count(count_fd, control_fd, save):
    count_fd.seek(0)
    done, = struct.unpack('<I', count_fd.read(4))
    if(done==1):
        os.write(control_fd, chr(WAIT_NSTART))
        count, = struct.unpack('<I', count_fd.read(4))
        print count
        save.write(str(count)+'\n')
    else:
        # sleep(INT_TIME)
        get_count(count_fd, control_fd, save)

def change_ctrl(control_fd, ctrl_val):
    os.lseek(control_fd, 1, os.SEEK_SET)
    os.write(control_fd, chr(ctrl_val))
    
os.write(control_fd, chr(INT_TIME))
change_ctrl(control_fd, WAIT_NSTART)
change_ctrl(control_fd, WAIT_START)
save_count(count_fd, control_fd, save)
change_ctrl(control_fd, NWAIT_NSTART)
change_ctrl(control_fd, WAIT_NSTART)
change_ctrl(control_fd, WAIT_START)
    
