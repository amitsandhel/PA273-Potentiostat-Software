import sys
import time
from main import setup_parser as sp
from Fake_Serial import Fake_Serial as fake_serial

"""pa273_v1.py
Created by Amit Sandhel on 2013-05-27. With contributions by Fredrick Leber.

Note: this script requires:
        1) Python 2.7
        2) matplotlib
        3) PySerial
"""

TIMEDELAY = 1  # how long (in seconds) the exp_setup function sleeps for

# SETTING UP CSV FILE
FILENAME = "SingleVoltageData.csv"
NEWLINE = "\n"


# Change COM PORT as needed, used by MySerialPort.open_port() function.
# String variable with word COM in caplocks in front is a must!
# example: "COM4", "COM2", "COM1", etc...
# Defaulted to COM4 here
defaultCOM = "COM4"


class MySerialPort(object):
    """Potentiostat class that reads the command file, and runs the command
    file from a serial port.
    """
    # Passing in the egain, igain and bias settings in "real time" to the
    # class directly for easier access
    def __init__(self, egain, igain, bias):
        '''Initializing the variables so all functions can access the
        self.s port and remain open.
        '''
        self.s = None

        # these settings are needed to initalize the class so I can work with
        # the class in the gui no choice must be here
        self.egain_val = egain
        self.igain_val = igain
        self.bias_val = bias

    def open_port(self, port=defaultCOM, baudrate=19200, bytesize=8,
                  parity='N', stopbits=1, timeout=1,
                  xonxoff=False, rtscts=False, writeTimeout=3, dsrdtr=False,
                  interCharTimeout=None):
        '''Open a self.s port, explicitly define all values to be sure
        they are set. Notes: I set a default read and write timeout of
        3 seconds to get it to respond quickly.
        '''
        self.s = Serial(port, baudrate, bytesize, parity, stopbits, timeout,
                        xonxoff, rtscts, writeTimeout, dsrdtr,
                        interCharTimeout)
        print('A serial port has been opened using ' + port + '.\n')

    def send(self, str_to_send):
        """sending commands to the serial port """
        chars_sent = self.s.write(str_to_send)
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
                    break
                elif new_char == "\r" or new_char == "\n":
                    # Watch for other special characters like "\r \f".
                    pass
                elif new_char == "?":
                    # should we break after an error?
                    break
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                print "Receive function timed out."
                break
        time.sleep(0.01)

        return data_string

    def close_port(self):
        '''closes the self.s port'''
        self.s.close()

    def bias(self):
        '''Setting the bias potential as soon as the cell is on.
        Reference: PAGE 15  BIAS[]
        '''
        try:
            # enter bias
            x = input('Enter the Potential Bias to apply (mV) between -8000 mV\
and +8000 mV: ')
            if x <= 8000 and x >= -8000:
                self.send('SETE %s \n' % x)
                self.sete_Val = x
                print ""
            else:
                print "Please enter a value in the proper range."
                self.bias()
        except:
            print 'Enter value again.'
            self.bias()

    def measure_values(self):
        '''Running the potentiostat to apply potential and measure the current,
        and then return the value directly to the computer. Note that each
        command is ran in single order due to ease and safety of command
        processing. The data is then saved into a dictionary directly, no
        if loop is required to check for error. However, note that two errors
        do exist. Also, note that all these commands are READ commands only; no
        writing is done in this function.
        '''

        self.send('READE \n')
        v = self.receive(25)
        self.measuredBIAS = v.strip()

        self.send('READI \n')
        i = self.receive(25)
        self.reply_current = i.strip()

        self.send('Q \n')
        q = self.receive(17)
        self.qval = q.strip()

    def record_data(self):
        '''Records the data output into a csv file with the timestamp'''
        myfile = open(FILENAME, 'a')
        newrow = time.strftime('%H:%M:%S,')
        newrow += str(self.sete_Val) + ","  # applied potential
        newrow += str(self.measuredBIAS) + ","  # measured potential
        newrow += str(self.reply_current) + ","  # CURRENT
        newrow += str(self.qval)  # CHARGE
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()

    def exp_setup(self):
        self.measure_values()
        self.record_data()
        time.sleep(TIMEDELAY)

    def run(self):
        '''main while loop that controls, runs and executes all other commands
        running everything in this main excution function.
        '''

        cycles = 1

        self.bias()

        # change from 'a' to 'w' to overwrite file if desired
        myfile = open(FILENAME, "a")
        myfile.write("new data," + time.strftime("%d/%m/%Y") + NEWLINE)
        myfile.write("Time,BIAS,Measured Voltage,Current,CurrentExp,CHARGE(Q),\
Qexp" + NEWLINE)
        myfile.close()

        while True:
            # using a loop with a try and except to cancel and exit
            # exit is only done via a ctrl-c loop
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
        # opening the MySerialPort class with built in parameters
        self.myfile = MySerialPort(egain=1, igain=1, bias=1)

    def fake_serial(self):
        """Runs the Fake_Serial() Class if the simulator parameter is True."""
        setattr(module, "Serial",  fake_serial)
        # setting com parameter with open_port() function
        self.myfile.open_port(self.com)
        self.myfile.run()
        # Closing serial port after run
        self.myfile.close_port()

    def run(self):
        print 'Note: To Close program press "Ctrl-C"'
        if self.sim is True:
            # Running fake serial port
            print 'Running simulator Mode: ', self.sim
            self.fake_serial()  # opening serial port in simulator class only
        else:
            # run real serial port:
            print 'Running Real Serial: ', self.sim
            # Import real serial class
            from serial import Serial
            setattr(module, "Serial", Serial)
            # open serial port, specifying comport choice
            self.myfile.open_port(self.com)
            self.myfile.run()
            self.myfile.close_port()
        print 'Closing Program'
        print 'Thank you and Have a Good Day'


###############################################################################
if __name__ == '__main__':
    parser = sp()
    b = Main(parser)
    b.run()
