import logging

# !/usr/bin/python
# encoding: utf-8
# graphclass.py

""" Created by Amit Sandhel with contributions by Fredrick Leber.
This script is designed to display the graph in real time.

Note: this program requires:
        1) Python 2.7
        2) Matplotlib
        3) logging-built in to Python
"""

# Setting up logging
logging.basicConfig(filename='graphclass.log', filemode='a',
                    level=logging.DEBUG, format='%(asctime)s, \
                    %(levelname)s, %(message)s')
logging.info(" ---------------------- root (%s) \
             --------------------------------" % __file__)

# name for log file
logger = logging.getLogger('graphclass.log')

# Does matplotlib exist on library
GRAPH = True
try:
    import matplotlib.pyplot as plt
except:
    GRAPH = False
    logger.debug('Error: Please install matplotlib.')


class GraphClass():
    """Takes the data and displays it in real time."""
    def __init__(self):
        # setting up figure variables
        # self.fig = plt.figure(1)  # this line is not necessary
        self.ax1 = plt.subplot(2, 1, 1)
        self.ax2 = plt.subplot(2, 1, 2)

        # lists to access data
        self.time_list = []
        self.bias_list = []
        self.current_list = []

    def analysis(self, timeData, BIASData, TPData):
        """appends the data obtained from beastie into individual lists and
        then graphs the elements of each list. (Used to be last 5 elements)
        """
        self.time_list.append(timeData)
        self.bias_list.append(BIASData)
        self.current_list.append(TPData)

        # call graph function and graphs last 5 elements of each list
        self.graph()

    def graph(self):
        '''graph function, takes parameters for graphing'''

        # clear the axis each iteration
        self.ax1.cla()
        self.ax2.cla()

        # labeling the time axis and the voltage bias axis
        self.ax1.set_ylabel('Voltage Bias (mV)')
        self.ax2.set_xlabel('Time (seconds)')

        # autoscale the graph
        plt.autoscale(enable=True, axis='both', tight=False)

        # plotting the graph with color
        self.ax1.plot(self.time_list, self.bias_list, "-m")

        # autoscale the axis
        plt.autoscale(enable=True, axis='both', tight=False)

        # plotting the graph with color
        self.ax2.plot(self.time_list, self.current_list, "-r")

        # Allows graphing in "real time". Every iteration new plot is displayed
        plt.show(block=False)
        plt.draw()

###############################################################################
if __name__ == '__main__':
    print('Welcome to my Graphclass Graphing Environment!\n')
    GraphClass()
