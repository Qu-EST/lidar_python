'''This thread reads the data from the fifo and puts it to the queue if not DEADBEEF'''

from threading import Thread, Event
from queue import Queue
from LidarData import LidarData


class ReaderThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lidar_data = LidarData()
        self.switch = Event()
        self.switch.clear()
        # open the fifo



    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            pass
        # close the fifo

    def off(self):
        '''this will be called to close the thread'''
        self.switch.set()
