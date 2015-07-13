#!/usr/bin/python
# encoding: utf-8
#pa273_v1.py

import sys
import time
import logging
from main import setup_parser as sp
from Fake_Serial import Fake_Serial as fake_serial


'''Created by Amit Sandhel on 2013-05-27. With contributions by Fredrick Leber.

Note: this program requires:
        1) Python 2.7
        2) matplotlib
        3) logging-built in to Python
        4) PySerial
'''

# making a logging file
logging.basicConfig(filename='pa273v1.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")

# name for the log file
logging1 = logging.getLogger('pa273v1.log')


TIMEDELAY = 1

# SETTING UP CSV FILE
#TODO: make this name a file with the time/date sved 
FILENAME = "BOOK3.csv"
NEWLINE = "\n"


# Change COM PORT as needed, used by MySerialPort.open_port() function.
# String variable with word COM in caplocks in front is a must!
# example: "COM4", "COM2", "COM1", etc...
# Defaulted to COM4 here
defaultCOM = "COM5"


class MySerialPort(object):
    """Potentiostat class that reads the command file, and runs the command
    file from a serial port.
    """
    #note that we are passing in the egain, igain and bias settings in "real time
    # to the class directly for easier access 
    def __init__(self, egain, igain, bias):
        '''Initializing the variable so all functions can access the
        self.s port and remain open.
        '''
        self.s = None
        
        #these settings are needed to initalize the class so I can work with the class in the gui no choice must be here
        self.egain_val = egain
        self.igain_val = igain
        self.bias_val = bias

    def open_port(self, port=defaultCOM, baudrate=19200, bytesize=8,
                  parity='N', stopbits=1, timeout=1,
                  xonxoff=False, rtscts=False, writeTimeout=3, dsrdtr=False,
                  interCharTimeout=None):
        '''Open a self.s port, explicitly define all values to be sure
        they are set. Notes: I set a default read and write timeout of
        1 second to get it to respond quickly.
        '''
        self.s = Serial(port, baudrate, bytesize, parity, stopbits, timeout,
                        xonxoff, rtscts, writeTimeout, dsrdtr,
                        interCharTimeout)
        print('A serial port has been opened using ' + port + '.\n')
        logging1.debug('Serial Port opened using ' + port)

    def send(self, str_to_send):
        """sending commands to the serial port """
        chars_sent = self.s.write(str_to_send)
        logging1.debug("Tx: " + repr(str_to_send) +
                       "bytes sent: %d" % chars_sent)
        return chars_sent

    def receive(self, max_chars):
        '''Receive string with timeout and wait for end-of-message
        character or error.
        '''
        data_string = ""
        start_time = time.time()
        MAXRECEIVETIMEOUT = 3
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                if new_char == "*":
                    logging1.debug("Rx -  * received")
                    break
                elif new_char == "\r" or new_char == "\n":
                    '''Watch for other special characters like "\r \f".
                    Review your logs to see if anything else is embedded.
                    '''
                    pass
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                logging1.debug("Rx Receive timeout, returning what \
                I have and hoping")
                print "Receive function timed out."
                break
        time.sleep(0.5)
        logging1.debug("Rx: " + repr(data_string) +
                          " bytes read: %d" % len(data_string))
        
        if new_char == "?":
            logging1.debug("Rx - Error recieve, now what?")
        return data_string

    def close_port(self):
        '''closes the self.s port'''
        self.s.close()

    def egain(self):
        '''setting potential measurement gain ahead of analog-to-digital
        converter. Important in parsing data. PAGE 8-9: FUNCTION EGAIN
        '''
        print '(1:--> X1; 5:->X5; 10:-->X10; 50:-->X50)'
        #here we are using a try and except statement to catch the error so we can actually 
        #run it multiple times to save a code blowout explosion 
        try:
            #enter value
            x = input('ENTER EGAIN VALUE: ')
            if x == 1 or x==5 or x==10 or x==50:
                self.send("EGAIN %s  \n" % x)
                reply = self.receive(12)
                return reply
            else: 
                #if the above options are not done reneter the value force user
                print 'Please re-enter correct option'
                self.egain()
        #catchin all these errors
        except (NameError, ValueError, TypeError, SyntaxError, KeyboardInterrupt, SystemExit):
            print 'Please enter value again'
            self.egain()

    def igain(self):
        '''setting current measurement ahead of A-to-D converter
        f.s. = functional sensitivity
        PAGE 9-10: FUNCTION IGAI
        '''
        print '(1:--> X1; 5:->X5; 10:-->X10; 50:-->X50)'
        try:
            #enter value
            x = input('ENTER IGAIN VALUE: ')
            if x == 1 or x==5 or x==10 or x==50:
                self.send("IGAIN %s  \n" % x)
                reply = self.receive(12)
                return reply
            else:
                #if the above options are not done reneter the value force user
                print 'Please re-enter correct option'
                self.igain()
        #catchin all these errors
        except (NameError, ValueError, TypeError, SyntaxError, KeyboardInterrupt, SystemExit):
            print 'Please enter value again'
            self.igain()

    def bias(self):
        '''Setting the bias potential as soon as the cell is on.
        Reference: PAGE 15  BIAS[]
        '''
        try:
            #enter bias 
            x = input('Enter the Potential Bias to apply (mV) between -8000 mV to +8000 mV: ')
            self.send('BIAS %s \n' % x)
            reply = self.receive(20)  # 13 AT MAX VALUE
            return reply
        #catch all these values 
        except (NameError, ValueError, TypeError, SyntaxError, KeyboardInterrupt, SystemExit):
            print 'enter value again'
            self.bias()

    def measure_potential(self):
        '''Running the potentiostat to apply potential and measure the current,
        and then return the value directly to the computer. Note that each
        command is ran in single order due to ease and safety of command
        processing. The data is then saved into a dictionary directly, no
        if loop is required to check for error. However, note that two errors
        do exist. Also, note that all these commands are READ commands only; no
        writing is done in this function.
        '''
        self.send('EGAIN \n')
        a = self.receive(12)
        self.egainval = a.strip()

        self.send('IGAIN \n')
        b = self.receive(12)
        self.igainval = b.strip()

        self.send('AS \n')
        c = self.receive(12)
        self.asval = c.strip()

        self.send('SIE 1; A/D \n')
        f = self.receive(25)
        self.adval = f.strip()

        self.send('BIAS \n')
        g = self.receive(25)
        self.seteval = g.strip()

        # uncomment the lines below to access the command measures resistance
        # This command is not built in the simulator
        # self.send('Q \n')
        # h = self.receive(17)
        # self.qval=h.strip()

    def record_data(self):
        '''Records the data output into a csv file with the timestamp'''
        myfile = open(FILENAME, 'a')
        newrow = time.strftime('%H:%M:%S,')
        newrow += str(self.seteval) + ","  # applied potential
        newrow += str(self.egainval) + ","  # EGAIN SETTING
        newrow += str(self.igainval) + ","  # IGAIN SETTING
        newrow += str(self.asval) + ","  # CURRENT RANGE
        # newrow += str(self.eppval) + ","  # APPLIED POTENTIAL READOUT
        newrow += str(self.adval) + ","  # CURRENT READOUT
        # newrow += str(self.qval)  # CHARGE READOUT
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()
    
    def exp_setup(self):
        self.measure_potential()
        self.record_data()
        time.sleep(TIMEDELAY)

    def run(self):
        '''main while loop that controls, runs and executes all other commands
           running everything in this main excution function
           '''
        '''AMIT: HERE WE REMOVED THE ENTIRE MSVCRT LIBRARY AS IT IS A HINDERANCE AND AN ANNYOANCE 
           IT IS NOT PLATFORM INDEPENDENT AND DIFFICULT TO IMPLEMENT 
           BECAUSE OUR LAB EXPERIMENTS WILL BE SIGNIFICANTLY LONG THEY CAN EASILY BE STORED ON SEPARATE EXCEL 
           CSV FILES NO LOSS OR HARM HERE AT ALL 
           '''
           
        cycles = 1
        # self.open_port() # redundant, as the port has already been opened
        self.egain()
        self.igain()
        self.bias()

        '''changed from 'w' to 'a' to append files indefinitely to
        preexisting file
        '''
        myfile = open(FILENAME, "a")
        myfile.write("new data" + NEWLINE)
        myfile.write("Time, BIAS, EGAIN, IGAIN, I-RANGE, Eapp_READOUT, \
        Current_Readout, CHARGE(Q), Qexp" + NEWLINE)
        myfile.close()
        
        while True:
            #using a loop with a try and except to cancel and exit
            #exit is only done via a ctrl-c loop
            try:
                print "cycle", cycles
                cycles += 1
                self.exp_setup()
            except (KeyboardInterrupt, SystemExit, ValueError):
                print 'Closing software have a good day'
                break

"""AMIT: Keep this module here not at the top"""
module = sys.modules[__name__]

class Main():
    """Main class which executes the entire pa273_v1 script."""
    def __init__(self, parser):
        args = parser.parse_args()
        self.sim = args.sim  # sim parameter
        self.com = 'COM' + str(args.com)
        #opening the MySerialPort class with built in parameters
        self.myfile = MySerialPort(egain=1, igain=1, bias=1)

    def fake_serial(self):
        """Runs the Fake_Serial() Class if the simulator parameter is True."""
        print 'com parameter setting: ', self.com
        setattr(module, "Serial",  fake_serial)
        #setting com parameter with open_port() function
        self.myfile.open_port(self.com)
        #run the function
        self.myfile.run()
        # Closing serial port after run
        self.myfile.close_port()

    def run(self):
        if self.sim is True:
            #Running fake serial port 
            print 'Running simulator Mode: ', self.sim
            #rn the fake_serial() function
            self.fake_serial()  # opening serial port in simulator class only
            logging1.debug("FAKE/VIRTUAL SIM VALUE: " + repr(self.sim))
        else:  
            # run real serial port:
            print 'Running Real Serial: ', self.sim
            
            # Import real serial class
            from serial import Serial as Serial
            setattr(module, "Serial", Serial)
            #open serial port with comport option
            self.myfile.open_port(self.com)
            #run the function
            self.myfile.run()
            #close port
            self.myfile.close_port()
            
            logging1.debug("REAL SIM VALUE: " + repr(self.sim))

###############################################################################
if __name__ == '__main__':
    parser = sp()
    b = Main(parser)
    b.run()
