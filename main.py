import sys
import argparse
import subprocess

'''main.py
Created by Amit Sandhel on 2013-05-27. With contributions by Fredrick Leber.

This script is the master file that controls all the other scripts. It also
contains the argparse command control, here the user can add his own argparse
commands as they need.

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
    parser.add_argument('-com', '-c',  help="Change COM PORT Settings",
                        type=int, default=5)  # default comport setting

    '''parser commands to possibly (but unlikely) be added in later:
    parser.add_argument('-debug', '-d', help='enhance log file output',
                        action = "store_true")
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
        """Initialize argparse command settings."""
        args = parser.parse_args()
        self.sim = args.sim
        self.version = args.version
        self.test = args.test
        self.com = args.com

    def run(self):
        # if the user has input the 'test' argument
        if self.test:
            '''If the test parameter is TRUE, then inform user to run the test
            script directly and RUN all TESTS DIRECTLY
            '''
            print "I'm sorry, run all tests DIRECTLY"

        else:
            '''all these settings can be changed together'''
            print "Testing skipped"

            if self.sim:
                # add a -s string character
                self.string_sim = " -s"
            else:
                # necessary to have, otherwise the real serial port will not
                # work at all because the sim parameter default value is
                # not given
                self.string_sim = ""

            if self.com:
                # add the COM PORT as a string character
                self.string_com = ' -c' + str(self.com)

            # Naming a string variable called COMMAND that combines all the
            # strings together. Each "potentiostat version script" can be
            # run with or without the '-s'.

            '''Note: If you don't add the 'python' command before the file then
            it won't work on some computers (possibly Windows 8/UNIX due to
            argparse not registering correctly.
            '''
            # potentiostat version1
            COMMAND = "python pa273_v1.py" + self.string_sim + self.string_com
            # potentiostat version2
            COMMAND2 = "python pa273_v2.py" + self.string_sim + self.string_com

            # run version 1 subcommands
            if self.version == 1:
                try:
                    subprocess.call(COMMAND, shell=True)
                except (KeyboardInterrupt, SystemExit):
                    print 'Thank you for using the v1 script. Goodbye.'
                    sys.exit()

            # run version 2 subcommands
            elif self.version == 2:
                try:
                    subprocess.call(COMMAND2, shell=True)
                except (KeyboardInterrupt, SystemExit):
                    print 'Thank you for using the v2 script. Goodbye.'
                    sys.exit()

            else:
                print 'Software is closing Thank You'


#######################################################################
if __name__ == '__main__':
    print "Welcome to Potentiostat P273A Software"
    parser = setup_parser()
    b = Main(parser)
    b.run()
