import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import counter3 as c
import random

x_len=200
y_range=[10,40]

fig = plt.figure()
ax = fig.add_subplot(1,2,1)
ax1 = fig.add_subplot(1,2,2)
#counts = list(range(0,200))
y=[0.0]*x_len
ax.set_xlim(y_range)

#line, = ax.plot(counts,y)

plt.title('QuEST LIDAR - Turbulance live graph')
plt.xlabel('Time in second')
plt.ylabel('Photon counts')

def animate(i):
    graph_data = open('rng_test.txt').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',') #separate x,y in column
            #x = (round(float(x)/1000))
            y = (round(float(y)/1000))
            xs.append(x)
            ys.append(y)
            # histogram graph
            
    ax.clear()
    ax.plot(xs,ys,'ro') # scatter plot



#def animate(i, counts):
   # count = c.get_count(200)
   
#    counts.append(count)


#    counts = counts[-x_len:]


#    line.set_ydata(counts)

#    return line,
    
#ani = animation.FuncAnimation(fig, animate, fargs=(counts, ), interval=100, blit=True)
ani = animation.FuncAnimation(fig, animate, interval = 100)
plt.show()
