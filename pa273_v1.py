#!/usr/bin/python
# encoding: utf-8
#pa273_v1.py

'''
Created by Amit Sandhel on 2013-05-27.
This module is to probe a COM port for the PA273 potentiostat 

'''

"""
Note: this program requires:
        1) Python 2.7
        2) Matplotlib
        3) NumPy
        4) SciPy
        4) math-built in to Pyton
        5) logging-built in to Python
"""

import sys
import time
import logging 
import subprocess

#import argparse for argparse commands
import argparse

from main import setup_parser as sp
import msvcrt

#making a logging file
logging.basicConfig(filename='pa273v1.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")

#name for the log file
logging1 = logging.getLogger('pa273v1.log')


#SETTING UP CSV FILE
FILENAME = "BOOK3.csv"
NEWLINE = "\n"

'''COM PORT SETTINGS
Change the com port setting to the com port value desired 
COM PORT SETTINGS CHANGE
NOTE: Must be STRING and have the  WORD "COM" in front of it in order to be used by MySerialPort.open_port() function
'''
'''STATIC DATA DO NOT TOUCH BASED ON POTENTIOSTAT MANUAL'''
TIMEDELAY = 1
EIGHTBITS = 8
PARITY_NONE = 'N'
STOPBITS_ONE = 1


#Change COM PORT AS NEEDED
#String varuiable with word COM in caplocks in front is a must
#example: "COM4", "COM2", "COM1", etc...
COM="COM4" #pick whichever com port your computer will need defaulted to COM4 here


#define the ports you have available
def list_ports():
    print "COM4"
    return ["COM4",]

class Fake_Serial():
    """Fake serial class for simulator development and testing
    this serial class mimicks a serial port  
    when user uses the -s setting Fake_Serial() is the class used """ 
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts,
                        writeTimeout, dsrdtr, interCharTimeout):
        '''This function is called when a class it first instantiated'''
        self.reply = ""
        self.bias = 0
        self.egain = 0
        self.b = None
        self.igain = 0
        self.As  = 0
        self.Sie = 0
        self.Sete = 0
        self.list = []

    def write(self, str_to_write):
        '''Fake sending a string to a serial device'''
        #TODO: Capture all sent text to a list in case you want to check it later
        chars_sent = len(str_to_write)
        self.b = str_to_write.strip().split(" ")
        # Flush Rx buffer:
        self.reply = ""
        
        
        logging1.debug("SIM.write got " + repr(str_to_write)) 
        logging1.debug("SIM.write command parsed as: "  + repr(self.b))
       
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
            if len(self.b) ==2:
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
                
        else:
            print 'NOT HANDLING CALL', repr(self.b)

        return chars_sent # this is a constant
    
    def Egain_Sim(self, param=None):
        self.reply = ""
        
        if param in [1,5,10,50]:
            self.egain = param
            self.reply = str(self.egain) + "*"
            
        if param == None:
            param = self.egain 
            self.reply = str(self.egain) + "*" 
        
        logging1.debug("EGAIN_SIM PARAM: " + repr(param))
        logging1.debug("EGAIN_SIM RECEIVED: " + repr(self.egain))
        
    
    def Igain_Sim(self, param=None):
        self.reply = ""
        
        if param in [1,5,10,50]:
            self.igain = param
            self.reply = str(self.igain) + "*"
        
        if param == None:
            param = self.igain
            self.reply = str(self.igain) + "*"
        
        logging1.debug("IGAIN_SIM PARAM: " + repr(param))
        logging1.debug("IGAIN_SIM RECEIVED: " + repr(self.egain))
        
    def Bias_Sim(self, param=None):
        if param in range(-8000,8000):
            self.bias = param
            self.reply = str(self.bias) + "*"
            
        if param == None:
            param = self.bias
            self.reply = str(self.bias)  +"*"
        
        logging1.debug("BIAS_SIM PARAM: " + repr(param))
        logging1.debug("BIAS_SIM RECEIVED: " + repr(self.egain))
    
    def As_Sim(self, param=None):
        self.reply = ""
        param = -4
        self.As = param
        self.reply = str(self.As) + "*"
        
        logging1.debug("AS_SIM PARAM: " + repr(param))
        logging1.debug("AS_SIM RECEIVED: " + repr(self.egain))
    
    
    def Sie_Sim(self, param = None):
        self.reply = ""
        param = 300
        self.Sie = param
        self.reply = str(self.Sie) + "*"
        
        logging1.debug("SIE_SIM PARAM: " + repr(param))
        logging1.debug("SIE_SIM RECEIVED: " + repr(self.egain))
        
    def Sete_Sim(self, param = None):
        self.reply = ""
        param = 1000
        self.Sete = param
        self.reply - str(self.Sete) + "*"
        
        logging1.debug("SETE_SIM PARAM: " + repr(param))
        logging1.debug("SETE_SIM RECEIVED: " + repr(self.egain))
    
    def inWaiting(self):
        logging1.debug("SIM.inWaiting has '" + str(self.reply) + "', returning %d" %len(self.reply))
        return len(self.reply)
    
    def read(self, chars_to_send): 
        logging1.debug("SIM.read: asked for " + str(chars_to_send) + " returned: " + str(self.reply))
        rtn = self.reply[0:chars_to_send]
        self.reply = self.reply[chars_to_send:]
        return rtn

    def close(self):
        #to close the virtual serial port
        pass


