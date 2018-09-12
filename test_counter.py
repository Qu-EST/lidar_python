import counter as c
import time

#for x in range(0,10000):
count_fd, control_fd = c.open_counter(10)
print c.count(control_fd, count_fd, 10)
time.sleep(10.0/1000)
c.close(control_fd, count_fd)
