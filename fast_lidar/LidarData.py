from queue import Queue
from queue import LifoQueue

class Singleton(type):
    '''Metaclass for the singleton'''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]




class LidarData(metaclass = Singleton):
    ''' data to be shared between the modules'''
    def __init__(self):
        self.data_queue = Queue(1000)
        self.args = None
        self.control_file = '/dev/xillybun_timeout_control'
        self.photoncount_file = '/dev/xillybun_status_photoncount'
        # self.dual_time = None
        # self.file_name = None
        # self.pixel_count = None
