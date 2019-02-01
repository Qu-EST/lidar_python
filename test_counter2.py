import mirror as m
import counter as c
import time

mems = m.open_mirror()
m.set_pos(mems, -0.035 ,-0.035)
save_file = open("moduleStability2.csv", 'w')
start = time.clock()
TDC = 100000
for x in range(0,5000):
#    m.set_pos(mems, 0.05, 0.05)
    #count_fd, control_fd = c.open_counter(100)
#    m.set_pos(mems, 0, 0)
    count = c.get_count(TDC)
    data = "{}\n".format(count)

    save_file.write(data)
    print data
    time.sleep(100.0/1000)
    #c.close(control_fd, count_fd)
    
print time.clock()-start
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
