from serial import Serial
from Gpib import *

#Mirror constants
PORT = '/dev/ttyUSB0'
COMMANDMODE = '$MTI$\n'
VD = 'MTI+VD 125\n'
BW = 'MTI+BW 140\n'
VB = 'MTI+VB 80\n'             #Vbias
EN = 'MTI+EN\n'                # enable mirror
GT = 'MTI+GT '                 # Go to pos
OUT = ' 255\n'                 # out from the mirror
DISABLE = 'MTI+DI\n'
EX = 'MTI+EX\n'

def open_mirror():
    mirror = Serial()
    mirror.port = PORT
    mirror.baudrate = 115200
    mirror.open()

    
    #enable the terminal mode in mirror
    mirror.write(COMMANDMODE)
    status = mirror.readline()

    #check if the terminal mode is enabled
    if(status[:12]=='MTI-Device M'):

        #set the MIrror parameters
        mirror.write(VD)
        if(check_status(mirror)==0):
            mirror.write(VB)
            if(check_status(mirror)==0):
                mirror.write(BW)
                if(check_status(mirror)==0):
                    mirror.write(EN)
                    if(check_status(mirror)==0):
                        return mirror
    
    return -1

def check_status(mirror):
    status = mirror.readline()
    if(status == 'MTI-OK\r\n'):
        return 0
    else:
        return -1

def set_pos(mirror, x, y):
    mirror.write(GT+str(x)+' '+str(y)+OUT)
    if(check_status(mirror)==0):
        return 0
    return -1
    



def close_mirror(mirror):
    set_pos(mirror, 0, 0)
    mirror.write(DISABLE)
    mirror.write(EX)
    mirror.close()
    return 0

    
