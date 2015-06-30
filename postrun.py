import logging

# !/usr/bin/python
# encoding: utf-8
# postrun,py

'''Created by Amit Sandhel.
This script is designed to take the saved raw data from "BOOK2.csv" and
automatically output the data into graphs for graphing and plotting purposes.
The data is saved as images for the user's behalf. Note that the filename
BOOK2.csv MUST be left as is and not be renamed.
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

# setting up the matplot figures and their geometrical sizes
fig = plt.figure(1)
ax1 = plt.subplot(2, 1, 1)
ax2 = plt.subplot(2, 1, 2)

# opening the csv file as a readline
# and reading the csv file line by line using readline
foo = open("BOOK2.csv", "r")

# removing the header of the csv file so it won't be parsed
z = foo.readline()

# parsing the lines into various temporary variables into various lists
# time, bias and current from lines 23-25
for line in foo:
    b = line.strip().split(',')
    time.append(float(b[0]))
    bias.append(float(b[2]))
    current.append(float(b[3]))

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
    # graph each section independently
    ax1.plot(n_d_time, n_d1_bias, "-m")
    ax2.plot(n_d_time, n_d2_current, "-r")

    # autoscale the axis
    plt.autoscale(enable=True, axis='both', tight=True)
    plt.savefig('figure1.png')
    plt.show()

###############################################################################
if __name__ == '__main__':
    print('Welcome to the POST RUN Testing Analysis Environment!\n')
    # outputting the graph function
    graph(time, bias, current)
