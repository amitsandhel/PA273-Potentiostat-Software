import logging
from pa273_v2 import MySerialPort

# !/usr/bin/python
# encoding: utf-8
# postrun,py

'''Created by Amit Sandhel with contributions by Fredrick Leber.
This script is designed to take the saved raw data from the filename specified
in v2 script and automatically graph the data. The graphs are saved as images
for the user's behalf. The filename is currently "BOOK2.csv" but in a later
version will be auto-named according to the current date and time.
'''

logging.basicConfig(filename='postrun.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root (%s) \
             --------------------------------" % __file__)

# name for the log file
logging = logging.getLogger('postrun.log')

# Check if matplotlib exist on library
GRAPH = True
try:
    import matplotlib.pyplot as plt

except:
    GRAPH = False
    logging.debug('Error: Please install Matplotlib')


# various lists we need to graph the data
bias = []
time = []
current = []

# default scale is the smallest (100nA or 10^-7A)
currentScale = int(-7)

# setting up the matplot figures and their geometrical sizes
fig = plt.figure(1)
ax1 = plt.subplot(2, 1, 1)
ax2 = plt.subplot(2, 1, 2)

# taking the filename saved by the v2 script
mygraphfile = MySerialPort()

# opening the csv file as a readline
# and reading the csv file line by line using readline
foo = open(mygraphfile.filename, "r")

# removing the header of the csv file so it won't be parsed
z = foo.readline()

# parsing the lines into various temporary variables into various lists
# time, bias and current from lines 32-35
for line in foo:
    b = line.strip().split(',')
    time.append(float(b[0]))
    bias.append(float(b[2]))
    current.append(float(b[3])*10**int(b[1]))

    # set the scale to accomodate the largest current value
    if int(b[1]) > int(currentScale):
        currentScale = int(b[1])

    logging.debug("time list values: " + repr(time))
    logging.debug("bias list values: " + repr(bias))
    logging.debug("current list values: " + repr(current))


def graph(n_d_time, n_d1_bias, n_d2_current):
    """Graphs the output from the csv file.
    Accepts the lists as arg arguments.
    """
    logging.debug("n_d_time arg values: " + repr(n_d_time))
    logging.debug("n_d1_bias arg values: " + repr(n_d1_bias))
    logging.debug("n_d2_current arg values: " + repr(n_d2_current))

    # labeling the time axis and the voltage bias axis
    ax1.set_ylabel('Voltage Bias (mV)')
    ax2.set_xlabel('Time (seconds)')

    adjustedCurrent = []

    # labeling the current axis
    if currentScale == 0 or currentScale <= -7:
        ax2.set_ylabel('Current (A)')
        for values in n_d2_current:
            adjustedCurrent.append(values)
    elif currentScale >= -3:
        ax2.set_ylabel('Current (mA)')
        for values in n_d2_current:
            adjustedCurrent.append(values * 10**3)
    elif currentScale >= -6:
        ax2.set_ylabel('Current (microamps)')
        for values in n_d2_current:
            adjustedCurrent.append(values * 10**6)

    # graph each section independently
    ax1.plot(n_d_time, n_d1_bias, "-m")
    ax2.plot(n_d_time, adjustedCurrent, "-r")

    # autoscale the axis
    plt.autoscale(enable=True, axis='both', tight=True)
    plt.savefig('figure1.png')
    plt.show()

###############################################################################
if __name__ == '__main__':
    print('Welcome to the POST RUN Testing Analysis Environment!\n')
    # outputting the graph function
    graph(time, bias, current)
