#PA273-Potentiostat Software
**Version 4.2**

**by Amit Sandhel**
**with contributions by Fredrick Leber**

This software is designed to operate the PA273 potentiostat developed using Python with a built in simulator for software and hardware testing development. 

Two pdf manuals are provided. Read both manuals before operating the potentiostat. It is recommended to first run the software using the simulator setting to understand software functionality.

Currently the software has two versions:

1. **pa273_v1.py:** Version 1 runs the potentiostat manually. Version 1 is designed to run single voltage experiments for long periods of time  
2. **pa273_v2.py:** Version 2 runs the potentiostat using a custom command language. Version 2 is designed for waveform programming. Manuals provide more information regarding waveform programming.

# Requirements
  1. Python (2.6, 2.7)
  2. Matplotlib
  3. PySerial
  4. Numpy (for GUI)
    

**The software comes with the following built in features: ** 
* Custom built command language to execute potentiostat commands (csv file)
* Graphical User Interface
* Built in simulator for testing, hardware and software development 
* Test folder with unittests (test folder)
* Displays data in real-time
* Post data analysis. Saves data as a png image and as a csv file. Data analysis is done using Matplotlib library. 
* Argparse command line to run the software using various settings and parameters
* Logging files which log/record all command executions
* Example folder contains sample data, log files and data that will be generated. This data can be generated by the user when using the simulator parameter. 
* Manuals folder contains the potentiostat manuals needed to operate the potentiostat.  
                    
The following scripts exist in this software. 
**Note** All names should remain as is and no duplicates of names should exist to prevent unwanted error!

1. **Test folder:** Contains unittests for all scripts. Run independently of the main software using the terminal/command prompt.
2. **__init__.py:** Empty folder to build the subdirectory. See Python manual for more information.
3. **graphclass.py:** Script outputs data in real-time. **Note** This script lags in Windows but is perfectly **OKAY** in Mac OS and Linux operating systems. 
4. **main.py:** Script contains argparse and controls the execution of all scripts. Handles command execution.
5. **pa273_v1.py:** Version 1 of potentiostat software. Version 1 is capable of running single volage measurements.
6. **pa273_v2.py:** Version 2 of potentiostat software. Version 2 is an enhanced software capable of waveform programming using a custom built command language. 
7. **postrun.py:** Generates data of experiment using matplotlib. Also saves the data as a png image file.
8. **beastiecommand.csv:** Command language for pa273_v2.py script. The command language reads the time and voltages from the beastie command. 
9. **BOOK2.csv:** Csv file where the data is recorded for pa273_v2.py script. 
10. **BOOK3.csv:** Csv file where the data is recorded for pa273_v1.py script.
11. **Examples folder:** Folder contains sample log files and sample recorded data. This data will be generated using the simulator parameter or when running the real experiment. Records all command and serial executions. 
12. **Manuals folder:** Folder containing the manuals to operate the potentiostat in pdf format.
13. **Fake_Serial.py:** Simulates a serial port when running the simulator.
14. **wxmain.py:** The main script that controls the GUI
15. **wxgui.py:** Skeleton for the GUI, autogenerated
16. **wxgui.wxg:** Used to design the GUI

# Operating Instructions
* Read the manuals provided on the potentiostat to understand all available commands and how to operate the potentiostat.  
* Run the software with the simulator to have a full understanding of how the software works, the log files generated and the graph display.

## Available Argparse Commands
* The Potentiostat runs using Python's argparse commands so this software is run from a terminal/command prompt.
* A list of available argparse commands are given below. Open the command prompt/terminal to the folder directory of the software and type the following available commands:
1. **"main -h":** Opens the help file for the argparse commands. Lists all the argparse commands available with descriptions.
2. **"main -t":** Runs the various test folders. 
3. **"main -s":** Runs the simulator. Must be run with the potentiostat version you wish to run via the -v (version) command. If no version is present number is presented, default version is version 1. 
4. **"main -c1":** Changes the COM PORT. The number 1 shown in the example can be changed to any number as desired. If this isn't set, the program defaults to COM4.

**Simulator Setting**

4. **"main -s -v1":** Runs version 1 on the simulator (py273_v1.py).
5. **"main -s -v2":** Runs version 2 on the simulator (py273_v2.py).

**Real Serial COM PORT Setting**

6. **"main -v1":** Runs version 1 on the real serial comport (py273_v1.py).
7. **"main -v2":** Runs version 2 on the real serial comport (py273_v2.py). 


The following instructions are how to operate the software using both versions. Read the manuals to understand setting parameters required/needed.

## **Version 1 py273_v1.py**

**Running With Simulator:**

Note: Commands have to be set directly within the software. The comport setting in Windows can be determined in the **Devices and Printers** folder. A new comport driver should be identified and labelled in the folder. 

