import random

"""Fake_Serial.py
Created by Amit Sandhel with contributions by Fredrick Leber
This module is to simulate a COM port for the PA273 potentiostat.

This class is the fake serial class for the simulator. It will allow us to
bypass the serial port, and also will be used for all the memory address swaps
we need for both potentiostat versions.
"""


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
        self.Q = 0
	self.reade = 0
	self.readi = 0

        # version 2 commands
        self.NC = 0
        self.As = 0
        self.TP = 0
        self.port = port

    def write(self, str_to_write):
        '''Fake sending a string to a serial device'''
        # TODO: Capture all sent text to a list
        # in case you want to check it later
        chars_sent = len(str_to_write)
        self.b = str_to_write.strip().split(" ")
        # Flush Rx buffer:
        self.reply = ""

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

        elif self.b[0] == 'Q':
            if len(self.b) == 2:
                self.Q_Sim(self.b[1])
            else:
                self.Q_Sim()
	
	elif self.b[0] == 'READE':
            if len(self.b) == 2:
                self.READE_Sim(self.b[1])
            else:
                self.READE_Sim()
		
	elif self.b[0] == 'READI':
            if len(self.b) == 2:
                self.READI_Sim(self.b[1])
            else:
                self.READI_Sim()

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

    def Igain_Sim(self, param=None):
        self.reply = ""

        if param in [1, 5, 10, 50]:
            self.igain = param
            self.reply = str(self.igain) + "*"

        if param is None:
            param = self.igain
            self.reply = str(self.igain) + "*"

    def Bias_Sim(self, param=None):
        if param in range(-8000, 8000):
            self.bias = param
            self.reply = str(self.bias) + "*"

        if param is None:
            param = self.bias
            self.reply = str(self.bias) + "*"

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

    def Sie_Sim(self, param=None):
        self.reply = ""
        param = 300
        # param = random.randrange(-1000, 1000)
        self.Sie = param
        self.reply = str(self.Sie) + "*"

    def Sete_Sim(self, param=None):
        self.reply = ""
        param = 1000
        self.Sete = param
        self.reply = str(self.Sete) + "*"

    def Q_Sim(self, param=None):
        self.reply = ""
        param = 50
        self.Q = param
        self.reply = str(self.Q) + "," + str(10) + "*"
        
    def READE_Sim(self, param=None):
        self.reply = ""
        param = 900
        self.reade = param
        self.reply = str(self.reade) + "*" #+ "," + str(10) + "*"

    def READI_Sim(self, param=None):
        self.reply = ""
        param = 600
        self.readi = param
        self.reply = str(self.readi) + "," + str(10) + "*"
    
    # version 2 commands
    def NC_Sim(self, param=None):
        self.reply = ""
        param = 2
        self.NC = param
        self.reply = str(self.NC) + "*"

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
        self.reply = str(1) + ',' + str(self.TP) + ',' + str(0) + "*"

    def inWaiting(self):
        return len(self.reply)

    def read(self, chars_to_send):
        rtn = self.reply[0:chars_to_send]
        self.reply = self.reply[chars_to_send:]
        return rtn

    def close(self):
        # closes the virtual serial port
        pass

###############################################################################
# if __name__ == '__main__':
    # Fake_Serial()
