#!/usr/bin/python
# encoding: utf-8
#graphclass.py
'''
Created by Amit Sandhel on 2013-05-27.
This script is designed to display the graph in real time
'''

"""
Note: this program requires:
        1) Python 2.7
        2) Matplotlib
        3) NumPy
        4) SciPy
        4) math-built in to Pyton
        5) logging-built in to Python
"""


'''Testing to ensure all libraries exist on computer'''

#Does matplotlib exist on library 
GRAPH = True
try:
    import matplotlib.pyplot as plt
    
except:
    GRAPH = False
    logger.debug('Error: Please install Matplotlib and Numpy')

#Does numpy library exist
NUMPY = True
try:
    #importing numpy library
    from numpy import * 
except:
    NUMPY = False
    #print statement to let user know to install properly libraries
    logger.debug('Error: Please install Numpy and SciPy')
    sys.exit(0)

from datetime import datetime




class GraphClass():
    '''takes the data and displayst the data in real time
    '''
    def __init__(self, data = None, data2 = None, data3 = None):
        #various arg pass in arguments
        self.data = data
        self.data2 = data2
        self.data3= data3
        
        #setting up figure variables
        self.fig = plt.figure(1)
        self.ax1 = plt.subplot(2,1,1)
        self.ax2 = plt.subplot(2,1,2)
        
        #lists to access data 
        self.time_list1=[]
        self.bias_list2=[]
        self.current_list3=[]
    
    def analysis(self, data, data2, data3):
        '''appends the data obtained from beastie into individual lists and then graphs the last 5 elements of each list'''
        self.time_list1.append( data )
        self.bias_list2.append( data2 )
        self.current_list3.append( data3)
        
        #call graph function and graphs last 5 elements of each list
        self.graph(self.time_list1[-5:], self.bias_list2[-5:], self.current_list3[-5:])
            
    def graph(self, n_d_time, n_d1_bias, n_d2_current): 
        '''graph function takes parameters for graphing'''
        #n_d = time
        #n_d1 = bias
        #n_d2 = current
        #clear the axis each iteration
        self.ax1.cla()
        
        #autoscale the graph
        plt.autoscale(enable = True, axis = 'both', tight = True)
        
        #plotting the graph with color
        self.ax1.plot(n_d_time, n_d1_bias, "-m")
        
        #clear the axis each iteration
        self.ax2.cla()
        
        #autoscale the axis
        plt.autoscale(enable = True, axis = 'both', tight = True)
        
        #plotting the graph with color
        self.ax2.plot( n_d_time, n_d2_current, "-r")
        
        #allows us to  graph in "real time" every iteration new plot is displayed
        plt.show(block = False)
        plt.draw()
    
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Graphclass Graphing Environment!\n')
    GraphClass()
  
