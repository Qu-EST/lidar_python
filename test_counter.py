import counter as c

count_fd, control_fd = c.open_counter(10)

print c.count(control_fd, count_fd, 10)
c.close(control_fd, count_fd)
