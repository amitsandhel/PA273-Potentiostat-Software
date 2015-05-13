#!/usr/bin/python
# encoding: utf-8
#test_graphclass.py


import sys
import os
import unittest
import time
import timeit
import logging 
import random
import matplotlib.pyplot as plt
from numpy import * 
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import graphclass



logging.basicConfig(filename='graphclass.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")


class graphtest(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        self.m = graphclass.GraphClass()
        #self.debug = False
        self.debug = True
        self.logger = logging.getLogger('graphclass')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
    def test01(self):
        '''testing the graph output by saving it to a data file by opening a csv file
        '''
        datalist = [] #empty list needed to append rows from csv file to an array 
        mydata = "BooK3.csv"
        readfile = open(mydata, "r")
        
        for line in readfile:
            datalist.append(line)
            self.m.make_graph(datalist)
            self.m.show_graph()
            
        #saving the graph to a png image and using it as a reference hence the "self" variable use name 
        self.newfile = plt.savefig('foo.png')
    
    def test02(self):
        '''test the dataarray output format via print statements only
        '''
        dataarray = array(self.data2, dtype = str)
        #print 'complete data array', dataarray
        #print 'Elapsed time',dataarray[:,6]
        #print 'Bias', dataarray[:,2]
        #print 'Current', dataarray[:,4]
    
    def test03(self):
        '''testing the creation of a one row array'''
        ans = array([ -4.00000000e+00, 5.00000000e+02,   1.00000000e+00, 1.45500000e+03,   0.00000000e+00,   1.14219999e+01])
        self.assertEqual(len(ans), len(self.data6))
        
        # trying to test the ability of validating both arrays are the same so far not working
        #ALTERNATIVELY CONVERT LIST TO ARRAY
        
        my_array = array( self.data3 )
        print 'RESPONSE', repr(my_array)
        print "TYPE", type(my_array)
        print "LENGTH", len(my_array)
        
        # array sections needed for graphing
        new2 = my_array[1]
        new4 = my_array[3]
        new6 = my_array[5]
        print "X", new6
        print "XX", new2
        print "XXX", new4
        
        #plt.plot(my_array[5], my_array[1], 'bo')
        #plt.axis( [0, 15, 0, 600] )
        #plt.plot(my_array[1], my_array[3], 'ro')
        #plt.axis( [0, 600, 0, 2000]) #readjusted the axis to see just one point
        #plt.show()
    
    def test04(self):
        '''testing a STATIC four point array system plot '''
        #print repr(self.data4)
        #verifying the correct columns have been taken
        sex = self.data4[ : ,1]
        sexy = self.data4[ : ,3]
        sexx = self.data4[ : ,5]
       
        #plt.plot(self.data4[ :,1], self.data4[: ,3], 'bo')
        #plt.axis( [400, 800, 1400, 2000])
        #plt.show()
        
    def test05(self):
        '''testing the development of a "living" array'''
        import random
        mylist = []
        self.data4 = array( [ [-4, 500, 1,  1500,  0, 9.4219999313],
                                    [-4, 600, 1,  1600,  0, 10.4219999313],
                                    [-4, 700, 1,  1700,  0, 11.4219999313],
                                    [-4, 800, 1,  1800,  0, 12.4219999313] ], dtype = float64 )
        
        #creating a random list
        a =empty

        for x in range(5):
            #mylist.append( [random.randrange(0,10), random.randrange(10,20), random.randrange(20,30) ] )
            myarray = array( [random.randrange(0,10), random.randrange(10,20), random.randrange(20,30) ] )
            #print repr(myarray)
            #print myarray[0]
            #ans = array( append(my_array) )
            #print ans
      
            a = append(a, [myarray[0]] )
        print repr(a)
        #bar = vstack(myarray)m

    def test06(self):
        '''making a sin wave plot using numpy ndarray using linspace'''
        start = time.time()
        x = linspace( 0, 5*pi, 100000)
        f = sin(x)
        print repr(f)
        plt.plot(f)
        #plt.show()
        plt.draw()
        self.end = time.time() - start
        print "TOTAL :", self.end
        
    def test07(self):
        ''' trying to recreate sine wave via a list but no change to array 
        Do note that this will not output the graph until the list is invincibilty 
        converted to numpy array'''
        import math
        #t = arange(0, 2*pi, 1)
        #s = sin(t)
        my = []
        t = range(-1000, 1000)
        for item in t:
            b = math.sin(item)
            my.append(b)
        #print my
        #plt.plot(my)
        #plt.show()
    
    def test08(self):
        '''trying to recreate sine wave bu changing to np.array internally
        Note: this test proves that if manually converted to array then the output is done immediately'''
        import math
        my = []
        t = range(-1000, 1000)
        for item in t:
            b = math.sin(item)
            my.append(b)
        mylist = array(my)
        #print repr(mylist)
        #print len(mylist)
        #plt.plot(mylist)
        #plt.show()
    
    def test09(self):
        '''test07 recreated using a generator function inspired off stackoverflow
        http://stackoverflow.com/questions/477486/python-decimal-range-step-value
        '''
        import math
        start = time.time()
        s=[]
        def drange(start, stop, step):
            r =start
            while r < stop:
                yield r
                r += step
        t = drange(0.0, 2.0, 0.01)
        #print ["%g" %x for x in t]
        for item in t:
            s.append(sin(2*pi*item))
        #print repr(s)
        #plt.plot(s)
        #plt.show()
        #plt.draw()
        self.end2 = time.time() - start
        #print "TOTAL: ", self.end2
    
    def test10(self):
        '''rebuilt version of test08 using the range and manually converting to an array'''
        import math
        start = time.time()
        s=[]
        def drange(start, stop, step):
            r =start
            while r < stop:
                yield r
                r += step
        t = drange(0.0, 2.0, 0.01)
        #print ["%g" %x for x in t]
        for item in t:
            s.append(sin(2*pi*item))
            np = array(s)
        #    plt.plot(np)
        #    plt.draw()
        self.end3 = time.time() - start
        #print "TOTAL :", self.end3
    '''
    def test11(self):
        #appending the row into a  single array then converting to big list using range function, bad ideA 
        import math
        start = time.time()
        array_list = []
        new_list = []
        
        def drange(start, stop, step):
            r =start
            while r < stop:
                yield r
                r += step
        t = drange(0.0, 2.0, 0.01)
        #print ["%g" %x for x in t]
        
        #fig = plt.figure(1)
        
        for item in t:
            s = array(sin(2*pi*item))
            array_list.append(s)
            np = array(array_list)
            new_list.append(np[100: ])
            line = plt.plot(np, 'ro')
            plt.draw()
            #fig.canvas.draw()
        self.end3 = time.time() - start
        print "TOTAL :", self.end3
    '''
    '''
    def test12(self):
        #''real time animated graph. this does an artistic animation NOT real time graphing ''
        x = arange(0,2*pi,0.01)            # x-array
        line, = plt.plot(x,sin(x))
        for i in arange(1,20):            #changed from 200 to 10,000
            line.set_ydata(sin(x+i/10.0))  # update the data
            plt.draw()                         # redraw the canvas
            
    def test13(self):
        #a sine graph in realt time off the website for 
        inspiration this does does an artistic animation NOT real time graphing
        x = arange(0,2*pi,0.01)         # we'll create an x-axis from 0 to 2 pi
        line, = plt.plot(x,x)               # this is our initial plot, and does nothing
        line.axes.set_ylim(-3,3)        # set the range for our plot
 
        starttime = time.time()         # this is our start time
        t = 0                           # this is our relative start time
 
        while(t < 5.0):                 # we'll limit ourselves to 5 seconds.
                                # set this to while(True) if you want to loop forever
            t = time.time() - starttime # find out how long the script has been running
            #y = -2*sin(x)*sin(t)        # just a function for a standing wave
            y = sin(x-t)                    # replace this with any function you want to animate
                                # for instance, y = sin(x-t)
 
            line.set_ydata(y)           # update the plot data
            plt.draw()                      # redraw the canvas
     '''       
    def test14(self):
        '''appending the row into a  single array then converting to big list
        creating an random point plot
        '''
        import random
        c = []
        b = array( arange(0,3))
        for item in range(100):
            x1 = random.randrange(9)
            x2 = random.randrange(9)
            x3 = random.randrange(9)
            c = array( [x1,x2,x3])
            b = vstack( [b,c] )
            plt.plot(b[-5:,1], b[-5:,2], 'ro')
            plt.draw()
            print repr(b[-5:,1])
        
    def test15(self):
        '''making a straight line in real time a much simplier idea over a sine graph but not very useful in detecting errrors
        '''
        x = 0 
        hot = []
        c = []
        d = [] 
        fig = plt.figure(1)
        for x in range(30):
            x+=1
            #y+=2
            hot.append([x,1,1])
            c.append([x,3,2])
            d.append([x,1,4])
            hotty = vstack( [hot, c, d] )
            plt.cla()
            #plt.clf()
            line, = plt.plot(hotty[:,0], hotty[:,1], 'r-')
            #a = plt.gca()
            #a.set_xlim( [0,20] )
            z = plt.axis()
            #a = plt.get_plot_commands() #IMPORTANT LINE DO NOT DELETE THIS HAS IMP INFO
            self.logger.debug("ANSWER TO PLT>.AXIS: " + repr(z) )
            #line, = plt.plot(hotty[-10:,1], hotty[-10:,2], 'ro')
            #plt.draw()
            fig.canvas.draw()
            #print repr(hotty[-10:,1])
            
    def test16(self):
        '''test that makes a real time graph resembling a sine graph 
        '''
        # note that by using list comprehension the first 20 points are auto plotted 
        fig = plt.figure(1)
        import math
        my = []
        t = range(-50, 50)
        for item in t:
            b = math.sin(item)
            my.append(b)
            mylist = array(my)
            
            plt.cla()
            plt.plot(my[-20:], '-r')
            #analyzing the plot components
            a = plt.get_backend()
            c = plt.isinteractive()
            
            # analyzing the axis commands
            z = plt.axis() 
            v =  plt.get_plot_commands() 
            #plt.draw()
            fig.canvas.draw()
            self.logger.debug("PLT.GET_NEXT_COMMANDS OUTPUT RESPONS: " + repr(v) )
        self.logger.debug("PLT.GET_BACKEND OUTPUT: " + repr(a) )
        #self.logger.debug("PLT.GET_NEXT_COMMANDS OUTPUT RESPONS: " + repr(d) )
        self.logger.debug("PLT.AXIS COMMAND OUTPUTANSWER TO PLT.AXIS: " + repr(z) )
    
    def test17(self):
        '''using a function to update the plot currently this is not what is happening'''
        # removed the def update_line() function
        # note that by using list comprehension the first 20 points are auto plotted 
        
        fig = plt.figure(1)
        import math
        my = []
        v=[]
        t = range(-50, 50)
        b = [ math.sin(i) for i in t]
        
        #def update_line():
        for item in b:
            v.append(item)
            ans = array( v[-15:] )
            plt.cla()
            plt.ylim((-1,1)) # locks axis into place?? bad right 
            plt.plot( ans )
            plt.show(block = False) 
            fig.canvas.draw()
        self.logger.debug("PLT.GET_BACKEND OUTPUT: " + repr(plt.get_plot_commands()) )
        
    
    def test18(self):
        '''using two functions to graph the plot in real time using a for loop 
        function needs to update the plot only this is still not happening yet 
        '''
        #USELESS TEST FUNCTION NEED REPAIRING
        # note that by using list comprehension the first 20 points are auto plotted 
        fig = plt.figure(1)
        import math
        my = []
        v=[]
        t = range(-50, 50)
        b = [ math.sin(i) for i in t]

        for item in b:
            def update_line():
                for item in b:
                    v.append(item)
                    self.ans = array(v[-10:])
                #return self.ans
                
            def graph():
                plt.cla()
                plt.ylim((-1,1)) # locks axis into place?? bad right 
                plt.plot(self.ans)
                plt.show(block = False)
                fig.canvas.draw()
            #self.logger.debug("PLT.GET_BACKEND OUTPUT: " + repr(plt.get_plot_commands()) )
            update_line()
            graph()
    
    def test19(self):
        '''testing the set_ydata function based on line.get_path results seems to be replacing the data but it is not it's 
        simply just animating it like an artist would'''
        self.logger.info("Starting TEST19")
        x = arange(0,2*pi,0.01)            # x-array
        self.logger.debug(" x array: %s" % repr(x))
        self.logger.debug(" sin(x): %s" % repr(sin(x)))
        
        line, = plt.plot(x,sin(x))
        for i in arange(1,100):            #changed from 200 to 10,000
            self.logger.debug("i: %s, x+i/10.0: %s, sin(x+i/10.0): %s" % (str(i), str(x+i/10.0), str(sin(x+i/10.0))) )
            line.set_ydata(sin(x+i/100.0))            # update the data
            plt.draw()     
            time.sleep(1)
        self.logger.debug("ORIGINAL: " + repr(line.get_path()))            
        self.logger.debug("PLT.GET_BACKEND OUTPUT: " + repr(plt.get_plot_commands()) )
        self.logger.debug("ans: " + repr(line.get_data()))
    
    def test20(self):
        '''using importmath to make the function work'''
        import math
        #my = []
        #v=[]
        t = range(-50, 50)
        b = [math.sin(i) for i in t]
        new_data = []
        
        #def update_graph(a, new_data): 
        
        def graph(n_d):
            plt.cla()
            plt.plot(new_data[-10:]) #, = plt.plot([], [])
            plt.draw()
            #plt.clf()
        
        for item in b:
            new_data.append(item)
                #plt.draw()
                #y.append(item)
            graph(new_data)
    
    def test21(self):
        '''making a *arg in a function for line by line realt time graph
        this is already being done by me in tests 31-34'''
        b = []
        c = []
        
        def graph(n_d, n_d1):
            plt.cla()
            #plt.plot(n_d[0], n_d[1], 'ro')
            plt.plot( n_d[-10:], n_d1[-10:] )
            plt.draw()

        f = open("xxx4.csv", "r")
        for line in f:
            #a = line.strip().split(',')
            b.append((line.strip().split(',')))
            A = array(b, int)
            p1, p2 = A.T
            A = array(b, int)
            #b = array(a[0], int)
            #c = array (a[1], int) 
            #d = concatenate ( (c) )
            #graph(array1, array2)    
            graph(p1,p2)
            
    def test22(self):
        '''testing a 2 column csv array for simplicity sakes only  '''
        b=[]
        def graph(n_d, n_d1):
            plt.cla()
            plt.plot( n_d[-10:], n_d1[-10:] )
            plt.draw()
            
        f = open("xxx3.csv", "r")
        for line in f:
            b.append((line.strip().split(',')))
            A = array(b, int)
            p1,p2,p3,p4,p5 = A.T
        
            graph(p1,p2)
            #a = line.strip().split(',')
            #b.append(float(a[0]))
            #c.append(float(a[1]))
            #p1, p2 = 
    
    def test23(self):
        '''testing a 5 column csv array mimicking actual beastie data type'''
        b=[]
        def graph(n_d, n_d1):
            plt.cla()
            plt.plot( n_d[-10:], n_d1[-10:] )
            plt.draw()
        
        f = open("xxx3.csv", "r")
        for line in f:
            b.append((line.strip().split(',')))
            A = array(b, int)
            #print repr(A
            p1,p2,p3,p4,p5 = A.T
            graph(p1,p2)

    def test24(self):
        '''using kwargs to get stuff done not very helpful but interesting idea'''
        def myplot(x, y, **kwargs):
            "make plot of x,y. save to fname if not None. provide kwargs to plot"
            plt.plot(x, y, **kwargs)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('xxx')
        
            plt.show()

        x = [1, 3, 4, 5]
        y = [3, 6, 9, 12]

        myplot(x, y, marker='s')
        #myplot(x, y, 'images/myfig2.png', **d)
    
    def test25(self):
        '''creating a large two class array for beastie simulation'''
        
        filename = "EXTRA.csv"
        NEWLINE = "\n"
        myfile = open(filename, "w")
        x = arange(0,2*pi,0.01) 
        
        #making the csv file 
        for item in range(len(x)):
            val1 = sin(item)
            newrow = str(item) + ","
            newrow +=str(val1) + ","
            newrow += (NEWLINE)
            myfile.write(newrow)
        myfile.close()
    
    def test26(self):
        '''creating a reference png image for analysis'''
        fig = plt.figure(1) 
        ax1 = fig.add_subplot(1,1,1) #1,1,1) # or plt.subplot(1,1,1)
        #ax1.set_xlim(0. , 7)
        ax2 = ax1.twinx()
        #ax2.set_xlim(0, 7)
        c=[]

        def graph_1(n_d, n_d1, n_d2):
            self.xaxis = n_d
            #xval = n_d[-100:]
            ax1.plot(n_d, n_d1, "-m")
            #ax2.cla()
            #plt.autoscale(enable = True, axis = 'both', tight = True)
            ax2.plot( n_d, n_d2, "-r")
            # no difference betwen fig.canvas.draw() or plt.draw()
            #fig.canvas.draw()
            #plt.draw()
            #make the png image save to a specific already made folder
            #fig.savefig('New Folder/test.png', bbox_inches='tight', transparent=True, pad_inches=0)
            fig.savefig('reference_1.png', bbox_inches='tight', transparent=True, pad_inches=0)
            plt.show()
            plt.close()
            
            img=mpimg.imread('ref.png')
            img2=mpimg.imread('reference_1.png')
            self.logger.debug("x axis " + repr(self.xaxis) )
            #self.logger.debug("y axis " + repr(n_d1) )
            #comparing the entire contents of both arrays
            #self.assertEqual(img.all(), img2.all())
            

        f = open("EXTRA.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append( (b[2], b[5], b[6]) )
            e = array(c)
        graph_1( e[:,0], e[:,1], e[:,2] )
        
        #opening both files as a array so they can be compared completlely as two array's
        #img=mpimg.imread('ref.png')
        #img2=mpimg.imread('reference_1.png')
        #self.logger.debug(img2)
        #comparing the entire contents of both arrays
        #self.assertEqual(img.all(), img2.all())
        

    def test27(self):
        '''running two clolumn array simulator creating lists and manually converting the lists to an array
        used a transpose function saw it doesn't work and help '''
        b=[]
        c=[]
        d=[]
        def graph(n_d, n_d1):
            plt.cla()
            plt.plot( n_d[-10:], n_d1[-10:] )
            plt.draw()
            
        f = open("xxx.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append(b[2])
            d.append(b[3])
            e = array(c)
            f = array(d)
            #A = array([c,d])
            #p1,p2= A.T
            #graph(c,d)
            graph(e,f)
        self.logger.debug("array length: " + repr(len(c)))  
        
    def test28(self):
        '''testing two column array test25() however making a tuple of the points and manual converting appending list to array'''
        b=[]
        c=[]
        d=[]
        def graph(n_d, n_d1):
            plt.cla()
            plt.plot( n_d[-10:], n_d1[-10:], )
            plt.draw()
            
        f = open("EXTRA.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append( (b[2], b[3]) )
            #d.append(b[1])
            e = array(c)
            #f = array(d)
            graph( e[:,0], e[:,1] )
            
    def test29(self):
        '''using the transpose function A.T for simulation purposes''' 
        b=[]
        c=[]
        d=[]
        
        def graph(n_d, n_d1, **kwargs):
        #def graph(**kwargs):
            plt.cla()
            plt.plot( n_d[-15:], n_d1[-15:], **kwargs)
            #plt.plot( n_d, n_d1, **kwargs)
            plt.draw()
            
        # using a kwargs not very helpful though 
        ok = {"color": "magenta", "marker": "d"}
        
        f = open("EXTRA.csv", "r")
        for line in f:
            b = line.strip().split(",")
            c = (float(b[2]), float(b[3]) )
            d.append(c)
            A = array(d)
            p1,p2 = A.T
            graph(p1, p2, **ok)
    
    def test30(self):
        '''creating a 5 column array CSV file called Extra for simulation purposes. Alternate columns are sinx * a factor for up and down transitions/transpositions '''
        filename = "EXTRA.csv"
        NEWLINE = "\n"
        myfile = open(filename, "w")
        x = arange(0,2*pi,0.01)
        start = time.time()        
        # creating the csv file  
        for num in x:
            #print x
            elapsed = time.time() - start
            val1= sin(num)
            val2 =sin(num*3)
            val3 = sin(num*5)
            val4 = sin(num*7)
            
            newrow = time.strftime('%H:%M:%S, ')
            newrow += str(elapsed) + ","
            newrow += str(num) + ","
            newrow +=str(val1) + ","
            newrow +=str(val2) + ","
            newrow +=str(val3) + ","
            newrow +=str(val4) + ","
            newrow += (NEWLINE)
            myfile.write(newrow)
        myfile.close()
    
    def test31(self):
        '''plotting two sine waves together simultaneously as a function of time '''
        fig = plt.figure(1) 
        ax1 = plt.subplot(1,1,1)
        ax2 = ax1.twinx()
        c=[]
        real_val = True
        real_val2 = False
        self.counter = 0
        self.count = 0
        
        canvas1 = ax1.figure.canvas
        canvas2= ax2.figure.canvas
        background = canvas1.copy_from_bbox(ax1.bbox)
        background2 = canvas2.copy_from_bbox(ax2.bbox)
        
        def sav_graph(bar1,bar2, x):
            plt.savefig("New Folder/xxx_%s.png" %x, frameon = True) # self.count)
        
        def graph(n_d, n_d1, n_d2):
            self.count +=1
            self.counter += 1
            xval = n_d[-50:]
            canvas1.restore_region(background)
            ax1.cla()
            line1=ax1.plot(xval, n_d1[-50:],"-mo")
            
            canvas2.restore_region(background2)
            ax2.cla()
            line2=ax2.plot( xval, n_d2[-50:], "-ro" )
            
            if self.counter == 50:
                sav_graph(line1,line2,self.count)
                #plt.savefig("New Folder/xxx_%s.png" %self.count)
                self.counter = 0
            
            plt.draw()
            
            #testing to prove that indeed the first value in the xval is always smaller then the back one 
            if len(xval) < 50:
                ans1 = False
                self.assertEqual(real_val2, ans1)
            else:
                ans3 = True # true that we have reached the limit above 50
                a1 = xval[0]
                a2 = xval[1]
                a3 = xval[48]
                a4 = xval[49]
                ans=(a1<a2)
                ans2=(a3<a4)
                #proving the axis indeed is of lenght 50
                self.assertEqual(real_val, ans3)
                #testing lower bound of axis limit
                self.assertEqual(real_val, ans)
                # testing upper bound of axis limit
                self.assertEqual(real_val, ans2)
                
        f = open("EXTRA.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append( (b[2], b[5], b[6]) )
            e = array(c)
            graph( e[:,0], e[:,1], e[:,2] )

    def test32(self):
        '''testing the vanishing plots by having fixed plots of 0 
        some plants 
        tried to test other class imports realized they don't help at all inital ideas have been asteriked out'''
        #http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
        #http://matplotlib.org/api/backend_bases_api.html?highlight=interactive
        #import matplotlib.figure as Fig
        #ok = Fig.Figure(figsize=(3,3), frameon=True, tight_layout=True)
        fig = plt.figure(1) 
        ax1 = fig.add_subplot(1,1,1) # or plt.subplot(1,1,1)
        plt.box('on') # makes the white box in the background
        
        ax2 = ax1.twinx()
        #ax2.ylim(-1,1)
        #plt.figure = (figsize=(8,6), dpi=80)
        #ax1 = plt.subplot(1,1,1)
        #plt.autoscale(enable = True, axis = 'x', tight = True)
        #plt.axes(axisbg = 'w',sharex)
        c=[]

        def graph(n_d, n_d1, n_d2):
            xval = n_d[-50:]
            ax1.cla()
            ax1.plot(xval, n_d1[-50:],"-m")
            ax2.cla()
            ax2.plot( xval, n_d2[-50:], "-r" )
            #plt.ginput(n=1, timeout = 10, show_clicks=True, mouse_stop=2)
            plt.draw()
            
        f = open("xxx.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append( (b[2], b[5], b[6]) )
            e = array(c)
            graph( e[:,0], e[:,1], e[:,2] )
    
    def test33(self):
        '''testing the Figure and other classes  by being directly called '''
        fig = plt.figure(1)
        ax1 = fig.add_subplot(1,1,1) 
        ax2 = ax1.twinx()
        c=[]
        
        self.counter = 0
        self.count = 0
        
        canvas1 = ax1.figure.canvas
        canvas2= ax2.figure.canvas
        background = canvas1.copy_from_bbox(ax1.bbox)
        background2 = canvas2.copy_from_bbox(ax2.bbox)
        
        def sav_graph(bar1,bar2, x):
            plt.savefig("New Folder/xxx_%s.png" %x, frameon = True)
            
        def graph(n_d, n_d1, n_d2):
            self.count +=1
            self.counter += 1
            xval = n_d[-100:]
            
            canvas1.restore_region(background)
            ax1.cla()
            plt.autoscale(enable = True, axis = 'both', tight = True)
            line1 = ax1.plot(xval, n_d1[-100:], "-m")
            
            canvas2.restore_region(background2)
            ax2.cla()
            plt.autoscale(enable = True, axis = 'both', tight = True)
            line2 = ax2.plot( xval, n_d2[-100:], "-r")
            
            if self.counter == 50:
                sav_graph(line1,line2,self.count)
                self.counter = 0
                
            plt.draw()
 
        f = open("xxx.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append( (b[2], b[5], b[6]) )
            e = array(c)
            graph( e[:,0], e[:,1], e[:,2] )

    def test34(self):
        '''ditching the idea of two lines in one graph it is a slower process speed wise
        hence making two separate subplots use below to get an idea of using artist class to use draw 
        to increase speed'''
        #http://wiki.scipy.org/Cookbook/Matplotlib/Animations#head-5fdb5aca449e867379b1830a01e113c69e015554
        #http://matplotlib.org/api/artist_api.html?highlight=draw#matplotlib.artist.Artist.draw
        fig = plt.figure(1)
        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)
        
        canvas = ax1.figure.canvas
        canvas2 = ax2.figure.canvas
        background = canvas.copy_from_bbox(ax1.bbox)
        background2 = canvas.copy_from_bbox(ax2.bbox)
        
        c=[]
        
        def graph(n_d, n_d1, n_d2):
            # restore the clean slate background
            canvas.restore_region(background)
            
            xval = n_d[-50:]
            ax1.cla()
            ax1.set_ylim( -2. ,  2. )
            ax1.plot(xval, n_d1[-50:],"-m")
            plt.autoscale(enable = True, axis = 'both', tight = True)
            canvas2.restore_region(background2)
            ax2.cla()
            plt.autoscale(enable = True, axis = 'both', tight = True)
            ax2.plot( xval, n_d2[-50:], "-r" )
            plt.draw()
            
        f = open("EXTRA.csv", "r")
        for line in f:
            b= line.strip().split(',')
            c.append( (b[2], b[5], b[6]) )
            e = array(c)
            graph( e[:,0], e[:,1], e[:,2] )

    def test35(self):
        '''popping several items and refreshing the list itself does nothing''' 
        #http://wiki.scipy.org/Cookbook/Matplotlib/Animations#head-5fdb5aca449e867379b1830a01e113c69e015554
        #list = list[ : -100 ]
        counter = 0
        c=[]
        d=[]
        e=[]
        
        f = open("xxx.csv", "r")
        for line in f:
            counter += 1
            b= line.strip().split(',')
            c.append(b[2])
            d.append(b[5])
            e.append(b[6])
            self.logger.debug(repr(c))
            
            if  counter==10:
                #c =c[:-10]
                #d =d[:-10]
                #e =e[:-10]
                #self.m.graph(c,d,e)
                self.m.graph(c[-10:],d[-10:],e[-10:]) 
                counter = 0
            #else:
              #  f = c[:-100]
               # g = d[:-100]
               # h = e[:-100]
                #print f
                
    def test36(self):
        '''moving test35() to graphclass and testing its simulation via for loop and measuring cpu and elapsed 
        time'''
        now = time.clock()
        nowc = time.time()
        c=[]
        #timelist = []
        #cpulist = []
        
        f = open("xxx.csv", "r")
        for line in f:
            now2 = time.clock() - now
            now3 = time.time() - nowc
            b= line.strip().split(',')
            c.append( (b[2], b[5], b[6]) )
            e = array(c)
            self.m.graph( e[:,0], e[:,1], e[:,2] )
            #timelist.append(now2)
            #cpulist.append(now3)
            #self.logger.debug("CPU time in test35() for loop: " + repr(now2) )
            #self.logger.debug("elapsed time in test35() for loop: " + repr(now3) )
        
        # measuring the AVERAGE elapsed time
        #average = sum(timelist)/len(timelist)
        #average2 = sum(cpulist)/len(cpulist)
        #self.logger.debug("AVERAGE TIME in test35() for loop: " + repr(average) )
        #self.logger.debug("CPU TIME in test35() for loop: " + repr(average2) )
    
    
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Graphclass Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    unittest.main()