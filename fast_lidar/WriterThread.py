'''This thread writes the data to the file from the queue'''

from threading import Thread, Event
from queue import Queue
from LidarData import LidarData


class WriterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lidar_data = LidarData()
        self.switch = Event()
        self.switch.clear()
        #open the file



    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            pass
        # close the file

    def off(self):
        '''this will be called to close the thread'''
        self.switch.set()
