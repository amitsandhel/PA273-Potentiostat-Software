import logging
import random

# !/usr/bin/python
# encoding: utf-8
# Fake_Serial.py

"""This class is the fake serial class for the simulator. It will allow us to
bypass the serial port, and also will be used for all the memory address swaps
we need for both potentiostat versions.

Created by Amit Sandhel
This module is to probe a COM port for the PA273 potentiostat
"""

# making a logging file
logging.basicConfig(filename='Fake_Serial.log', filemode='a',
                    level=logging.DEBUG, format='%(asctime)s, \
                    %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")

# name for the log file
logging1 = logging.getLogger('Fake_Serial.log')


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

    def write(self, str_to_write):
        '''Fake sending a string to a serial device'''
        # TODO: Capture all sent text to a list
        # in case you want to check it later
        chars_sent = len(str_to_write)
        self.b = str_to_write.strip().split(" ")
        # Flush Rx buffer:
        self.reply = ""

        logging1.debug("SIM.write got " + repr(str_to_write))
        logging1.debug("SIM.write command parsed as: " + repr(self.b))

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

        # version 2 commands
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

        logging1.debug("EGAIN_SIM PARAM: " + repr(param))
        logging1.debug("EGAIN_SIM RECEIVED: " + repr(self.egain))

    def Igain_Sim(self, param=None):
        self.reply = ""

        if param in [1, 5, 10, 50]:
            self.igain = param
            self.reply = str(self.igain) + "*"

        if param is None:
            param = self.igain
            self.reply = str(self.igain) + "*"

        logging1.debug("IGAIN_SIM PARAM: " + repr(param))
        logging1.debug("IGAIN_SIM RECEIVED: " + repr(self.egain))

    def Bias_Sim(self, param=None):
        if param in range(-8000, 8000):
            self.bias = param
            self.reply = str(self.bias) + "*"

        if param is None:
            param = self.bias
            self.reply = str(self.bias) + "*"

        logging1.debug("BIAS_SIM PARAM: " + repr(param))
        logging1.debug("BIAS_SIM RECEIVED: " + repr(self.egain))

    def As_Sim(self, param=None):
        self.reply = ""
        param = -2
        self.As = param
        self.reply = str(self.As) + "*"

        logging1.debug("AS_SIM PARAM: " + repr(param))
        logging1.debug("AS_SIM RECEIVED: " + repr(self.egain))

    def Sie_Sim(self, param=None):
        self.reply = ""
        param = 300
        self.Sie = param
        self.reply = str(self.Sie) + "*"

        logging1.debug("SIE_SIM PARAM: " + repr(param))
        logging1.debug("SIE_SIM RECEIVED: " + repr(self.egain))

    def Sete_Sim(self, param=None):
        self.reply = ""
        param = 1000
        self.Sete = param
        self.reply - str(self.Sete) + "*"

        logging1.debug("SETE_SIM PARAM: " + repr(param))
        logging1.debug("SETE_SIM RECEIVED: " + repr(self.egain))

    # version 2 commands
    def NC_Sim(self, param=None):
        self.reply = ""
        param = 2
        self.NC = param
        self.reply = str(self.NC) + "*"

        logging1.debug("NC_SIM PARAM: " + repr(param))
        logging1.debug("NC_SIM RECEIVED: " + repr(self.NC))

    def TP_Sim(self, param=None):
        self.reply = ""
        # adding a random generator to generate a random current value output
        # param = [1,x,0]
        param = random.randrange(100, 999)
        self.TP = param / 100.0
        self.reply = str(self.TP) + "*"

        logging1.debug("TP_SIM PARAM: " + repr(param))
        logging1.debug("TP_SIM RECEIVED: " + repr(self.TP))

    def inWaiting(self):
        logging1.debug("SIM.inWaiting has '" + str(self.reply) +
                       "', returning %d" % len(self.reply))
        return len(self.reply)

    def read(self, chars_to_send):
        logging1.debug("SIM.read: asked for " + str(chars_to_send) +
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
