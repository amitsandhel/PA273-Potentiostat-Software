#!/usr/bin/python
# encoding: utf-8
# test_beastie.py
'''
Created by Amit Sandhel.
This module is tests the py273_v2.py script
'''
import sys
import os
import unittest
import time
import logging
#import pprint
#pp = pprint.pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#print "\nNew System Path:"
#pp(sys.path) 

#importing beastie module for testing 
import pa273_v2

pa273_v2.Serial = pa273_v2.Fake_Serial

class pa273_v2test(unittest.TestCase):
    '''unittest class for testing and TDD of beastie.py script ONLY'''
    
    def setUp(self):
        self.m= pa273_v2.MySerialPort()
        self.m.open_port()
        self.debug = True
        self.logger = logging.getLogger('MAIN')
        
    def tearDown(self):
        self.m.close_port()
    
    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
    def test01(self):
        ''' Test basic command list parsing  '''
        test_commands = (
            ("0, BIAS -200"),
            ('100, BIASS'),
            ('200, BIAS -300'),
            ('300, BIASS'),
            ('400, BIAS 400'),
            ("500, BIASS"),
        )
        self.m.parse_commands(test_commands)
        self.assertEqual(len(test_commands), len(self.m.command_dict))
        for item in test_commands:
            time, cmd = item.strip().split(",")
            self.assertEquals(self.m.command_dict[float(time)], (cmd.strip(), ) )
    
    def test02(self):
        ''' testing the readfiles command'''
        '''verifying the right file is even opened to begin with'''
        file2 = None
        #self.b = self.m.readfiles()
        self.assertEqual(file2, None) #self.m.readfiles())
        
    def test03(self):
        '''testing the read_command() function
        specifically the self.cmd_output variable
        '''
        self.m.command_dict = {0:("BIAS 200",), 2: ("BIAS 400",), 3:("BIAS 300",) }
        sorted_list = [0, 2,3]
        self.m.read_command()
        self.assertEqual(sorted_list, self.m.cmd_output)
    
    def test04(self):
        ''' testing the get_next_command() 
        testing the efficiency of the reply command and that it 
        is reporting the value that is expected with the correct 
        time index        
        '''
        self.m.command_dict = {0:("BIAS 200",), 3: ("BIAS 500",), 5:("BIAS 300",),4: ("BIAS 400",)}
        self.m.cmd_output = [0,3,4,5]
        
        keylist = [0,3,4,5]
        cmd = [('BIAS 200',), ('BIAS 500',),('BIAS 400',),('BIAS 300',)]
        
        for x in range(4):
            a = keylist.pop(0)
            b = cmd.pop(0)
            reply2 = (a,b)
            next_time, next_cmd = self.m.get_next_command()
            reply = (next_time, next_cmd)
            self.assertEqual(reply2, reply) 
            
    def test05(self):
        ''' testing the while function in get_next_command 
        itself with a correct timer
        '''
        self.m.command_dict = {1: ("BIAS 200",), 3: ("BIASS",), 8:("BIAS 300",), 6: ("BIAS 400",)}
        self.m.cmd_output = [1,3,6,8]
        # using this keylist_output and the cmdlist_output lists to compare the outputs from the next_time and next_cmd if loop
        keylist_output = [1.0,3.0,6.0,8.0]
        cmdlist_output = [('BIAS 200',), ('BIASS',),('BIAS 400',),('BIAS 300',)]
        
        start_time = time.time()
        new_time = 0
        
        while True:
            elapsed_time = time.time() - start_time
            #next_time, next_cmd = self.m.get_next_command()
      
            #if start_time > 0:
            if elapsed_time >= new_time:
                    
                if len(self.m.cmd_output) == 0:
                    self.assertEqual(0, len(self.m.cmd_output)) 
                    break 
                #    else:
                next_time, next_cmd = self.m.get_next_command()
                reply = (next_time, next_cmd)
                #print (time.time(), reply)
                new_time = reply[0]
                
                self.assertEqual(keylist_output.pop(0), next_time)
                self.assertEqual(cmdlist_output.pop(0), next_cmd)
    
    def test06(self):
        '''testing the time_meter_command() function which 
        is the while true loop found in test05 which is rebuilt
        '''
        self.m.command_dict = {1: ("BIAS 200",), 3: ("BIAS 500",), 5:("BIAS 300",), 4: ("BIAS 400",)}
        self.m.cmd_output = [1,3,4,5]
        # using this keylist_output and the cmdlist_output lists to compare the outputs from the next_time and next_cmd if loop
        keylist_output = [1.0,3.0,4.0,5.0]
        cmdlist_output = [(1.0,('BIAS 200',)), (3.0, ('BIAS 500',)),(4.0, ('BIAS 400',)),(5.0, ('BIAS 300',))]
        
        for x in range(3):
            next_time = self.m.run() #time_meter_command()
            break
            self.assertEqual(cmdlist_output.pop(0), next_time)
 
    
    def test07(self):
        '''testing the execute_command() 
        with the simulator
        '''
        self.m.command_dict = {"2": ("BIAS 200",), "3": ("BIAS 250",), "4":("BIAS 300",),"5": ("BIAS 400",),
        "6": ("BIAS 500",), "7": ("BIAS 550",), "10":("BIAS 600",), "15": ("BIAS 700",)}
        self.m.cmd_output = ['2', '3']
        #self.m.run() #time_meter_command()
    
    def test08(self):
        '''testing the entire time_meter_command() function
        simply by running the time_meter_command() function as is
        '''
        self.m.run() #time_meter_command()
    
    def test09(self):
        '''converted test10() into a class and moved upwards the class works successfully 
        now onwards to real time'''
        #self.n.make_graph()
        '''
        IMPORTANT IMPORTNAT IMPORNTAT LINK PLEASE LOOK AT 
        ESPECIALLY THE TOP THREE WEBSITES
        http://stackoverflow.com/questions/17518085/python-real-time-plotting-memory-leak
        http://stackoverflow.com/questions/17039901/plot-time-values-with-matplotlib
        http://synesthesiam.com/posts/an-exercise-with-functions-and-plotting.html
        
        http://matplotlib.org/users/recipes.html
        http://stackoverflow.com/questions/1574088/plotting-time-in-python-with-matplotlib
        http://www.loria.fr/~rougier/teaching/matplotlib/#simple-plot
        http://matplotlib.org/users/pyplot_tutorial.html
        http://matplotlib.org/examples/index.html
        '''
        pass 

###########################################################################    
if __name__ == '__main__':
    unittest.main()
  