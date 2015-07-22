import wx
import wxgui
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
# safest way to import the myserialport class for versions 1 and 2
from pa273_v1 import MySerialPort as MySerialPort
from pa273_v2 import MySerialPort as MySerialPort2
# import numpy (needed indirectly for graphing)
import numpy as np
import pylab

"""wxmain.py
Created by Amit Sandhel with contributions by Fredrick Leber.
This script is the main (engine) script for the gui (Graphical User Interface)

DO NOT EVER IN THE HISTROY OF YOUR SANE MIND AND LOGIC EVER TOUCH THE
FILE CALLED wxgui.py

THAT FILE IS GENERATED FROM THE WXGLADE AND IS THE SKELETON FILE TO THE
GRAPHICAL INTERFACE. WE ARE GOING TO USE IT TO SIMPLY IMPORT THE SKELETON AND
THEN USING SUPER "OVERRIDE" THE FUNCTIONS AS WE SEE FIT AND NEED.

THE ADVANTAGE OF WXGLADE IS THAT IT HELPS US DEVELOP THE GUI FRAMEWORK
RELATIVELY EASILY OTHER GUI OPTIONS ARE KIVY, BOA CONSTRUCTOR (A FULL IDE) AND
POSSIBLY EVEN I-PYTHON ARE POSSIBILITIES

References:
https://blog.laslabs.com/2013/02/super-raises-typeerror-must-be-type-not-
classobj/
http://stackoverflow.com/questions/1713038/super-fails-with-error-typeerror-
argument-1-must-be-type-not-classobj
http://stackoverflow.com/questions/3877209/how-to-convert-an-array-of-strings-
to-an-array-of-floats-in-numpy
http://learnpythonthehardway.org/book/ex44.html
"""

NEWLINE = "\n"
DEFAULTCOM = "COM4"
FILENAMEv1 = "SingleVoltageData.csv"
FILENAMEv2 = "WaveformData.csv"


class Version1(MySerialPort):
    """Version 1 is the parent class that inherits properties from the v1
    MySerialPort. This way we can modify functions and inherit all variables
    from the parent class as well for this we use the Super() Function which is
    designed for new style classes.
    """
    def __init__(self, bias):
        # bias variable will be passed into the class by the gui
        self.bias_Val = bias
        super(Version1, self).__init__(bias)

    def bias(self):
        '''Rewriting the bias function using the pass in parameter rather than
        input() function used by parent class.
        '''
        self.send('BIAS %s \n' % str(self.bias_Val))
        return self.receive(15)  # 13 AT MAX VALUE