class MySerialPort():
    '''potentiostat class that reads the command file, runs the command file from a serial port 
    '''
    def __init__(self):
        # initializing the variable so all functions can access the self.s port and remain open
        self.s = None
    
    def my_ports():
        '''Call tool to detect and list all serial ports'''
        return list_ports.main()
        
    def open_port(self, port=COM, baudrate=19200, bytesize=EIGHTBITS, parity=PARITY_NONE,
                            stopbits=STOPBITS_ONE, timeout=1, xonxoff=False, rtscts=False,
                            writeTimeout=3, dsrdtr=False, interCharTimeout=None):
        '''Open a self.s port, explicitly define all values to be sure they are set'''
        # Notes I set a default read and write timeout of 1 seconds to get it to respond quickly 
        
        s = Serial(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts,
                            writeTimeout, dsrdtr, interCharTimeout)
        self.s = s

    def send(self, str_to_send):
        """sending commands to the serial port """
        chars_sent = self.s.write(str_to_send)
        logging1.debug("Tx: " + repr(str_to_send) + "bytes sent: %d" % chars_sent)
        return chars_sent
    
    def receive(self, max_chars):
        '''Receive string with timeout and wait for end-of-message character or error'''
        data_string = ""
        start_time = time.time()
        MAXRECEIVETIMEOUT = 3  # is this in seconds or milli seconds?  Look up time.now()
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                if new_char == "*":
                    logging1.debug("Rx -  * received")
                    break
                    
                elif new_char == "\r" or new_char == "\n":
                    # watch for other special characters like "\r \f" review your logs to see if anything else is embedded.
                    pass 
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                logging1.debug("Rx Receive timeout, returning what I have and hoping")
                break
        time.sleep(0.01)
                #logging1.debug("Rx: " + repr(data_string) + " bytes read: %d" % len(data_string))
        if new_char == "?":
            logging1.debug("Rx - Error recieve, now what?")
        return data_string
    
    def close_port(self):
        '''closes the self.s port'''
        self.s.close()

    def egain(self):
        '''setting potential measurement gain ahead of analog-to-digital converter
        important in parsing data
        PAGE 8-9: FUNCTION EGAIN
        '''
        print '(1:--> X1; 5:->X5; 10:-->X10; 50:-->X50)'
        x = input('ENTER EGAIN VALUE: ')
        self.send("EGAIN %s  \n" %x)
        reply = self.receive(12)
        print reply
        return reply
        
    def igain(self):
        '''setting current measurement ahead of A-to-D converter
        f.s. = functional sensitivity
        PAGE 9-10: FUNCTION IGAI
        '''
        print '(1:--> X1; 5:->X5; 10:-->X10; 50:-->X50)'
        x = input('ENTER IGAIN VALUE: ')
        self.send("IGAIN %s  \n" %x)
        reply = self.receive(12)
        print reply
        return reply

    def bias(self):
        '''setting the bias potential as soon as the cell is on
        PAGE 15  BIAS[]
        '''
        x = input('Enter the Potential Bias to apply (mV): ')
        self.send('BIAS %s \n'%x)
        reply = self.receive(20) #13 AT MAX VALUE
        print reply
        return reply
        
    def measure_potential(self):
        '''running the potentiostat to apply potential and measure the 
        current and then return the value directly to the computer
        Note that each command is ran in single order due to ease and safety of command processing 
        the data is then saved into a dictionary directly and no if loop is required to check for error
        however do note that two errors do exist
        Also note that all these commands are READ commands only no writing is done in this function
        '''
        self.send('EGAIN \n')
        a = self.receive(12)
        self.egainval=a.strip()
        
        
        self.send('IGAIN \n')
        b =self.receive(12)
        self.igainval=b.strip()
        
        
        self.send('AS \n')
        c = self.receive(12)
        self.asval=c.strip()
        
        
        self.send('SIE 1; A/D \n')
        f = self.receive(25)
        self.adval=f.strip()
      
        self.send('BIAS \n')
        g = self.receive(25)
        self.seteval=g.strip()
        
        #uncomment the lines below to access the command measures resistance 
        #This command is not built in the simulator
        #self.send('Q \n')
        #h = self.receive(17)
        #self.qval=h.strip()
        

    def record_data(self):
        '''this is to record the data output into a csv file with the timestamp'''
        myfile = open(FILENAME, 'a')
        newrow = time.strftime('%H:%M:%S,')
        newrow += str(self.seteval) + "," #applied potential
        newrow += str(self.egainval) + "," #EGAIN SETTING
        newrow += str(self.igainval) + "," #IGAIN SETTING
        newrow += str(self.asval) + "," #CURRENT RANGE
        #newrow += str(self.eppval) + "," #APPLIED POTENTIAL READOUT
        newrow += str(self.adval) + "," #CURRENT READOUT
        #newrow += str(self.qval)  #CHARGE READOUT
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()
    
    def run(self):
        '''main while loop that controls, runs and executes all other commands'''
        '''running everything in this main excution function'''
        cycles = 1
        
        self.open_port()
        self.egain()
        self.igain()
        self.bias()
        
        # changed from 'w' to 'a' to append files indefinitely to preexisting file
        myfile = open(FILENAME, "a")
        myfile.write("new data" + NEWLINE)
        myfile.write("Time, BIAS, EGAIN, IGAIN, I-RANGE, Eapp_READOUT, Current_Readout, CHARGE(Q), Qexp" + NEWLINE)
        myfile.close()
    
        first_run = True
        while True:
            print "cycle", cycles
            cycles += 1
            self.measure_potential()
            self.record_data()
            time.sleep(TIMEDELAY)
            #making a keyboard excution stop loop
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch.upper() == 'A' or first_run:
                    first_run = False
                    #re-running function commands 
                    self.egain()
                    self.igain()
                    self.bias()
                    myfile = open(FILENAME, "a")
                    myfile.write("NEW DATA" + NEWLINE)
                    myfile.write("Time, BIAS, EGAIN, IGAIN, I-RANGE, Eapp_READOUT, Current_Readout, CHARGE(Q), Qexp" + NEWLINE)
                    myfile.close()
                    
                #to quit the program in all entirely 
                elif ch.upper() == "Q":
                    self.close_port()
                    break

        
module = sys.modules[__name__]

class Main():
    """Main class which executes the entire beastie script"""
    def __init__(self, parser):
        args = parser.parse_args()
        self.sim = args.sim #sim parameter
    
        self.myfile = MySerialPort()
        
    def run(self):
        if self.sim == True:
            logging1.debug("FAKE/VIRTUAL SIM VALUE: " + repr(self.sim) )
            print 'running sim: ', self.sim
            
            '''calling fake serial function opening serial port in simulator class only'''
            setattr(module, "Serial", Fake_Serial)
            self.myfile.open_port()
            self.myfile.run() 
            
            '''closing serial port after run'''
            self.myfile.close_port()
            
        if self.sim == False:
            logging1.debug("REAL SIM VALUE: " + repr(self.sim) )
            
            print 'real sim result: ', self.sim
            
            '''running real simulator function which imports serial'''
            from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE 
            
            setattr(module, "Serial", Serial)
            self.myfile.open_port()
            self.myfile.run() 
            
            '''closing serial port after run'''
            self.myfile.close_port()
        
            
            
#####################################################################################  
if __name__ == '__main__':
    parser = sp()
    b= Main(parser)
    b.run()  
 
