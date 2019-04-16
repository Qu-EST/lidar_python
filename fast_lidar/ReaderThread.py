'''This thread reads the data from the fifo and puts it to the queue if not DEADBEEF'''

from threading import Thread, Event
from queue import Queue
from LidarData import LidarData
import struct


class ReaderThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lidar_data = LidarData()
        self.switch = Event()
        self.switch.clear()
        # open the fifo
        self.count_file = open(self.lidar_data.photoncount_file, 'rb')


    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            raw_count = self.count_file.read(4)
            count, = struct.unpack('<I', raw_count)
            if((count != 0xDEADBEEF) ):
                if(count != 0xBAADF00D):
                    print(count)
                    self.lidar_data.data_queue.put(count)
            
        # close the fifo
        self.count_file.close()
    def off(self):
        '''this will be called to close the thread'''
        self.switch.set()
