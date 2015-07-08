import logging

# !/usr/bin/python
# encoding: utf-8
# postrun.py

'''Created by Amit Sandhel with contributions by Fredrick Leber.
This script is designed to take the saved raw data from the filename specified
in v2 script and automatically graph the data. The graphs are saved as images
for the user's behalf. The filename is auto-named according to the current
date and time.
'''

logging.basicConfig(filename='postrun.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root (%s)\
             --------------------------------" % __file__)
# name for the log file
logging = logging.getLogger('postrun.log')

# Check if matplotlib exist on library
try:
    import matplotlib.pyplot as plt

except:
    logging.debug('Error: please install matplotlib.')


class PostRun():
    def __init__(self, filename):
        # various lists we need to graph the data
        self.bias = []
        self.time = []
        self.current = []
        self.adjustedCurrent = []
        # default scale is the smallest (100nA or 10^-7A)
        self.currentScale = int(-7)
        self.minBIAS = 0
        self.maxBIAS = 0
        # opening the csv file as a readline
        # and reading the csv file line by line using readline
        foo = open(filename, "r")

        # removing the header of the csv file so it won't be parsed
        foo.readline()

        # parsing the lines into various temporary variables into various lists
        # time, bias and current from lines 35-37
        for line in foo:
            b = line.strip().split(',')
            self.time.append(float(b[0]))
            self.bias.append(float(b[2]))
            self.current.append(float(b[3])*10**int(b[1]))
            if float(b[2]) > self.maxBIAS:
                self.maxBIAS = float(b[2])
            elif float(b[2]) < self.minBIAS:
                self.minBIAS = float(b[2])

        # set the scale to accomodate the largest current value
        if int(b[1]) > int(self.currentScale):
            self.currentScale = int(b[1])

        logging.debug("time list values: " + repr(self.time))
        logging.debug("bias list values: " + repr(self.bias))
        logging.debug("current list values: " + repr(self.current))

    def graph(self):
        """Graphs the output from the csv file."""
        print('Welcome to the POST RUN Testing Analysis Environment!\n')
        logging.debug("n_d_time arg values: " + repr(self.time))
        logging.debug("n_d1_bias arg values: " + repr(self.bias))
        logging.debug("n_d2_current arg values: " + repr(self.current))

        # setting up the matplot figures and their geometrical sizes
        # fig = plt.figure(1) # this line is probably not needed
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2)

        # clear the plots that were left over from graphclass
        ax1.cla()
        ax2.cla()

        # labeling the time axis and the voltage bias axis
        ax1.set_ylabel('Voltage Bias (mV)')
        ax2.set_xlabel('Time (seconds)')

        # labeling the current axis
        if self.currentScale == 0 or self.currentScale <= -7:
            ax2.set_ylabel('Current (A)')
            for values in self.current:
                self.adjustedCurrent.append(values)
        elif self.currentScale >= -3:
            ax2.set_ylabel('Current (mA)')
            for values in self.current:
                self.adjustedCurrent.append(values * 10**3)
        elif self.currentScale >= -6:
            ax2.set_ylabel('Current (microamps)')
            for values in self.current:
                self.adjustedCurrent.append(values * 10**6)

        # graph each section independently
        ax1.plot(self.time, self.bias, "-m")
        ax2.plot(self.time, self.adjustedCurrent, "-r")

        # autoscale the axis
        plt.autoscale(enable=True, axis='both', tight=False)
        # but manually scale the BIAS
        ax1.set_ylim([self.minBIAS - 150, self.maxBIAS + 150])
        plt.savefig('figure1.png')
        plt.show()
