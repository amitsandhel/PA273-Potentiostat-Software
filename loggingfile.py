
#loggingfile.py

import sys
import time
import logging


'''Created by Amit Sandhel on 2013-05-27. With contributions by Fredrick Leber.

Note: this program requires:
        1) Python 2.7
'''

    
class Logging_File():
    def __init__(self, logger_name, log_file, level=logging.DEBUG):
        self.log_file = log_file
        self.level = level
        self.l = logging.getLogger(logger_name)
        self.setup_logger()
        
    def setup_logger(self): #, logger_name, log_file, level=logging.DEBUG):
        """This function is designed for logging setup"""
        formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
        
        fileHandler = logging.FileHandler(self.log_file, mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        
        self.l.setLevel(self.level)
        self.l.addHandler(fileHandler)
        
        #uncommenting this line below allows you to print all the logs to the dos terminal
        #self.l.addHandler(streamHandler)  