1. **Change COM Port setting.** Open the pa273_v1.py script in a text editor software. Go to line 61 of code. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
2. Save the pa273_v1.py script **(DO NOT RENAME THIS FILE OVERRIDE AND SAVE IT)**.
3. In terminal/command prompt type **"main -s -v1"** To run the program using the simulator.
4. Enter in **EGAIN** value: Options are 1, 5, 10 or 50 as stated in command prompt and in the pdf manual. Note entering in incorrect value will crash the software. Therefore user has to restart. 
5. Enter in **IGAIN** value: Options are 1, 5, 10 or 50 as stated in command prompt and in the pdf manual
6. Enter the Bias/Potential to apply in millivolts (mV).
7. Software will run with incrementing cycle counter displayed. Data is not displayed in real time. Data will be saved in a csv file called **BOOK3.csv**.
8. If a new voltage is desired, press **"A"**. The character "A" stands for **Again**. **"A"** must be Caps-lock or software will crash. Re-Enter steps 5-8. The command **"A"** can be entered repeatedly as required to run the single voltage measurements. 
9. Software will run potentiostat with new voltage and continue to record data in BOOK3.csv file.
10. Press **"Q"** to exit the software.

**BOOK3.csv** records the time, BIAS [mV], the EGIAN, IGAIN, I-RANGE (set to auto manually on machine), voltage readout, and current charge and Qexp. 

**Running To Actual Serial Port-Without Simulator Setting:**

To run the software without the simulator setting (running to actual serial comport). The only change is the argparse terminal/command prompt used. All other setting commands are the same. 

1. Change COM Port setting. Open the **pa273_v1.py** script in a text editor software. Go to line 61 of code again. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
3. Save the pa273_v1.py script **(DO NOT RENAME THIS FILE OVERRIDE AND SAVE IT)**.
4. In terminal/command prompt type **"main -v1"** To run the program.
5. Execute commands 4-10 as needed. 
   
## **Version 2 py273_v2.py**

**Running With Simulator:**

1.  Open **"beastiecommand.csv"** command file. This is a csv excel file.
2.  Write the desired times (in seconds) and the voltages (millivolts) needed for waveform programming 
3.  Save the csv excel file and close it. Do not rename this file.  
4.  Change COM Port setting. Open the **pa273_v2.py** script in a text editor software. Go to line 61 of the code. Section is named **COM PORT SETTINGS**. Change the comport settings to the number desired.
5. Save the **pa273_v2.py** script. Do not rename file.  
6. In terminal/command prompt type **"main -s -v2"** to run the program using the simulator.
7. Software will execute. A real time graph will be displayed showing the voltage and the current output. The voltage is displayed in the top graph and the current is displayed in the bottom graph. The data is stored in a csv file called **"BOOK2.csv"**. This file is then opened by postrun.py script automatically to display the static data and saves the data as a png image as well.

**BOOK2.csv** records the Time, AS, BIAS(voltage mV), TP-point (current)

**Running To Actual Serial Port-Without Simulator Setting:**

To run the software without the simulator setting (running to actual serial comport). The only change is the argparse terminal command used. All other setting commands have to be used as is. Change the command file beastiecommand.csv as needed. 

1. Change COM Port setting. Open the **pa273_v2.py** script in a text editor software. Go to line 61 of code. Section is named **COM PORT SETTINGS**. Change the comport setting to the number desired.
3. Save the pa273_v2.py script.
4. In terminal/command prompt type **"main -v2"** To run the program.


# Notes of Caution:
* The simulator accepts the BIAS command only. Adding in any other potentiostat commands will result in the simulator failing. However additional commands can be easily developed by the user by increasing functionality of the user. 
* The Simulator class is built within the pa273_v1.py and pa273_v2.py scripts individually. The Class is called Fake_Serial() in both py273_v1.py and py273_v2.py scripts. 
* The command language file name beastiecommand.csv and the filename BOOK2.csv must not be changed. These filenames are opened by py273v2.py and postrun.py scripts respectively. 
* Some unittests have been commented out. User may wish to uncomment them for testing purposes. They are commented out because they are design and concept tests.
* unittests are in a separate file and are run separately. To run the test files, open the terminal/command prompt in the **test** folder and type the name of the script. Examples included are 
**"C:\>test_graphclass.py"** and **"C:\>test_pa273_v2.py"**



# To Do/Future Features:
* **(WILL NOT BE DONE)** Add threads and a callback feature.
* **(WILL NOT BE DONE)** Run test files using command line and add unit tests.
* **(PROBABLY WILL NOT BE DONE)**Make the pa273_v1.py script compatible with postrun.py
* **(DONE)** Separate the serial simulator class into a separate individual script.
* **(DONE)** Add a comport setting to argparse-change the comport setting from argparse.
* **(DONE)** Add axes labels to graphs.
* **(DONE)** Improve Documentation.
* **(DONE)** Add auto-naming feature that names the log file (the current BOOK2) after the current date and time.
* **(DONE FOR BIAS, WILL NOT BE DONE FOR CURRENT)** Fix bug where graphclass graphs and postrun graphs do not match up
* **(DONE)** Fix bug when taking data from BeastieCommand.csv
* **(DONE)** Add GUI