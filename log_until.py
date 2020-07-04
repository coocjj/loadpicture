from LoadCq9Photo.hand_cfg import Hand_cfg
import logging
import threading
import time,os
from logging.handlers import RotatingFileHandler

class LogSignleton(object):
    def __new__(cls):
        mutex = threading.Lock()
        mutex.acquire()#上锁，防止多线程下出问题
        if not hasattr(cls,'instance'):
            cls.instance = super(LogSignleton,cls).__new__(cls)
            current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_path = current_path + '\\Logs'
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            cls.instance.log_filename = os.path.join(log_path, time.strftime('%Y-%m-%d %H-%M-%S'+'.log', time.localtime()))
            hd = Hand_cfg()
            cls.instance.max_bytes_each = int(hd.get_config('LOGGING','max_bytes_each'))
            cls.instance.backup_count = int(hd.get_config('LOGGING','backup_count'))
            cls.instance.fmt = hd.get_config('LOGGING','fmt')
            cls.instance.log_level = int(hd.get_config('LOGGING','log_level'))
            cls.instance.logger_name = hd.get_config('LOGGING','logger_name')
            cls.instance.console_log_on = int(hd.get_config('LOGGING','console_log_on'))
            cls.instance.logfile_log_on = int(hd.get_config('LOGGING', 'logfile_log_on'))
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
        mutex.release()
        return cls.instance


    def get_logger(self):
        self.logger.setLevel(self.log_level)
        return self.logger


    def __config_logger(self):
        fmt = self.fmt.replace('|','%')
        formatter = logging.Formatter(fmt)

        if self.console_log_on == 1:
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)

        if self.logfile_log_on == 1:
            rt_file_handle = RotatingFileHandler(self.log_filename,maxBytes=self.max_bytes_each,backupCount=self.backup_count)
            rt_file_handle.setFormatter(formatter)
            self.logger.addHandler(rt_file_handle)

lg = LogSignleton()
logger = lg.get_logger()








