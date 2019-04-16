import matplotlib.pyplot as plt
import matplotlib.animation as animation
import counter3 as c

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
counts =[0]
y=[0.0]


def animate(i, counts, y):
    count = c.get_count(200)
    counts.append(count)
    y.append(y[-1]+0.5)

    counts = counts[-20:]
    y=y[-20:]

    ax.clear()
    ax.plot( y, counts)

    plt.title('QuEST LIDAR - Turbulance live graph')
    plt.xlabel('Time in second')
    plt.ylabel('Photon counts')

ani = animation.FuncAnimation(fig, animate, fargs=(counts, y), interval=100)
plt.show()
