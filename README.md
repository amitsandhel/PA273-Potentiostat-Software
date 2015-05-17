#PA273-Potentiostat Software
Version 1.0 by Amit Sandhel

This software is designed to operate the PA273 potentiostat. 
Two pdf manuals are provided. Read both manuals before operating the potentiostat. It is also recommended to run the software using the simulator setting to understand software functionality.

Currently the software has two versions

1. **pa273v1.py:** Version 1 runs the potentiostat manually. Version 1 is designed to run single voltage experiements for long periods of time  
2. **pa273v2.py:** Version 2 runs the potentionstat using a custom command language. Version 2 is designed for waveform programming Read the manuals provided for more information on waveform programming.

# Requirements
  1. Python (2.6, 2.7)
  2. Numpy
  3. Matplotlib
    

**The software comes with the following built in features: ** 
* Custom built command language to execute potentiostat commands (csv file)
* Built in simulator for testing, hardware and software development 
* Test folder with unittests (test folder)
* Displays real-time data
* Post data run analysis analyses and saves data  
* Argparse command line to run the software using various settings and parameters
* Logging files which log/record all command executions
* Example folder which contains sample data, log files amd data that will be generated. This data can be generated by the user when using the simulator parameter. 
* Manuals folder contains the potentiostat manuals needed to operate the potentiostat.  
                    
The following scripts exist in this software. 
**Note** All names should remain as is and no duplicates of names should exist to prevent unwanted error!

1. **Test folder:** Contains unittests for all scripts. These are run independently of the main software using the terminal/command prompt
2. **__init__.py:** Empty folder to build the subdirectory
3. **graphclass.py:** Script which outputs the data in real-time. **Note** This script lags in windows but is perfectly **OKAY** in Mac OS and Linux operating systems. 
4. **main.py:** Script which contains argparse and controls the execution of all scripts. Handles command execution
5. **pa273_v1.py:** Version 1 of potentiostat software. Version 1 is capable of running single volage measurements.
6. **pa273_v2.py:** Version 2 of potentiostat software. Version 2 is an enhanced software capable of waveform programming using a custom built command language. 
7. **postrun.py:** Generates data of experiment using matplotlib. Also saves the data as a png image file.
8. **beastiecommand.csv:** Command language for pa273_v2.py script. The command language reads the time and voltages from the beastie command. 
9. **BOOK2.csv:** csv file where the data is recorded for pa273_v2.py script. T
10. **BOOK3.csv:** csv file where the data is recorded for pa273_v1.py script.
11. **Examples:** Folder that contains sample log files and sample recorded data. This data can be generated via the simulator parameter or when running the real experiment. 
12. **manuals folder:** Folder containing the manuals to operate the potentiostat in pdf format. 

#Operating Instructions
* Read the pdf manuals provided on the potentiostat to fully understand all the commands available and how to operate the potentiostat.  
* Run the software with the simulator to have a full understanding of how the software works, the log files generated and the graph display.

## Available Argparse Commands
* The Potentiostat runs using Python's argparse commands so this software is run from a terminal/command prompt.
* A list of available argparse commands are given below.
* Open the command prompt/terminal to the folder directory of the software and type the following available commands:
1. **"main -h":** Opens the help file for the argparse commands. Lists all the argparse commands available with descriptions.
2. **"main -t":** Runs the various test folders. 
3. **"main -s":** Runs the simulator. Must be run with the potentiostat version you wish to run via the -v (version) command. If no version is present number is presented, default version is version 1. 
4. **"main -s -v1":** Runs version 1 on the simulator (py273_v1.py).
5. **"main -s -v2":** Runs version 1 on the simulator (py273_v2.py).
6. **"main -v1":** Runs version 1 on the real serial port (py273_v1.py).
7. **"main -v2":** Runs version 2 on the real serial port (py273_v2.py). 

## Operating Instructions
The following instructions are how to operate the software using both versions. Read the manuals to understand setting parameters required/needed.

##**Version 1 py273_v1.py**

**Running With Simulator:**

