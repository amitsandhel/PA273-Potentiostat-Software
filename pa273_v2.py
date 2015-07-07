import sys
import time
import logging
from postrun import PostRun
from main import setup_parser as sp
from Fake_Serial import Fake_Serial as fake_serial
# import graphclass script for real-time graphing
from graphclass import GraphClass

# !/usr/bin/python
# encoding: utf-8
# pa273_v2.py

"""Created by Amit Sandhel with contributions by Fredrick Leber.

This script runs the potentiostat using a custom command language. This script
comes with a built in simulator which simulates the serial port if one
is not present. Designed for testing and software development purposes.
There are two serial classes: Fake_Serial() class is a class that connects
to a virtual/fake serial port. This class also is the simulator which simulates
the potentiostat commands.

References/Sources of information used:
#http://stackoverflow.com/questions/423379/using-global-variables-in-a-function
-other-than-the-one-that-created-them
#http://stackoverflow.com/questions/1429814/how-to-programmatically-set-a-globa
l-module-variable  http://www.sitepoint.com/forums/showthread.php?1175398-Pytho
n-Django-Can-t-use-quot-setattr-quot-with-FileField
#http://stackoverflow.com/questions/1419470/python-init-setattr-on-arguments/14
19950#1419950
#http://stackoverflow.com/questions/2933470/how-do-i-call-setattr-on-the-curren
t-module
#https://www.inkling.com/read/learning-python-mark-lutz-4th/chapter-37/--getatt
r---and---getattribute--

Note: this program requires
        1) Python 2.7
        2) matplotlib
        3) logging-built in to Python
        4) Pyserial
"""

