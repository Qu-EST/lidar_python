'''This thread writes the data to the file from the queue'''

from threading import Thread, Event
from queue import Queue
from LidarData import LidarData
import struct


class WriterThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lidar_data = LidarData()
        self.switch = Event()
        self.switch.clear()
        #open the file
        self.write_file = open(self.lidar_data.args.file_name, 'w')

        
        #number of pixels received
        self.received_pixels = 0


    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            self.write_file.write("{}\n".format(self.lidar_data.current_z))
            with self.lidar_data.frame_done:
                while self.received_pixels < self.lidar_data.args.pixel_count:
                    count_data = self.lidar_data.data_queue.get()
                    print("count: {} received: {} to get: {}".format(count_data, self.received_pixels,self.lidar_data.args.pixel_count ))
#                    print
                    self.received_pixels += 1
                    self.write_file.write("{}\n".format(count_data))
                self.lidar_data.frame_done.notify()
        
        # close the file
        self.write_file.close()
        
    def off(self):
        '''this will be called to close the thread'''
        self.switch.set()
