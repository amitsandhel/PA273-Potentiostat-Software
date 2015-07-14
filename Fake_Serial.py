# !/usr/bin/python
# encoding: utf-8
# Fake_Serial.py

import logging
import random

#import logging library 
from loggingfile import Logging_File as Log_File


"""This class is the fake serial class for the simulator. It will allow us to
bypass the serial port, and also will be used for all the memory address swaps
we need for both potentiostat versions.

Created by Amit Sandhel with contributions by Fredrick Leber
This module is to simulate a COM port for the PA273 potentiostat.
"""

"""
Note that we have used PEP8 standard notation.
Therefore instead of using if x == y we write if x is y
"""

# making a logging file

#Logging Setup
"""NOTE:: the file path is to be manually set to the folder or the path directory you wish to save this too logging file must also be in 
there """
Log_File('Fake_Serial', r'F:\beastie_python_version 4\Logging\Fake_Serial.log')




class Fake_Serial():
    """Fake serial class for simulator development and testing. This serial
    class mimicks a serial port. When the user uses the -s setting,
    Fake_Serial() is the class used.
    """
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout,
                 xonxoff, rtscts, writeTimeout, dsrdtr, interCharTimeout):
        '''This function is called when a class is first instantiated'''
        self.reply = ""
        self.bias = 0
        self.egain = 0
        self.b = None
        self.igain = 0
        self.As = 0
        self.Sie = 0
        self.Sete = 0
        self.list = []

        # version 2 commands
        self.NC = 0
        self.As = 0
        self.TP = 0
        self.port = port
        
        self.logging1 = logging.getLogger('Fake_Serial')
        self.logging1.info(" ---------------------- root --------------------------------")
        
        self.logging1.debug("SIM.write got " + repr(self.port))

    def write(self, str_to_write):
        '''Fake sending a string to a serial device'''
        # TODO: Capture all sent text to a list
        # in case you want to check it later
        chars_sent = len(str_to_write)
        self.b = str_to_write.strip().split(" ")
        # Flush Rx buffer:
        self.reply = ""

        self.logging1.debug("SIM.write got " + repr(str_to_write))
        self.logging1.debug("SIM.write command parsed as: " + repr(self.b))

        if self.b[0] == 'EGAIN':
            if len(self.b) == 2:
                self.c = float(self.b[1])
                self.Egain_Sim(self.c)
            else:
                self.Egain_Sim()

        elif self.b[0] == 'IGAIN':
            if len(self.b) == 2:
                self.d = float(self.b[1])
                self.Igain_Sim(self.d)
            else:
                self.Igain_Sim()

        elif self.b[0] == 'BIAS':
            if len(self.b) == 2:
                self.e = float(self.b[1])
                self.Bias_Sim(self.e)
            else:
                self.Bias_Sim()

        elif self.b[0] == 'AS':
            if len(self.b) == 2:
                self.As_Sim(self.b[1])
            else:
                self.As_Sim()

        elif self.b[0] == 'SIE':
            if len(self.b) == 3:
                self.Sie_Sim(self.b[2])
            else:
                self.Sie_Sim()

        elif self.b[0] == 'SETE':
            if len(self.b) == 2:
                self.Sete_Sim(self.b[1])
            else:
                self.Sete_Sim()

        #Version 2 commands below
        
        elif self.b[0] == 'NC':
            if len(self.b) == 2:
                self.NC_Sim(self.b[1])
            else:
                self.NC_Sim()

        elif self.b[0] == 'TP':
            if len(self.b) == 2:
                self.TP_Sim(self.b[1])
            else:
                self.TP_Sim()

        else:
            print 'NOT HANDLING CALL', repr(self.b)

        return chars_sent  # this is a constant

    def Egain_Sim(self, param=None):
        self.reply = ""

        if param in [1, 5, 10, 50]:
            self.egain = param
            self.reply = str(self.egain) + "*"

        if param is None:
            param = self.egain
            self.reply = str(self.egain) + "*"

        self.logging1.debug("EGAIN_SIM PARAM: " + repr(param))
        self.logging1.debug("EGAIN_SIM RECEIVED: " + repr(self.egain))

    def Igain_Sim(self, param=None):
        self.reply = ""

        if param in [1, 5, 10, 50]:
            self.igain = param
            self.reply = str(self.igain) + "*"

        if param is None:
            param = self.igain
            self.reply = str(self.igain) + "*"

        self.logging1.debug("IGAIN_SIM PARAM: " + repr(param))
        self.logging1.debug("IGAIN_SIM RECEIVED: " + repr(self.egain))

    def Bias_Sim(self, param=None):
        if param in range(-8000, 8000):
            self.bias = param
            self.reply = str(self.bias) + "*"

        if param is None:
            param = self.bias
            self.reply = str(self.bias) + "*"

        self.logging1.debug("BIAS_SIM PARAM: " + repr(param))
        self.logging1.debug("BIAS_SIM RECEIVED: " + repr(self.egain))

    def As_Sim(self, param=None):
        self.reply = ""
        # param = -2 just an arbitrary initialization

        # scales the current with the BIAS
        if abs(self.bias / 1000.0) >= 1:
            self.As = -1
        elif abs(self.bias / 100.0) >= 1:
            self.As = -2
        elif abs(self.bias / 10.0) >= 1:
            self.As = -3
        else:
            self.As = -4

        self.reply = str(self.As) + "*"

        self.logging1.debug("AS_SIM PARAM: " + repr(param))
        self.logging1.debug("AS_SIM RECEIVED: " + repr(self.egain))

    def Sie_Sim(self, param=None):
        self.reply = ""
        param = 300
        #param = random.randrange(-1000, 1000)
        self.Sie = param
        self.reply = str(self.Sie) + "*"

        self.logging1.debug("SIE_SIM PARAM: " + repr(param))
        self.logging1.debug("SIE_SIM RECEIVED: " + repr(self.egain))

    def Sete_Sim(self, param=None):
        self.reply = ""
        param = 1000
        self.Sete = param
        self.reply - str(self.Sete) + "*"

        self.logging1.debug("SETE_SIM PARAM: " + repr(param))
        self.logging1.debug("SETE_SIM RECEIVED: " + repr(self.egain))

    # version 2 commands
    def NC_Sim(self, param=None):
        self.reply = ""
        param = 2
        self.NC = param
        self.reply = str(self.NC) + "*"

        self.logging1.debug("NC_SIM PARAM: " + repr(param))
        self.logging1.debug("NC_SIM RECEIVED: " + repr(self.NC))

    def TP_Sim(self, param=None):
        self.reply = ""
        # adding a random generator to generate a random current value output
        # param = [1,x,0]
        param = random.randrange(100, 999)  # 'random noise'

        # the random noise can be negative or positive
        neg = random.randrange(0, 1)
        if neg == 1:
            param = param * -1

        # this scales the current with the BIAS
        if abs(self.bias / 1000.0) >= 1:
            adjBIAS = self.bias / 1000.0
            param = param / 1000.0
        elif abs(self.bias / 100.0) >= 1:
            adjBIAS = self.bias / 100.0
            param = param / 100.0
        elif abs(self.bias / 10.0) >= 1:
            adjBIAS = self.bias / 10.0
            param = param / 10.0
        else:
            adjBIAS = self.bias

        self.TP = param + adjBIAS
        val = param + adjBIAS
        #self.TP = 0, val, 0
        self.reply = str(1)+','+str(self.TP)+','+ str(0)  + "*"

        self.logging1.debug("TP_SIM PARAM: " + repr(param))
        self.logging1.debug("TP_SIM RECEIVED: " + repr(self.TP))

    def inWaiting(self):
        self.logging1.debug("SIM.inWaiting has '" + str(self.reply) +
                       "', returning %d" % len(self.reply))
        return len(self.reply)

    def read(self, chars_to_send):
        self.logging1.debug("SIM.read: asked for " + str(chars_to_send) +
                       " returned: " + str(self.reply))
        rtn = self.reply[0:chars_to_send]
        self.reply = self.reply[chars_to_send:]
        return rtn

    def close(self):
        # closes the virtual serial port
        pass

###############################################################################
# if __name__ == '__main__':
    # Fake_Serial()
