import sys
import time
# from postrun import PostRun
from main import setup_parser as sp
from Fake_Serial import Fake_Serial as fake_serial
# import graphclass script for real-time graphing (not currently being used)
# from graphclass import GraphClass

"""pa273_v2.py
Created by Amit Sandhel with contributions by Fredrick Leber.

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

Note: this script requires
        1) Python 2.7
        2) matplotlib
        3) Pyserial
"""

# SETTING UP CSV FILE (uncomment the next two lines and delete the book2 line
# to restore autonaming based on date)
# b = time.strftime('%Y-%m-%d-%H-%M-%S')
# FILENAME = "pa273_version_2-%s.csv" % b
FILENAME = "WaveformData.csv"
NEWLINE = "\n"

# Change COM PORT as needed, used by MySerialPort.open_port() function.
# String variable with word COM in caplocks in front is a must!
# example: "COM4", "COM2", "COM1", etc...
# Defaulted to COM4 here
defaultCOM = "COM4"


class MySerialPort():
    """Potentiostat class that reads the command file, and runs the command
    file from a serial port.
    """
    def __init__(self, sim=False):
        # initializing the variable so all functions can access the self.s port
        # and remain open
        self.s = None
        self.command_dict = {}
        self.cmd_output = None
        self.sim = sim

        # initalizing the values for graphclass
        self.elapsed_time = 0.0
        self.replyAS = -7
        self.replyBIAS = 0  # initialize value to zero
        self.reply_current = 0

        '''opens the pyplot graph class (not used for now)'''
        # self.mygraph = GraphClass()

    def open_port(self, port=defaultCOM, baudrate=19200, bytesize=8,
                  parity='N', stopbits=1, timeout=1,
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
        print('A serial port has been opened using ' + port + '.\n')

    def close_port(self):
        '''Closes the self.s port.'''
        self.s.close()

    def send(self, str_to_send):
        """Sending commands to the serial port."""
        self.s.write(str_to_send)

    def receive(self, max_chars):
        '''Receive string with timeout and wait for end-of-message character
        or error.
        '''
        data_string = ""
        start_time = time.time()
        MAXRECEIVETIMEOUT = 0.3
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                if new_char == "*":
                    break
                elif new_char == "\r" or new_char == "\n":
                    # watch for other special characters like "\r \f"
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

    def readfiles(self):
        """Reads the command csv file called beastiecommandfile.csv"""
        file = "beastiecommand.csv"
        command_list = []
        readfile = open(file, "r")
        for line in readfile:
            command_list.append(line)
        return command_list

    def parse_and_sort_commands(self, command_list):
        """Pass in the command list and we return a command dictionary.
        The command dictionary used the command times as keys, which
        correspond to different BIAS values in tuple form (or other commands)
        """
        # parsing command list
        for line in command_list:
            time, command = line.strip().split(",")
            # try and except clause is here to catch errors. Otherwise if a
            # user fails to write bias correctly the software will crash
            try:
                if float(time) in self.command_dict.keys():
                    # Append to existing:
                    # Note: .strip() removes surrounding whitespace
                    # from the string
                    self.command_dict[float(time)] += command.strip()
                else:
                    # Create new entry:
                    self.command_dict[float(time)] = command.strip()
            except:
                print "An error occured when importing the command excel file."

        '''For debugging purposes
        for k, v in self.command_dict.iteritems():
            print k, v
        '''
        # sorting the dictionary keys (command times)
        self.cmd_output = self.command_dict.keys()
        self.cmd_output.sort()

    def command_execute(self, inputBIAS):
        '''Execute the inputted BIAS'''
        self.send(inputBIAS + " \n")
        # The '15' below represents an arbitrarily high number of characters
        # Note: in the future if different/more commands other than BIAS are
        # going to be input, you need an if statement here to determine which
        # self.replyXXX variable to write to
        self.replyBIAS = self.receive(15)

    def read_data(self):
        """All these commands are read commands only."""
        self.send("Q \n")
        self.replyQ = self.receive(25)

        self.send('READI \n')
        self.READI = self.receive(25)

        self.send('READE \n')
        self.READE = self.receive(25)

        if self.sim is False:
            self.send("BIAS \n")
            self.replyBIAS = self.receive(25)

    def record_data(self):
        '''Recording the results into a csv file using local variables
        to increase process speed.
        '''
        myfile = open(FILENAME, 'a')

        newrow = str(self.elapsed_time) + ","
        newrow += str(self.replyBIAS) + ","
        newrow += str(self.READE) + ","
        newrow += str(self.READI) + ","
        newrow += str(self.replyQ) + ","
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()

    def run(self):
        # opening excel file in write only mode. will rewrite on top of data
        # in existing file. change to "a" to instead append the data
        myfile = open(FILENAME, "a")
        myfile.write("new data," + time.strftime("%d/%m/%Y") + NEWLINE)
        myfile.write("Time,BIAS,Measured Voltage,Current,CurrentExp,CHARGE(Q),\
Qexp" + NEWLINE)
        myfile.close()

        start_time = time.time()

        # get the command list from beastiecommand.csv and make the commands
        # into a dictionary. Sort them based on time.
        self.parse_and_sort_commands(self.readfiles())
        totalCommands = len(self.cmd_output)
        counts = totalCommands
        totalTime = self.cmd_output[-1]

        for times in self.cmd_output[:]:
            counts -= 1
            while (time.time() - start_time) < times:
                self.elapsed_time = time.time() - start_time
                self.read_data()
                self.record_data()
            print "Now running cycle " + \
                  str(totalCommands - counts) + \
                  " of " + str(totalCommands),
            print "   ETA: " + str(round((totalTime - time.time() +
                                          start_time), 1)) + " seconds."
            if self.command_dict[times] == "END":
                    print("")
                    break
            self.elapsed_time = time.time() - start_time
            self.command_execute(self.command_dict[times])
            self.read_data()
            self.record_data()

# AMIT: leave this module here as it truly belongs to the stuff at the bottom
# running the Main() class to execute everything off argparse
module = sys.modules[__name__]


class Main():
    """Main class which executes the entire pa273_v2 script."""
    def __init__(self, parser):
        args = parser.parse_args()
        self.sim = args.sim  # sim parameter
        self.com = 'COM' + str(args.com)
        self.myfile = MySerialPort(sim=self.sim)

    def fake_serial(self):
        """Runs the Fake_Serial() Class if the simulator parameter is True."""
        setattr(module, "Serial", fake_serial)
        self.myfile.open_port(self.com)
        self.myfile.run()
        # Closing serial port after run
        self.myfile.close_port()

    def run(self):
        # print 'The COM PORT is ' + self.com  # not needed for now
        if self.sim is True:
            print 'running simulator: ', self.sim
            self.fake_serial()  # opening serial port in simulator class only
        else:  # run real serial port:
            print 'Running using real serial port.'
            # Import real serial class
            from serial import Serial
            setattr(module, "Serial", Serial)
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
