import mirror as m
import counter as c
import time

mems = m.open_mirror()
m.set_pos(mems,-0.02 ,0.3)

start = time.clock()
for x in range(0,500):
#    m.set_pos(mems, 0.05, 0.05)
    count_fd, control_fd = c.open_counter(200000)
#    m.set_pos(mems, 0, 0)
    print c.count(control_fd, count_fd, 200000)
    time.sleep(210.0/1000)
    c.close(control_fd, count_fd)
print time.clock()-start

"""
m.set_pos(mems,-0.3,0.3)
for x in range(0,100):
    m.set_pos(mems, 0.05, 0.05)
    count_fd, control_fd = c.open_counter(100)
    m.set_pos(mems, 0, 0)
    print c.count(control_fd, count_fd, 100)
    time.sleep(100.0/1000)
    c.close(control_fd, count_fd)
"""




mems = m.close_mirror(mems)
