import mirror as m
import counter as c
import time

mems = m.open_mirror()
m.set_pos(mems, -0.02 ,0.12)
save_file = open("hotTurbulence.csv", 'w')
start = time.clock()
TDC = 5000
for x in range(0,2000):


start = time.clock()

#    m.set_pos(mems, 0.05, 0.05)
    #count_fd, control_fd = c.open_counter(5000)
    count = c.get_count(5000)
#    m.set_pos(mems, 0, 0)
    print count #c.count(control_fd, count_fd, 5000)
    time.sleep(210.0/1000)
   # c.close(control_fd, count_fd)
print time.clock()-start#    m.set_pos(mems, 0.05, 0.05)

save_file.close()

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