# setting up logging
logging.basicConfig(filename='pa273v2.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root (%s)\
 --------------------------------" % __file__)

# name for log file
logger2 = logging.getLogger('pa273v2.log')

# SETTING UP CSV FILE
b = time.strftime('%Y-%m-%d-%H-%M-%S')
FILENAME = "pa273_version_2-%s.csv" % b
NEWLINE = "\n"

# STATIC DATA - DO NOT TOUCH! BASED ON POTENTIOSTAT MANUAL
EIGHTBITS = 8
PARITY_NONE = 'N'
STOPBITS_ONE = 1

# Change COM PORT as needed, used by MySerialPort.open_port() function.
# String variable with word COM in caplocks in front is a must!
# example: "COM4", "COM2", "COM1", etc...
# Defaulted to COM4 here
defaultCOM = "COM4"

# running the Main() class to execute everything off argparse
module = sys.modules[__name__]


class MySerialPort():
    """Potentiostat class that reads the command file, and runs the command
    file from a serial port.
    """
    def __init__(self):
        # initializing the variable so all functions can access the self.s port
        # and remain open
        self.s = None
        self.command_dict = {}
        self.cmd_output = None
        self.next_cmd = None
        self.next_cmd_list = []

        # initalizing the values for graphclass
        self.elapsed_time = None
        self.replyAS = None
        self.replyBIAS = None
        self.replyTP = None

        '''self variable that opens the pyplot graph class'''
        self.dataTIME = self.elapsed_time
        self.dataBIAS = self.replyBIAS
        self.dataTP = self.replyTP

        self.mygraph = GraphClass(self.dataTIME, self.dataBIAS, self.dataTP)

    def open_port(self, port=defaultCOM, baudrate=19200, bytesize=EIGHTBITS,
                  parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=1,
                  xonxoff=False, rtscts=False, writeTimeout=3, dsrdtr=False,
                  interCharTimeout=None):
        """Open a self.s port and explicitly define all values to be
        sure they are set.
        """
        # Note: default read and write timeout is 1 second to get it
        # to respond quickly
        self.s = Serial(port, baudrate, bytesize, parity, stopbits, timeout,
                        xonxoff, rtscts, writeTimeout, dsrdtr,
                        interCharTimeout)
        logger2.debug('Serial Port opened using ' + port)
        print('A serial port has been opened using ' + port + '.\n')

    def close_port(self):
        '''Closes the self.s port'''
        logger2.debug('Closing Serial Port')
        self.s.close()

    def send(self, str_to_send):
        """Sending commands to the serial port."""
        chars_sent = self.s.write(str_to_send)
        logger2.debug("Tx: " + repr(str_to_send) +
                      "bytes sent: %d" % chars_sent)

    def receive(self, max_chars):
        '''Receive string with timeout and wait for end-of-message character
        or error.
        '''
        data_string = ""
        start_time = time.time()
        MAXRECEIVETIMEOUT = 0.05  # time.now() is in seconds
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                if new_char == "*":
                    logger2.debug("Rx -  * received")
                    break
                elif new_char == "\r" or new_char == "\n":
                    # watch for other special characters like "\r \f" review
                    # your logs to see if anything else is embedded.
                    pass
                elif new_char == "?":
                    logger2.debug("Rx - Error receive, now what?")
                    # should we break after an error?
                    break
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                logger2.debug("Rx Receive timeout, returning what I have\
                and hoping")
                print "Receive function timed out."
                break
        # time.sleep(0.05)  # initially 0.01, was set to 0.05
        logger2.debug("Rx: " + repr(data_string) + " bytes read: %d" %
                      len(data_string))

        return data_string

    def readfiles(self):
        """Reads the command csv file called beastiecommandfile.csv"""
        file = "beastiecommand.csv"
        command_list = []
        readfile = open(file, "r")
        for line in readfile:
            command_list.append(line)
        logger2.debug("readfiles() timing response: " + repr(command_list))
        return command_list

    def parse_and_sort_commands(self, command_list):
        '''Pass in the command list and we return a command dictionary.'''
        # parsing pass in command list
        for line in command_list:
            time, command = line.strip().split(",")
            if float(time) in self.command_dict.keys():
                # Append to existing:
                # Note: .strip() removes surrounding whitespace from the string
                self.command_dict[float(time)] += (command.strip(), )
            else:
                # Create new entry:
                self.command_dict[float(time)] = (command.strip(), )

        '''For debugging purposes
        for k, v in self.command_dict.iteritems():
            print k, v
        '''
        logger2.debug("New command dict: " + repr(self.command_dict))

        # sorting the dictionary keys (command times)
        self.cmd_output = self.command_dict.keys()
        self.cmd_output.sort()

    def get_next_command(self):
        '''This function is parsing the commands from the command file
        into a tuple.
        '''
        next_time = self.cmd_output.pop(0)
        next_cmd = self.command_dict[next_time]
        reply = (next_time, next_cmd)

        logger2.debug("get_next_command() reply timing response: " +
                      repr(reply))
        return reply

    def command_execute(self, reply):
        '''Calling the reply from the function above get_next_command()'''
        self.send(reply[1])  # I don't think this newline is needed (+ " \n")
        # The '20' below represents an arbitrarily high number of characters
        # Note: in the future if different/more commands other than BIAS are
        # going to be input, you need an if statement here to determine which
        # self.replyXXX variable to write to
        self.replyBIAS = self.receive(20)
        logger2.debug("command execute()reply timing response: " +
                      repr(reply[1]))

    def always_read_commands(self):
        '''Commands that are always read all the time.
        All these commands are read commands only.
        '''
        self.send("NC \n")
        self.reply1 = self.receive(4)
        logger2.debug("NC TIMER RESPONSE: " + repr(self.reply1))

        self.send("AS \n")
        self.replyAS = self.receive(4)
        logger2.debug("AS TIMER RESPONSE: " + repr(self.replyAS))

        '''The BIAS is actually obtained from the 'command_execute' function
        self.send("BIAS \n")
        self.replyBIAS = self.receive(7)
        logger2.debug("BIAS TIMER RESPONSE: " + repr(self.replyBIAS))
        '''

        self.send("TP \n")
        self.replyTP = self.receive(4)
        logger2.debug("TP TIMER RESPONSE: " + repr(self.replyTP))

    def record_data(self):
        '''Recording the results into a csv file using local variables
        to increase process speed.
        '''
        myfile = open(FILENAME, 'a')
        newrow = str(self.elapsed_time) + ","
        newrow += str(self.replyAS) + ","
        newrow += str(self.replyBIAS) + ","
        newrow += str(self.replyTP) + ","
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()

    def run(self):
        start_time = time.time()
        new_time = 0.0  # initalization value
        self.replyBIAS = 0  # initialize value to zero
        # opening excel file in write only mode
        # will rewrite on top of data in existing file. change to "a" to
        # instead append the data
        myfile = open(FILENAME, "w")
        myfile.write("Time, AS, BIAS, TP-point#, TP-current, TP-bias, " +
                     NEWLINE)
        myfile.close()

        logger2.debug('time_meter_command() myfile timing VALUE: ' +
                      repr(myfile))

        # get the command list from beastiecommand.csv and make the commands
        # into a dictionary. Sort them based on time.
        command_list = self.readfiles()
        self.parse_and_sort_commands(command_list)
        totalCommands = len(self.cmd_output)
        totalTime = self.cmd_output[-1]

        while True:
            # while loop that measures the elapsed time
            self.elapsed_time = time.time() - start_time
            self.always_read_commands()
            self.record_data()
            time.sleep(0.05)
            if time.time() - start_time >= new_time:
                if len(self.cmd_output) == 0:
                    print("")  # just a blank line
                    break
                new_time, newcmd = self.get_next_command()
                print "Now running cycle " + \
                      str(totalCommands - len(self.cmd_output)) + " of " + \
                      str(totalCommands),
                print "   ETA: " + \
                      str(round((totalTime - time.time() + start_time), 1)) + \
                      " seconds."
                self.elapsed_time = time.time() - start_time
                for item in newcmd:
                    reply = (new_time, item)
                    self.command_execute(reply)
                    self.always_read_commands()
                    self.record_data()

                # running the graphclass script to draw the graph in real time
                # self.mygraph.analysis(self.elapsed_time, self.replyBIAS,
                #                      self.replyTP)

                logger2.debug('mygraph elapsed_time data: ' +
                              repr(self.elapsed_time))
                logger2.debug('mygraph self.replyBIAS data: ' +
                              repr(self.replyBIAS))
                logger2.debug('mygraph self.replyTP data: ' +
                              repr(self.replyTP))


class Main():
    """Main class which executes the entire pa273_v2 script."""
    def __init__(self, parser):
        args = parser.parse_args()
        self.sim = args.sim  # sim parameter
        self.com = 'COM' + str(args.com)
        self.myfile = MySerialPort()

    def fake_serial(self):
        """Runs the Fake_Serial() Class if the simulator parameter is True."""
        setattr(module, "Serial", fake_serial)  # Fake_Serial
        self.myfile.open_port(self.com)
        self.myfile.run()
        # Closing serial port after run
        self.myfile.close_port()

    def run(self):
        # print 'The COM PORT is ' + self.com  # not needed for now
        if self.sim is True:
            logging.debug("FAKE/VIRTUAL SIM VALUE: " + repr(self.sim))
            print 'running sim: ', self.sim
            self.fake_serial()  # opening serial port in simulator class only

            self.postrun = PostRun(FILENAME)
            self.postrun.graph()
        else:  # run real serial port:
            logging.debug("REAL SIM VALUE: " + repr(self.sim))
            print 'running real simulator: ', self.sim
            # Import real serial class
            from serial import Serial

            setattr(module, "Serial", Serial)
            self.myfile.open_port(self.com)
            self.myfile.run()
            self.myfile.close_port()

            self.postrun = PostRun(FILENAME)
            self.postrun.graph()


###############################################################################

if __name__ == '__main__':
    parser = sp()
    b = Main(parser)
    b.run()
