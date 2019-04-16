import matplotlib.pyplot as plt
import matplotlib.animation as animation
import counter3 as c

x_len=200
y_range=[10,40]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
counts = list(range(0,200))
y=[0.0]*x_len
ax.set_xlim(y_range)

line, = ax.plot(counts,y)

plt.title('QuEST LIDAR - Turbulance live graph')
plt.xlabel('Time in second')
plt.ylabel('Photon counts')


def animate(i, counts):
    count = c.get_count(200)
    counts.append(count)


    counts = counts[-x_len:]


    line.set_ydata(counts)

    return line,
    
ani = animation.FuncAnimation(fig, animate, fargs=(counts, ), interval=100, blit=True)
plt.show()
