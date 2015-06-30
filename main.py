import logging
import argparse
import subprocess

# !/usr/bin/python
# encoding: utf-8
# main.py

'''Created by Amit Sandhel on 2013-05-27.

This script is the master file that controls all the other scripts
It also contains the argparse command control
here the user can add his own argparse commands as they need

References/Sources of information used:
http://docs.python.org/2/howto/argparse.html#id1
'''


def setup_parser():
    '''Parser function that is designed to initalize all the argparse command
    functions. Note that some argument functions are either deprecated or still
    need to be developed. Deprecated functions are currently commented out.

    Postrun option is depreciated as potentiostat script will run the postrun
    analysis directly, not via parser.
    '''
    POTENTIOSTATVERSION = 'Determine potentiostat version to execute \
    (default: %(default)s):\n  1 - pa273_v1.py ...\n  2 - pa273_v2.py ....'

    parser = argparse.ArgumentParser(description='operating Potentiostat \
                                                 Modules.')

    parser.add_argument('-sim', '-s', help='run simulator',
                        action="store_true")
    parser.add_argument('-version', '-v', help=POTENTIOSTATVERSION,
                        type=int, default=1)
    parser.add_argument('-test', '-t',  help='Run unit tests',
                        action="store_true")

    '''parser commands to be added in later:
    parser.add_argument('-debug', '-d', help='enhance log file output',
                        action = "store_true")
    parser.add_argument('-com', '-c',  help = "Change COM PORT Settings",
                        type = str, default = 4) # default comport setting
    parser.add_argument('-filename','-f', help='change name of data saving \
                        file deprecated function', action = "store_true")
    parser.add_argument('-postrun', '-p', help='post run graph of entire \
                        display', action = "store_true")
    '''
    return parser


class Main():
    """Main class which executes the argparse and execution of the various
       script files
       """

    def __init__(self, parser):
        # argparse command settings
        args = parser.parse_args()
        self.sim = args.sim
        self.version = args.version
        self.test = args.test

        # self variables, will be set and used based on the argparse settings
        self.string_1 = ""

    def run(self):
        '''runs the class'''

        # if the user has input the 'test' argument
        if self.test:
            '''If the test parameter is TRUE, then inform user to run the test
            script directly and RUN all TESTS DIRECTLY
            '''
            print "I'm sorry, run all tests DIRECTLY"

        else:
            '''all these settings can be changed together'''
            print "Testing skipped"

            if self.sim is True:
                # adding a -s string character
                self.string_1 = " -s"

            else:
                # keep empty
                self.string_1 = ""

            # naming a string variable called COMMAND
            # combining all the strings together
            # two command strings exist for each "potentiostat version script"

            '''Note: If you don't add the 'python' command before the file then
            it won't work on some computers (possible Windows 8/UNIX due to
            argparse not registering correctly.
            '''
            # potentiostat version1
            COMMAND = "python pa273_v1.py" + self.string_1

            # potentiostat version2
            COMMAND2 = "python pa273_v2.py" + self.string_1

            # running version 1 subcommands
            if self.version == 1:
                subprocess.call(COMMAND, shell=True)

                '''Logging file Setup'''
                # opening up parser to main library separately for each
                # self.version to prevent overlapping logs
                logging.basicConfig(filename='main.log', filemode='a',
                                    level=logging.DEBUG, format='%(asctime)s, \
                                    %(levelname)s, %(message)s')
                logging.info(" ---------------------- root (%s) \
                --------------------------------" % __file__)

                # naming log file
                log1 = logging.getLogger('main.log')

                log1.debug("subprocess call: " + repr(COMMAND))

            # running version 2 subcommands
            elif self.version == 2:
                subprocess.call(COMMAND2, shell=True)

                '''Logging file Setup'''
                # opening up parser to main library separately
                logging.basicConfig(filename='main.log', filemode='a',
                                    level=logging.DEBUG, format='%(asctime)s, \
                                    %(levelname)s, %(message)s')
                logging.info(" ---------------------- root (%s) \
                --------------------------------" % __file__)

                # naming log file
                log1 = logging.getLogger('main.log')

                log1.debug("subprocess call: " + repr(COMMAND2))

            else:
                print 'Software is closing Thank You'


#######################################################################
if __name__ == '__main__':
    print "Welcome to Potentiostat P273A Software"
    parser = setup_parser()
    b = Main(parser)
    b.run()
