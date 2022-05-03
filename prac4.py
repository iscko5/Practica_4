import serial
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from drawnow import drawnow, figure

# Set path to my Arduino device
portPath = "/dev/tty.usbmodemfa411"
baud = 9600
sample_time = 0.1
sim_time = 10

# Initializing Lists
# Data Collection
data_log = []
line_data = []

# Establishing Serial Connection
connection = serial.Serial(portPath, baud)

# Calculating the length of data to collect based on the
# sample time and simulation time (set by user)
max_length = sim_time/sample_time

plt.ion()  # Tell matplotlib you want interactive mode to plot live data

# Create a function that makes our desired plot


def makeFig():
    plt.ylim(15, 35)
    plt.title('Temperatur Sensor Data')
    plt.grid(True)
    plt.ylabel('Temperatur C')
    plt.plot(data_log, 'ro-', label='Degrees C')


# Collecting the data from the serial port
while True:
    line = connection.readline()
    line_data = re.findall('\d*\.\d*', str(line))
    line_data = filter(None, line_data)
    line_data = [float(x) for x in line_data]
    if len(line_data) > 0:
        print(line_data[0])
        if float(line_data[0]) > 0.0:
            drawnow(makeFig)
            plt.pause(.000001)
            data_log.append(line_data)
    if len(data_log) > max_length - 1:
        break
