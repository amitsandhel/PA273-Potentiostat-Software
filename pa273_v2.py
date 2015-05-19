#!/usr/bin/python
# encoding: utf-8
#pa273_v2.py


"""
Created by Amit Sandhel.
This module is to probe a COM port for the PA273 potentiostat 

<<<<<<< HEAD
This script runs the potentiostat using a custom command language.
=======
This script runs the potentiostat script that operates the potentiostat
>>>>>>> origin/master
This script comes with a built in simulator which simulates the serial port if one is not present. Designed for testing and software development 
purposes
There are two serial classes Fake_Serial() class is a class that connects to a virtual/fake serial port. 
This class also is the simulator which simlates the potentiostat commands 
"""


'''References/ Sources of information used '''
#website references
#http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
#http://stackoverflow.com/questions/1429814/how-to-programmatically-set-a-global-module-variable  http://www.sitepoint.com/forums/showthread.php?1175398-Python-Django-Can-t-use-quot-setattr-quot-with-FileField
#http://stackoverflow.com/questions/1419470/python-init-setattr-on-arguments/1419950#1419950
#http://stackoverflow.com/questions/2933470/how-do-i-call-setattr-on-the-current-module
#https://www.inkling.com/read/learning-python-mark-lutz-4th/chapter-37/--getattr---and---getattribute--


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
import random

#import graphclass script for real-time graphing
from graphclass import GraphClass 

import subprocess
#import argparse for argparse commands
import argparse
from main import setup_parser as sp

