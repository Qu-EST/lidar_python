import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x","--xmin", type=float, help="X min value", default=0.5)
parser.add_argument("-X", "--xmax", type=float, help="X max value", default =1)
parser.add_argument("-y", "--ymin", type=float, help="Y min value", defalut=0.5)
parser.add_argument("-Y", "--ymax", type=float, help="Y max value", default=1)
parser.add_argument("-z", "--zmin", type=float, help="Z min value", defalut=0)
parser.add_argument("-Z", "--zmax", type=float, help="Z max value", default=200)
parser.add_argument('-s', '--xstep', type=float, help='x step size', default=0.1)
parser.add_argument('-u', '--ystep', type=float, help='y stepsize', default=0.1)
parser.add_argument('-m', '--zmicro', type=float, help='z micro step size', default=4)
parser.add_argument('-M', '--zmacro', type=float, help='z Macro step size', default=20)
parser.add_argument('-f', '--filename', type=str, help='filename to save the data', default='lidar.csv')
parser.add_argument('-t', '--tdc', type=int, help='tdc integration time', default=10)
parser.add_argument('-p', '--peakcheck', type=float, help='peak check', default=10)
parser.add_argument('-l', '--peakcheck', help='doing a normal lidar', action='store_true')
parser.add_argument('-v', '--verbose', help='print the verbose', action='store_true')


args=parser.parse_args()