class MyFrame(wxgui.MyFrame):
    """MyFrame is a class that is inheriting from the wxgui script
    here we are making an instance of the class there and 'overriding' the
    functions as needed. i.e we are writing what those functiosn are supposed
    to do rather than be empty varaibles.
    NEVER TOUCH THE WXGUI SCRIPT AS IT IS IMPORTED AND MODIFIED HERE
    All event.skip() functions MUST Be kept in all widget event functions.
    """
    def __init__(self, *args, **kwds):
        super(MyFrame, self).__init__(*args, **kwds)

        """Version 1 command initalization"""
        # sim value from sim toggle button
        self.sim_value = self.button_sim.GetValue()
        # port value for version 1
        self.port_value = DEFAULTCOM
        # get the bias value default value is set to 1 in the wxgui widget
        self.bias_value = self.spin_ctrl_bias.GetValue()
        # opening the version 1 MyserialPort class using the Inherited class
        self.myfile1 = Version1(self.bias_value)

        # writing down csv filename
        myfile = open(FILENAMEv1, "a")
        myfile.write("new data," + time.strftime("%d/%m/%Y") + NEWLINE)
        myfile.write("Time,BIAS,Measured Voltage,Current,CurrentExp,CHARGE(Q),\
Qexp" + NEWLINE)
        myfile.close()

        # the timer function is used for looping over version 1 software
        # Note: version 2 does not need this wx timer due to built in while
        # loop in run function
        # Timer class event
        self.redraw_timer = wx.Timer(self)
        # Binding class to redraw() function
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)

        """version 2 command initalization"""
        # version 2 sim setting
        self.sim_value_v2 = self.button_sim_v2.GetValue()
        # setting the com port value for vesrion 2 to the default value
        self.port_value_v2 = DEFAULTCOM
        # opening version 2 MyserialPort class
        self.myfile2 = MySerialPort2()

        # empty array of the bias and current y values for
        # version 2 (labelled v2)
        self.bias_v2 = []
        self.current_v2 = []

        # plot initialization for the static graph  done here for both versions
        self.init_plot()

    def On_Sim(self, event):  # wxGlade: MyFrame.<event_handler>
        """This function is the event for the SIM toggle button and stores the
        value into a self variable.
        This is the toggle button for version 1
        """
        self.sim_value = self.button_sim.GetValue()
        event.Skip()

    def On_Port(self, event):  # wxGlade: MyFrame.<event_handler>
        """This function isets the com port number for version 1
        AMIT NOTE: THE USER BETTER KNOW HOW TO FIND THE COMPORT HIMSELF
        THIS DOES NOT HELP YOU FIND IT IN ANY WAY
        """
        ans2 = self.spin_ctrl_port.GetValue()
        # store local variables and converting into string variable
        self.port_value = "COM" + str(ans2)
        event.Skip()

    def On_bias(self, event):  # wxGlade: MyFrame.<event_handler>
        """This function is to set the bias from 8000 mV to -8000 mV from a
        spin control widget for Version 1.
        NOTE: if a value beyond the range is given the entire system will crash
        """
        # TODO: so need to write a text box in the widget guito talk about this
        ans = self.spin_ctrl_bias.GetValue()
        self.myfile1.bias_Val = ans
        event.Skip()

    def On_Start(self, event):  # wxGlade: MyFrame.<event_handler>
        """Function for start button with a built in timer for 9 ms and runs
        the version 1 MySerialPort.run() class with the memory swapped
        open_port() function"""
        # running the redraw timer
        self.redraw_timer.Start(9)
        # run the version 1 run() function
        self.run_engine_v1()
        # redrawing the plot
        self.redraw_plot(event)
        event.Skip()

    def On_Pause(self, event):  # wxGlade: MyFrame.<event_handler>
        """The pause button to pause the experiment"""
        print "Experiment Paused!"
        self.redraw_timer.Stop()  # stop the timer
        event.Skip()

    def On_Close(self, event):  # wxGlade: MyFrame.<event_handler>
        """This function is the close button it closes the interface """
        self.redraw_timer.Stop()  # Stop timer
        self.Destroy()  # Destroy all widgets
        event.Skip()

    def open_port_rev(self, port=DEFAULTCOM, baudrate=19200, bytesize=8,
                      parity='N', stopbits=1, timeout=1, xonxoff=False,
                      rtscts=False, writeTimeout=3, dsrdtr=False,
                      interCharTimeout=None):
        '''This is opening a self.s port however this is a revised port for
        memory swap purposes.
        '''
        # this if loop determines which sim parameter you need and opens the
        # associated serial port
        # TODO: but you can only run this once then you must disable the
        # widgets to close the program
        if self.sim_value is True:
            # import the fake serial class
            from Fake_Serial import Fake_Serial
            self.myfile1.s = Fake_Serial(port, baudrate, bytesize, parity,
                                         stopbits, timeout, xonxoff, rtscts,
                                         writeTimeout, dsrdtr,
                                         interCharTimeout)
        else:
            # import the real serial class
            from serial import Serial
            self.myfile1.s = Serial(port, baudrate, bytesize, parity, stopbits,
                                    timeout, xonxoff, rtscts, writeTimeout,
                                    dsrdtr, interCharTimeout)

    def v1_exp_setup(self):
        """Modified run function for Version 1."""
        self.myfile1.bias()
        self.myfile1.measure_values()
        self.myfile1.record_data()
        # appending values to text ctrl widgets
        self.text_ctrl_bias.AppendText(str(self.myfile1.measuredBIAS) + "\n")
        self.text_ctrl_current.AppendText(str(self.myfile1.reply_current) +
                                          "\n")
        time.sleep(0.1)  # switched from 0.3

    def run_engine_v1(self):
        """The run function engine to start the experiment."""
        self.open_port_rev(port=self.port_value)
        self.v1_exp_setup()
        # initalizing the new variables into the class again
        self.myfile1.bias_val = self.bias_value
        self.myfile1.close_port()

    def init_plot(self):
        """This function graphs and displays the inital graph in the graph
        panel for BOTH version 1 and version 2. We are adding two subpanels,
        one for bias and one for current or whatever we wish."""
        # opening Figure class
        self.fig = Figure(figsize=(9, 9), dpi=45)
        # setting the axes fo the figure graph
        self.axes = self.fig.add_subplot(2, 1, 1)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Applied Potential', size=20)
        self.axes.grid(True, color='red', linewidth=2)

        pylab.setp(self.axes.get_xticklabels(), fontsize=14)
        pylab.setp(self.axes.get_yticklabels(), fontsize=14)

        # second subpanel graph settings for Version 2
        self.axes2 = self.fig.add_subplot(2, 1, 2)
        self.axes2.set_axis_bgcolor('black')
        self.axes2.set_title('Current', size=20)
        self.axes2.grid(True, color='cyan', linewidth=2)

        pylab.setp(self.axes2.get_xticklabels(), fontsize=14)
        pylab.setp(self.axes2.get_yticklabels(), fontsize=14)

        # This is the first plot graph
        self.plotData = self.axes.plot([0], linewidth=1,
                                       color=(1, 1, 0),)[0]
        # This is the second plot graph
        self.plotData2 = self.axes2.plot([0], linewidth=1,
                                         color='magenta',)[0]

        # This is the canvas display for the first notepad tab-v1
        self.canvas = FigCanvas(self.panel_1, -1, self.fig)
        # This is the second canvas display for the second notepad tab-v2
        self.canvas2 = FigCanvas(self.panel_graph_v2, -1, self.fig)

    def redraw_plot(self, event):
        """This function is recalled using the wxtimer loop and redraws the
        plot/graph for figure 1 giving us the real time graph display
        note that the axis do not self adjust however that is OK as the
        experiment length is only 30 mins at best max and won't time out
        The data is saved into textctrl widgets and the data is retrieved
        from the text ctrl widgets and displayed. This also allows the user
        to see the actual raw values coming from the experiment
        """
        # TODO: maybe make a running x axis display possibly

        # getting the local value
        eapp_val = str(self.text_ctrl_bias.GetValue())
        # stripping the endline character and obtaining the values for a list
        eapp_val2 = eapp_val.strip().split('\n')
        # converting the list into an array
        eapp_val3 = np.array(eapp_val2)
        # converting the entire array into a float in one shot for graphing
        bias_value_v1 = eapp_val3.astype(np.float)

        current_val = str(self.text_ctrl_current.GetValue())
        # converting ',' to 'E' for easy float movement
        current_val2 = current_val.replace(',', 'e')
        # strippping the endline character and removing the endline character
        current_val3 = (current_val2.strip().split('\n'))
        current_val4 = np.array(current_val3)
        current_value_v1 = current_val4.astype(np.float)

        # graphing the values for the first subpanel graph
        # to graph the last 100 data poitns use [-100] otherwise leave it alone
        self.plotData = self.axes.plot(bias_value_v1, linewidth=1,
                                       color=(1, 1, 0),)[0]
        # graphing the values for the second subpanel graph
        self.plotData2 = self.axes2.plot(current_value_v1, linewidth=1,
                                         color='magenta',)[0]

        self.canvas.draw()

    def on_redraw_timer(self, event):
        '''This function loops the OnStart event button until new parameters
        are not added when the pause button is clicked.'''
        self.On_Start(event)

    # Version 2 functions and features are below

    def On_sim_v2(self, event):  # wxGlade: MyFrame.<event_handler>
        """Function for version 2 sim toggle button updates and store
        the values."""
        # print "Event handler 'On_sim_v2' not implemented!"
        ans = self.button_sim_v2.GetValue()
        self.sim_value_v2 = ans
        event.Skip()

    def On_port_v2(self, event):  # wxGlade: MyFrame.<event_handler>
        """Version 2 port settings. Same thing as port settings for version 1.
        This function is to set the com port number.
        Note: This only sets the comport number, the user has to figure out
        how to find the comport value himself.
        """
        ans2 = self.spin_ctrl_port_v2.GetValue()
        # update the values
        self.port_value_v2 = "COM" + str(ans2)
        event.Skip()

    def On_start_v2(self, event):  # wxGlade: MyFrame.<event_handler>
        """This is the start button function for v2."""
        self.open_port_rev_v2(port=self.port_value_v2)
        self.run_rev_v2()
        self.myfile2.close_port()
        event.Skip()

    def On_Close_v2(self, event):  # wxGlade: MyFrame.<event_handler>
        """The close button for the v2 tab."""
        print 'Closing program, Thank you and have a good day'
        self.Destroy()
        event.Skip()

    def open_port_rev_v2(self, port=DEFAULTCOM, baudrate=19200, bytesize=8,
                         parity='N', stopbits=1, timeout=1, xonxoff=False,
                         rtscts=False, writeTimeout=3, dsrdtr=False,
                         interCharTimeout=None):
        '''This is opening a self.s port for Version 2.'''
        # doing an if loop to determine which type of library to import

        if self.sim_value_v2 is True:
            # import the fake serial class
            from Fake_Serial import Fake_Serial
            self.myfile2.s = Fake_Serial(port, baudrate, bytesize, parity,
                                         stopbits, timeout, xonxoff, rtscts,
                                         writeTimeout, dsrdtr,
                                         interCharTimeout)
        else:
            # import the real serial class
            from serial import Serial
            self.myfile2.s = Serial(port, baudrate, bytesize, parity, stopbits,
                                    timeout, xonxoff, rtscts, writeTimeout,
                                    dsrdtr, interCharTimeout)

    def run_rev_v2(self):
        """This is the memory samiwap run function """
        # opening excel file in write only mode. will rewrite on top of data
        # in existing file. change to "a" to instead append the data
        myfile = open(FILENAMEv2, "a")
        myfile.write("new data," + time.strftime("%d/%m/%Y") + NEWLINE)
        myfile.write("Time,BIAS,Measured Voltage,Current,CurrentExp,CHARGE(Q),\
Qexp" + NEWLINE)
        myfile.close()

        start_time = time.time()

        # get the command list from beastiecommand.csv and make the commands
        # into a dictionary. Sort them based on time.
        self.myfile2.parse_and_sort_commands(self.myfile2.readfiles())
        for times in self.myfile2.cmd_output[:]:
            while (time.time() - start_time) < times:
                self.myfile2.elapsed_time = time.time() - start_time
                self.myfile2.read_data()
                self.myfile2.record_data()

                # appending the self values into the text ctrl widget
                self.text_ctrl_bias_v2.AppendText(str(self.myfile2.
                                                      READE) + "\n")
                self.text_ctrl_current_v2.AppendText(str(self.myfile2.
                                                         READI) + "\n")
                # redrawing the plot
                self.redraw_plot_v2()

            if self.myfile2.command_dict[times] == "END":
                    break
            self.myfile2.elapsed_time = time.time() - start_time
            self.myfile2.command_execute(self.myfile2.command_dict[times])
            self.myfile2.read_data()
            self.myfile2.record_data()

            self.text_ctrl_bias_v2.AppendText(str(self.myfile2.
                                                  READE) + "\n")
            self.text_ctrl_current_v2.AppendText(str(self.myfile2.
                                                     READI) + "\n")
            self.redraw_plot_v2()

    def redraw_plot_v2(self):
        """Function which redraws the figure."""
        # getting the local value
        eapp_val = str(self.text_ctrl_bias_v2.GetValue())
        # stripping the endline character and obtaining the values for a list
        eapp_val2 = eapp_val.strip().split('\n')
        # converting the list into an array
        eapp_val3 = np.array(eapp_val2)
        # converting the entire array into a float in one shot for graphing
        self.bias_v2 = eapp_val3.astype(np.float)

        current_val = str(self.text_ctrl_current_v2.GetValue())
        # strippping the endline character and removing the endline character
        # converting ',' to 'E' for easy float movement
        current_val2 = current_val.replace(',', 'e')
        # strippping the endline character and removing the endline character
        current_val3 = (current_val2.strip().split('\n'))
        current_val4 = np.array(current_val3)
        current_value_v2 = current_val4.astype(np.float)

        # graphing the values for the first subpanel graph
        self.plotData = self.axes.plot(self.bias_v2, linewidth=1,
                                       color=(1, 1, 0),)[0]

        self.plotData2 = self.axes2.plot(current_value_v2, linewidth=1,
                                         color='magenta',)[0]
        # redraw the canvas
        self.canvas2.draw()

# end of class Version1Dialog


class MyApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

###############################################################################

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