'''Setting up logging'''
logging.basicConfig(filename='pa273v2.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root (%s) --------------------------------" % __file__)

#name for log file
logger2 = logging.getLogger('pa273v2.log')

#SETTING UP CSV FILE
FILENAME = "BOOK2.csv"
NEWLINE = "\n"


'''COM PORT SETTINGS
Change the com port setting to the com port value desired 
COM PORT SETTINGS CHANGE
NOTE: Must be STRING and have the  WORD "COM" in front of it in order to be used by MySerialPort.open_port() function
'''
'''STATIC DATA DO NOT TOUCH BASED ON POTENTIOSTAT MANUAL'''
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
    This serial class mimicks a serial port  
    when user uses the -s setting Fake_Serial() is the class used """     
    
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts,
                        writeTimeout, dsrdtr, interCharTimeout):
        '''This function is called when a class it first instantiated'''
        #potentiostat commands needed
        self.reply = ""
        self.bias = 0
        self.b = None
        self.NC = 0
        self.As  = 0
        self.TP = 0
    
    def write(self, str_to_write):
        '''Fake sending a string to a serial device'''
        #TODO: Capture all sent text to a list in case you want to check it later
        chars_sent = len(str_to_write)
        self.b = str_to_write.strip().split(" ")
        # Flush Rx buffer:
        self.reply = ""
            
        logger2.debug("SIM.write got " + repr(str_to_write)) 
        logger2.debug("SIM.write command parsed as: "  + repr(self.b))
           
        if self.b[0] == 'BIAS':
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
                    
        elif self.b[0] == 'NC':
            if len(self.b) ==2:
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

        return chars_sent # this is a constant
        
    def Bias_Sim(self, param=None):
        #Bias Command function
        if param in range(-8000,8000):
            self.bias = param
            self.reply = str(self.bias) + "*"
                
        if param == None:
            param = self.bias
            self.reply = str(self.bias)  +"*"
            
        logger2.debug("BIAS_SIM PARAM: " + repr(param))
        logger2.debug("BIAS_SIM RECEIVED: " + repr(self.bias))
        
    def As_Sim(self, param=None):
        #Current Command function
        self.reply = ""
        param = -4
        self.As = param
        self.reply = str(self.As) + "*"
            
        logger2.debug("AS_SIM PARAM: " + repr(param))
        logger2.debug("AS_SIM RECEIVED: " + repr(self.As))
        
        
    def NC_Sim(self, param = None):
        self.reply = ""
        param = 2
        self.NC = param
        self.reply = str(self.NC) + "*"
            
        logger2.debug("NC_SIM PARAM: " + repr(param))
        logger2.debug("NC_SIM RECEIVED: " + repr(self.NC))
            
    def TP_Sim(self, param = None):
        self.reply = ""
        #adding a random generator to generate a random current value output 
        x= random.randrange(0,2000)
        #param = [1,x,0]
        param1 = 1
        param2 = x
        param3 = 0
        self.TP = param2
        self.reply = str(self.TP) + "*"
            
        logger2.debug("TP_SIM PARAM: " + repr(param))
        logger2.debug("TP_SIM RECEIVED: " + repr(self.TP))
    
        
    def inWaiting(self):
        logger2.debug("SIM.inWaiting has '" + str(self.reply) + "', returning %d" %len(self.reply))
        return len(self.reply)
        
    def read(self, chars_to_send): 
        logger2.debug("SIM.read: asked for " + str(chars_to_send) + " returned: " + str(self.reply))
        rtn = self.reply[0:chars_to_send]
        self.reply = self.reply[chars_to_send:]
        return rtn

    def close(self):
        #closes the virtual serial port via a pass command
        pass


    
class MySerialPort():
    '''potentiostat class that reads the command file, runs the command file from a serial port 
    '''
    def __init__(self):
        # initializing the variable so all functions can access the self.s port and remain open
        self.s = None
        self.command_dict = {}
        self.cmd_output = None 
        self.next_cmd = None
        self.next_cmd_list = []
        
        #initalizing the values for graphclass
        self.elapsed_time = None 
        self.reply3 = None
        self.reply4 = None

        '''self variable that opens the pyplot graph class'''
        self.data = self.elapsed_time
        self.data2 = self.reply3
        self.data3= self.reply4
        
        self.mygraph = GraphClass(self.data, self.data2, self.data3)
     
    def my_ports():
        '''Call tool to detect and list all serial ports'''
        return list_ports.main()
        
    def open_port(self, port=COM, baudrate=19200, bytesize=EIGHTBITS, parity=PARITY_NONE,
                            stopbits=STOPBITS_ONE, timeout=1, xonxoff=False, rtscts=False,
                            writeTimeout=3, dsrdtr=False, interCharTimeout=None):
        '''Open a self.s port, explicitly define all values to be sure they are set'''
        # Notes I set a default read and write timeout of 1 seconds to get it to respond quickly 
        self.s = Serial(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts,
                            writeTimeout, dsrdtr, interCharTimeout)
        logger2.debug('Serial Port opened')
        
        
    def send(self, str_to_send):
        """sending commands to the serial port """
        chars_sent = self.s.write(str_to_send)
        logger2.debug("Tx: " + repr(str_to_send) + "bytes sent: %d" % chars_sent)
        return chars_sent
    
    def receive(self, max_chars):
        '''Receive string with timeout and wait for end-of-message character or error'''
        data_string = ""
        start_time = time.time()
        MAXRECEIVETIMEOUT = 0.05  # is this in seconds or milli seconds?  Look up time.now()
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                if new_char == "*":
                    logger2.debug("Rx -  * received")
                    break
                elif new_char == "\r" or new_char == "\n":
                    # watch for other special characters like "\r \f" review your logs to see if anything else is embedded.
                    pass 
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                logger2.debug("Rx Receive timeout, returning what I have and hoping")
                break
        time.sleep(0.05) #initallyo 0.01 was set to 0.5 
        logger2.debug("Rx: " + repr(data_string) + " bytes read: %d" % len(data_string))
        if new_char == "?":
            logger2.debug("Rx - Error receive, now what?")
            # should we break after an error?
            # break
        return data_string
    
    def close_port(self):
        '''closes the self.s port'''
        logger2.debug('Closing Serial Port')
        self.s.close()
    
    def readfiles(self):
        '''reading the command csv file called beastiecommandfile''' 
        file = "beastiecommand.csv"
        global command_list
        command_list = []
        readfile = open(file, "r")
        #print readfile 
        for line in readfile:
            command_list.append(line,)
            #return command_list
        logger2.debug("readfiles() timing response: " + repr(command_list))

    def parse_commands(self, command_list = None):   
        '''Pass in the command list and we return a command dictionary'''
        #parsing pass in command list
        for line in command_list:
            time, command = line.strip().split(",")
            try:
                if self.command_dict[float(time)]:
                    # Append to existing:
                    self.command_dict[float(time)] += (command.strip(),)
                else:
                    # Create first entry:
                    self.command_dict[float(time)] = (command.strip() , )
            except:
                # Create first entry:
                self.command_dict[float(time)] = (command.strip() , )
                
        logger2.debug("New command dict: " + repr(self.command_dict))
    
    def read_command(self):
        '''parsing the dictionary commands based on the timeout commands'''
        self.cmd_output = self.command_dict.keys()
        self.cmd_output.sort() 

        return self.cmd_output
        
    
    def get_next_command(self):
        '''This function is parsing the commands from the command file into a tupule '''
        next_time = self.cmd_output.pop(0)
        next_cmd = self.command_dict[next_time]
        reply = (next_time, next_cmd) 
        
        logger2.debug("get_next_command() reply timing response: " + repr(reply))
        return reply
    
    def command_execute(self, reply):
        '''Calling the reply from the function above get_next_command()'''
        self.send(reply[1] + " \n" )
        self.reply = self.receive(20)
        
        logger2.debug("command execute()reply timing response: " + repr(reply[1]))
    
    def always_read_commands(self):
        '''Commands that are always read all the time. All these commands are read commands only'''
        self.send("NC \n")
        self.reply1 = self.receive(4)
        logger2.debug("NC TIMER RESPONSE: " + repr(self.reply1))
        
        self.send("AS \n")
        self.reply2 = self.receive(4)
        logger2.debug("AS TIMER RESPONSE: " + repr(self.reply2))
                
        self.send("BIAS  \n")
        self.reply3 = self.receive(7)
        logger2.debug("BIAS TIMER RESPONSE: " + repr(self.reply3))
                
        self.send('TP \n')
        self.reply4 = self.receive(4)
        logger2.debug("TP TIMER RESPONSE: " + repr(self.reply4))
        
    def record_data(self, exceldata):
        '''recording the results into a csv file using local variables to increase process speed'''
        myfile = open(FILENAME, 'a')
        newrow = str(self.elapsed_time) + ',' 
        newrow += str(self.reply2) + "," 
        newrow += str(self.reply3) + ","  
        newrow += str(self.reply4) + ","  
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()


    def run(self): 
        '''main while loop that controls, runs and executes all other commands'''
        
        start_time = time.time()
        timer = time.time()  # timer for recording the data
        new_time = 0.0 #initalization value
        
        #opening and writing excel file writeable only 
        #therefore will rewrite ontop of existing file change to "a" for appending data
        myfile = open(FILENAME, "w")
        myfile.write("Time, AS, BIAS, TP-point#, TP-current, TP-bias, " + NEWLINE)
        myfile.close()
        
        logger2.debug('time_meter_command() myfile timing VALUE: '  + repr(myfile))
        self.readfiles()
        self.parse_commands(command_list)
        self.read_command()
 
        while True:
            #while loop that measures the elapsed time
            self.elapsed_time = time.time() - start_time
            exceldata = self.always_read_commands()
            self.record_data(exceldata)
            
            if time.time() - start_time >= new_time:
                if len(self.cmd_output) == 0:
                    break 
                newtime, newcmd = self.get_next_command()
                for item in newcmd:
                    reply = (newtime, item)
                    self.command_execute(reply)
                    
                    exceldata = self.always_read_commands()
                    self.record_data(exceldata)
                    
                    
                '''running the graphclass script to output the graph in real time '''
                self.mygraph.analysis(self.elapsed_time, self.reply3, self.reply4)
                logger2.debug('mygraph elapsed_time data: ' + repr(self.elapsed_time) )
                logger2.debug('mygraph self.reply3 data: ' + repr(self.reply3) )
                logger2.debug('mygraph self.reply4 data: ' + repr(self.reply4) )
                
                #updating the new_time from the tupule above
                new_time = newtime

#running the Main() class to execute everything off argparse

module = sys.modules[__name__]

class Main():
    """Main class which executes the entire pa273_v2 script"""
    
    def __init__(self, parser):
        args = parser.parse_args()
        self.sim = args.sim 
        
        #opening serial port
        self.myfile = MySerialPort()
    
    def fake_serial(self):
        '''runs the Fake_Serial() Class if simulator is True'''
        setattr(module, "Serial", Fake_Serial)
        self.myfile.open_port()
        self.myfile.run()
        '''closing serial port after run'''
        self.myfile.close_port()
        
    def run(self):
        if self.sim == True: 
            logging.debug("FAKE/VIRTUAL SIM VALUE: " + repr(self.sim) )
            print 'running sim: ', self.sim
            self.fake_serial()
            '''calling fake serial function opening serial port in simulator class only'''
            subprocess.call("postrun", shell = True)
        else:    
            #if self.sim == False run real serial port:
            logging.debug("REAL SIM VALUE: " + repr(self.sim) )
            print 'running real simulator: ',self.sim
            '''running real simulator function which imports real serial class'''
            from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

            setattr(module, "Serial", Serial)
            self.myfile.open_port()
            
            '''only calling the function below not open_port() '''
            self.myfile.run()
            self.myfile.close_port()
            subprocess.call("postrun", shell = True)


############################################################    
if __name__ == '__main__':
    parser = sp()
    b= Main(parser)
    b.run()  
