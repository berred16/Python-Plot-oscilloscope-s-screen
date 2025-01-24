# *******************************************************
# Little script to draw the waveform of an oscilloscpe's
# signal using matplotlib
# The oscillsocpe must have a USBTMC or LXI interface
# By Berred 2025
# *******************************************************

# Before importing you need to install modules in your
# virtual environment:
# pyvisa, pyvisa-py, numpy, matplotlib
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time

# instance for resource manager
rm = pyvisa.ResourceManager()
# Here you must insert your name / adress of your oscilloscope
# e.g. osci_1 = rm.open_resource('TCPIP::192.168.178.112::INSTR')
# e.g. osci_2 = rm.open_resource('TCPIP::192.168.178.112::5025::SOCKET')
hmo1024 = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')  

# Here. the oscilloscope must be set in the right way: Time/Div, Voltage/DIV and trigger
# The settings depend on your signal you want to plot
hmo1024.write('TIMEbase:SCALe 5ms')   
hmo1024.write('CHANnel1:STAte on')   
hmo1024.write('CHANnel1:POSItion 0') 
hmo1024.write('CHANnel1:SCALe 2')
#
# query data from oscilloscope
data = (hmo1024.query('CHANnel1:DATA?'))  

# modify the result of date. Removes the ","
m_points = np.array([float(i) for i in data.split(',')])

# aquire date, save it as float
samplerate = float(hmo1024.query('ACQuire:SRATe?'))

# Now a function from the NumPy library in Python that is used to
#generate an array of numbers that are evenly spaced over a specified range.
# np.linspace(start, stop, numbers)
time = np.linspace(0, len(m_points) / samplerate, len(m_points))

# Now plot the result using matplotlib
# X = time, Y = m_points
plt.plot(time, m_points)
plt.title("Oscilloscope's Signal")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.show()