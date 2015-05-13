#!/usr/bin/python
# encoding: utf-8
#test_main.py

#http://docs.python.org/2/howto/argparse.html#id1

import sys
import os
import unittest
import logging
import argparse

#importing the main class
import main

class MainTest(unittest.TestCase):
    '''unittest class for testing and TDD'''
        
    def setUp(self):
        self.parser = main.setup_parser()
        #self.m = main.Main(parser)
        #self.ans = main.setup_parser()
        #self.m = main.Main(self.ans)
        #self.m = main(parser)
        #self.debug = False
        self.debug = True
        self.logger = logging.getLogger('MAIN')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
    def test01(self):
        '''test SIM mode command line argument'''
        m = main.Main(self.parser)
        args = parser.parse_args()
        self.sim = args.sim
        #self.debug = args.debug
        #parser.sim = self.m.sim
        #ans = main.setup_parser() 
        #m = main.Main(ans)
        #self.ans.sim = self.m.sim
        #print ans
        #print 'dir', dir(ans)
        #print 'type',type (ans)
        #self.ans.sim = True # = "--sim"
        #ans.sim = True
        #ans = "--sim"
        #m = main.Main(ans)
        #self.m(self.ans)
        #m.run()
        #m = main.Main(main.parser)
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
  