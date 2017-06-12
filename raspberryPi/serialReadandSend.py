# Reads serial data and directly sends it to the host computer over netcat

import subprocess
import sys
import time
import serial
 
ser = serial.Serial(
  
   port='/dev/ttyACM0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)
counter=0

# generator function
def execute_byline(process):
    
    # Open a process
    ps = process

    for stdout_line in iter(ps.stdout.readline, ''):
        yield stdout_line

# start the process. IP adress of command computer
command = ('nc', '192.168.1.3', '59')
ps = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)


while 1:
    x = ser.readline()
    ps.stdin.write(x)
    
