from Gpib import *
import time
import counter as c

INT_TIME = 10
DEVICE_NAME = 0
PRIMARY_ADDR = 5
LOOPTILL = 500
INIT_DLY = 0
END_DLY = 70
FILENAME = 'dll_swp.csv'

datalist=[]

delay_fd =  Gpib(name =DEVICE_NAME, pad =PRIMARY_ADDR)

delay_fd.write("DLY {}".format(INIT_DLY))

start = time.clock()

delay_fd.write("DLY {}".format(END_DLY))

for i in range (0,LOOPTILL):
    count_fd, control_fd = c.open_counter(INT_TIME)
    count =c.count(control_fd, count_fd, INT_TIME)
    datalist.append([count, time.clock()-start])
    c.close(control_fd, count_fd)
    print('{},{}'.format(count,time.clock()-start))

save = open(FILENAME, 'w+')
save.write('count, time\n')

for data in datalist:
    save.write('{}, {}\n'.format(data[0],data[1]))

save.close()
