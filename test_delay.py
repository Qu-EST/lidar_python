from Gpib import *
d = Gpib(name =0, pad =5)
d.write("DLY 70")
