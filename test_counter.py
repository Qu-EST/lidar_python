import counter

count_fd, control_fd = open_counter(10)

print count(control_fd, count_fd, 10)
