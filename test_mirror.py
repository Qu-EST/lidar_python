import mirror as m
import time
def frange(end,start=0,inc=0,precision=1):
    """A range function that accepts float increments."""
    import math

    if not start:
        start = end + 0.0
        end = 0.0
    else: end += 0.0
    
    if not inc:
        inc = 1.0
    count = int(math.ceil((start - end) / inc))

   # L = [None] * count
    L = []
    L.append(float(end))
   # L.append(end)
    for i in (xrange(1,count)):
        L.append(L[i-1] + inc)
    return L
mems = m.open_mirror()
i = -0.25
j = 0.06
k = -0.05
l = 0.15
ystep = 0.004
xstep = 0.05
#time.sleep(1)
ylist = [y for y in frange(k, l,ystep)]
xlist = [x for x in frange(i,j,xstep)]
for y in ylist:
    #rint(y)
    for x in xlist:
        print(x,y)
        m.set_pos(mems,x,y)
       #time.sleep(0.5)
   #time.sleep(0.20)
   #m.set_pos(mems,-0.05,y)
   #m.set_pos(mems,j,y)
   #time.sleep(0.2  )
        
time.sleep(1)
m.set_pos(mems,i,k)   
#m.set_pos(mems, 0,0)
#m.close_mirror(mems)
