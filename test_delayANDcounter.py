from Gpib import *
import counter as c
import time


d = Gpib(name =0, pad =5)

d.write("DLY 70")


count_fd, control_fd = c.open_counter(10)
print c.count(control_fd, count_fd, 10)

c.close(control_fd, count_fd)

count_fd, control_fd = c.open_counter(10)
print c.count(control_fd, count_fd, 10)
time.sleep(10.0/1000)
c.close(control_fd, count_fd)

d.write("DLY 0")

#for x in range(0,10000):
count_fd, control_fd = c.open_counter(10)
print c.count(control_fd, count_fd, 10)
time.sleep(10.0/1000)
c.close(control_fd, count_fd)

count_fd, control_fd = c.open_counter(10)
print c.count(control_fd, count_fd, 10)
time.sleep(10.0/1000)
c.close(control_fd, count_fd)
#time.sleep(2


 
