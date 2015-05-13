#!/usr/bin/python
# encoding: utf-8
#maintest.py
"""
Created by Amit Sandhel on 2013-05-27.
Copyright (c) 2013  All rights reserved.
This module is to probe a COM port for the beastie potentiostat named Grimlock after Transformers

This script tests the beastie potentiostat using unittests

work in progress
"""


import sys
import os
import unittest
import time
import logging
import argparse
#http://docs.python.org/2/howto/argparse.html#id1
#importing the testing class
import main

class MainTest(unittest.TestCase):
    '''unittest class for testing and TDD'''
        
    def setUp(self):
        self.ans = main.setup_parser()
        self.m = main.Main(self.ans)
        #self.m = main(parser)
        #self.debug = False
        self.debug = True
        self.logger = logging.getLogger('MAIN')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
    def test01(self):
        '''test SIM mode command line argument'''
        #ans = main.setup_parser() 
        #m = main.Main(ans)
        self.ans.sim = self.m.sim
        #print ans
        #print 'dir', dir(ans)
        #print 'type',type (ans)
        #self.ans.sim = True # = "--sim"
        #ans = "--sim"
        #self.m(self.ans)
        #m.run()
        #m = main.Main(main.parser)
        self.assertEqual(self.ans.sim, False)
    
    def test02(self):
        '''test Version and all paramter settings mode command line argument
        note that store_true means that the DEFAULT SETTING is False and store_false means the default setting 
        is FALSE have to get explanation for this'''
        #ans = main.setup_parser() #okparser.parse_args(bar ="--sim")
        #ans.sim = True # = "--sim"
        #ans = "--sim"
        #m = main.Main(ans)
        self.ans.sim = self.m.sim
        self.ans.debug = self.m.debug
        self.ans.version = self.m.version
        self.ans.test = self.m.test
        self.ans.postrun = self.m.postrun
        #m = main.Main(main.parser)
        self.assertEqual(self.ans.sim, False)
        self.assertEqual(self.ans.debug, False)
        self.assertEqual(self.ans.version, 1)
        self.assertEqual(self.ans.test, False)
        self.assertEqual(self.ans.postrun, False) #this was changed from store_false to store_true otherwise the graph does not even print out
    
    def test03(self):
        import argparse
        from main import setup_parser as sp
        import beastie_test
        parser = sp()
        b= Main(parser)
        b.run()  
        #ok = beastie.
        

###########################################################################    
if __name__ == '__main__':
    unittest.main()
  