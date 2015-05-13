#!/usr/bin/python
# encoding: utf-8
#test_main.py
'''
Created by Amit Sandhel on 2013-05-27.
Copyright (c) 2013  All rights reserved.
This module tests the main.py script
'''

#http://docs.python.org/2/howto/argparse.html#id1
#NOTE THAT TO RUN THE UNITTEST DISCOVER REQUIRES THE FOLLOWING LINE:
    # python -m unittest discover -s test -p "test*"

#import sys
#import os
import unittest
import logging
import argparse
#import pprint
#pp = pprint.pprint

# For test modules, they need access to the Mudule Under Test, which is in the folder above.
# So we append that folder to the system PATH so our import will work.
#print "Calculate path to parent folder: ", os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#print "Existing System Path:"
#pp(sys.path) 
# http://docs.python.org/2/library/sys.html#sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#print "\nNew System Path:"
#pp(sys.path) 

#importing the main class
import main

class MainTest(unittest.TestCase):
    '''unittest class for testing and TDD'''
        
    def setUp(self):
        self.parser = main.setup_parser()
        self.debug = True
        self.logger = logging.getLogger('MAIN_test')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
    def test01(self):
        '''test SIM mode command line argument'''
        m = main.Main(self.parser)
        args = parser.parse_args()
        self.sim = args.sim
        self.assertEqual(self.sim, False)
    
    def test02(self):
        '''test Version and all paramter settings mode command line argument
        note that store_true means that the DEFAULT SETTING is False and store_false means the default setting 
        is FALSE have to get explanation for this'''
        #ans = main.setup_parser() #okparser.parse_args(bar ="--sim")
        #ans.sim = True # = "--sim"
        #ans = "--sim"
        #m = main.Main(ans)
        self.parser.sim = self.m.sim
        self.parser.debug = self.m.debug
        self.parser.version = self.m.version
        self.parser.test = self.m.test
        self.parser.postrun = self.m.postrun
        #m = main.Main(main.parser)
        self.assertEqual(self.ans.sim, False)
        self.assertEqual(self.ans.debug, False)
        self.assertEqual(self.ans.version, 1)
        self.assertEqual(self.ans.test, False)
        self.assertEqual(self.ans.postrun, False) #this was changed from store_false to store_true otherwise the graph does not even print out
   
###########################################################################    
if __name__ == '__main__':
    unittest.main()
  