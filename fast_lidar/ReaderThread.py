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
        deadbeef_count =0
        baadfood_count =0
        while not self.switch.is_set():
            raw_count = self.count_file.read(4)
            count, = struct.unpack('<I', raw_count)
            if(count == 0xDEADBEEF ):
                deadbeef_count += 1
                print(count)
            elif(count == 0xBAADF00D):
                baadfood_count += 1
                
                
            else:
             #   print(count)
                self.lidar_data.data_queue.put(count)
            if(deadbeef_count==1):
                print(count)
            # if(baadfood_count==1):
            #     print(count)

        # close the fifo
        self.count_file.close()
        print('total deadbeef: {}'.format(deadbeef_count))
        print("total baadfood: {}".format(baadfood_count))
    def off(self):
        '''this will be called to close the thread'''
        self.switch.set()