1. Commands to be passed in to set the parameters
2. Change COM Port setting. Open the pa273_v1.py script in a text editor software. Go to line 61 of code. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
3. Save the pa273_v1.py script **(DO NOT RENAME THIS FILE OVERRIDE AND SAVE IT)**.
4. In terminal/command prompt type **"main -s -v1"** To run the program using the simulator.
5. Enter in EGAIN value: options are 1, 5, 10 or 50 as stated in command prompt and in the pdf manual.
6. Note entering in incorrect value will crash the software. Therefore user has to reenter command 4 and restart the procedure. 
7. Enter in IGAIN value: options are 1, 5, 10 or 50 as stated in command prompt and in the pdf manual
8. Enter the potential to apply in millivolts (mV).
9. Software will run with incrementing cycle counter displayed. No data is displayed in real time. Data is saved in a csv file called BOOK3.csv.
10. if a new voltage is desired press **"A"**. Note the character "A" stands for **Again** must be Caps-lock or software will crash. Re-Enter steps 5-8. The command **"A"** can be entered as many times as needed to run as many single voltage measurements as desired. 
11. software will run potentiostat with new voltage and record data in BOOK3.csv file.
12. Press **"Q"** to exit the software.
**Note**BOOK3.csv records the time, BIAS [mV], the EGIAN, IGAIN, I-RANGE (set to auto manually on machine), voltage readout, and current charge and Qexp. 

**Running To Actual Serial Port-Without Simulator Setting:**

To run the software without the simulator setting (running to actual serial comport). Note that the only change is the argparse terminal command used. All other setting commands have to be used as is. 

1. Change COM Port setting. Open the pa273_v1.py script in a text editor software. Go to line 61 of code. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
3. Save the pa273_v1.py script **(DO NOT RENAME THIS FILE OVERRIDE AND SAVE IT)**.
4. In terminal/command prompt type **"main -v1"** To run the program.
5. Execute commands 5-12 as needed. 
   
##**Version 2 py273_v2.py**

**Running With Simulator:**

1.  Open **"beastiecommand.csv"** command file. This is a csv excel file.
2.  Write the desired times (in milliseconds) and the voltages (millivolts) needed for waveform programming 
3.  save the csv excel file and close it. Do not rename this file.  
4.  Change COM Port setting. Open the pa273_v1.py script in a text editor software. Go to line 61 of code. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
5. Save the pa273_v2.py script 
6. In terminal/command prompt type **"main -s -v2"** To run the program using the simulator.
7. Software will execute. Note that a graph in real time will be displayed. The data is stored in another csv file called "BOOK2.csv". That file is then opened by postrun.py script automatically to display the static data and saves the data as a png image as well.
**Note:**BOOK2.csv records the Time, AS, BIAS(voltage mV), TP-point (current)

**Running To Actual Serial Port-Without Simulator Setting:**

To run the software without the simulator setting (running to actual serial comport). Note that the only change is the argparse terminal command used. All other setting commands have to be used as is. Change the command file beastiecommand.csv as needed. 

1. Change COM Port setting. Open the pa273_v1.py script in a text editor software. Go to line 61 of code. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
3. Save the pa273_v2.py script.
4. In terminal/command prompt type **"main -v2"** To run the program.


#Notes of Caution:
* The simultaor accepts the BIAS command only. Adding in any other potentiostat commands will result in the simulator failing. However additional commands can be easily developed by the user by increasing functionality of the user. 
* The Simulator class is built within the pa273_v1.py and pa273_v2.py scripts individually. Class is called Fake_Serial(). 
* The command language file name beastiecommand.csv and the filename BOOK2.csv must not be changed. These filenames are opened by py273v2.py and postrun.py scripts respectively. 
* Many spike and concept tests have been commented out. User may wish to uncomment them for testing purposes 


#To Do/Future Features:
* Add threads and a callback feature
* Separate the serial simulator class into a separate individual script
* Add a comport setting to argparse-change the comport setting from argparse.
* Add axes labels to graphs
* Add ability to change filenames if necessary
* Improve test coverage
* improve Documentation
