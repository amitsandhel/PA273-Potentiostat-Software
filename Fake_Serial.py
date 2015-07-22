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
        '''This function is called when the class is first instantiated.'''
        self.reply = ""
        self.bias = 0
        self.b = None
        self.list = []
        self.Q = 0
        self.reade = 0
        self.readi = 0

    def write(self, str_to_write):
        '''Fake sending a string to a serial device'''
        # TODO: Capture all sent text to a list
        # in case you want to check it later
        chars_sent = len(str_to_write)
        self.b = str_to_write.strip().split(" ")
        # Flush Rx buffer:
        self.reply = ""

        if self.b[0] == 'BIAS' or self.b[0] == 'SETE':
            if len(self.b) == 2:
                self.e = float(self.b[1])
                self.Bias_Sim(self.e)
            else:
                self.Bias_Sim()

        elif self.b[0] == 'Q':
                self.Q_Sim()

        elif self.b[0] == 'READE':
                self.READE_Sim()

        elif self.b[0] == 'READI':
                self.READI_Sim()

        else:
            print 'NOT HANDLING CALL', repr(self.b)

        return chars_sent  # this is a constant

    def Bias_Sim(self, param=None):
        if param in range(-8000, 8000):
            self.bias = param
            self.reply = str(self.bias) + "*"

        if param is None:
            param = self.bias
            self.reply = str(self.bias) + "*"

    def current_Mag_Sim(self):
        # scales the current with the BIAS
        if abs(self.bias / 1000.0) >= 1:
            return str(-2)
        elif abs(self.bias / 100.0) >= 1:
            return str(-3)
        elif abs(self.bias / 10.0) >= 1:
            return str(-4)
        else:
            return str(-5)

    def bias_Noise_Sim(self):
        param = random.randrange(50, 100)  # 'random noise'
        param = param / 100.0  # now we have a value between 0.5 and 1

        # the random noise can be negative or positive
        if random.randrange(0, 1) == 1:
            param = param * -1

        # tolerance for the voltage is 10mV. Multiplying because
        # noise will likely be less than maximum possible
        return int(10 * param)

    def Q_Sim(self):
        self.Q = 50
        self.reply = str(self.Q) + "," + str(10) + "*"

    def READE_Sim(self):
        self.reply = str(self.bias + self.bias_Noise_Sim()) + "*"

    def READI_Sim(self):
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

        self.readi = param + adjBIAS
        self.reply = str(self.readi) + "," + str(self.current_Mag_Sim()) + "*"

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
