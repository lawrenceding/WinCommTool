#!/usr/bin/python
# Filename : helloworld.py
import serial
from Color import *
from datetime import datetime
#from colorama import init, deinit
#from colorama import Fore, Back, Style
print 'CommTool V0.1'
print 'Ctrl+C to exit'
#init()
log = Color()
ser = serial.Serial(4, 115200, timeout=0)
try:
    while True:
        start_time = datetime.now()
        cur_time = start_time
        last_time = start_time
        s = ''
        while True:
            cur_time = datetime.now()
            num = ser.inWaiting()
            if num > 0:
                last_time = cur_time    
                s += ser.read(num)
            else:
                idle_time = cur_time - last_time
                if idle_time.microseconds > 10000:
                    break
        if s != '':
            #print "test"
            log.print_green_text(start_time)
            log.reset_color()
            print s
            #rint log
            #print(Fore.GREEN p+ 'Receive:'), start_time, (Fore.WHITE + s)
except:
    print 'Ctrl+C pressed'
ser.close()
#deinit()
print 'Exit'
