import counter as c
import time
start = time.clock()
for x in range(0,1000):
    count_fd, control_fd = c.open_counter(10)
#for x in range(0, 100):
    print c.count(control_fd, count_fd, 10)
    time.sleep(1000.0/1000)
    #c.close(control_fd, count_fd)
print time.clock()-start
