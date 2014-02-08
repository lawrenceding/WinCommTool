#!/usr/bin/python
# Filename : helloworld.py
# "python -m serial.tools.list_ports" can be used to list all avaliable ports
import sys, getopt  #import this to check the input from console as the parameters of this script
import serial
from Color import *
from datetime import datetime
import string   #convert from string to integer
import logging  

print 'CommTool V0.1'
print 'Ctrl+C to exit'

def main(argv):
    port = 1
    baud = 115200
    outputfile = 'RF6.log'
    try:
        opts, args = getopt.getopt(argv,"hp:o:b:",["port=","baudrate=","output="])
    except getopt.GetoptError:
        print 'python logging.py -p <uartport> -o <outputfile>'
        sys.exit(2)

    #parse the parameters input form console
    for opt, arg in opts:
        # print opt, args #debug only  
        if opt == '-h':
            print 'python logtool.py -p <uartport> -o <outputfile>'
            sys.exit()
        elif opt in ("-p", "--port"):
            port = string.atoi(arg)
            if port < 0:
                print 'Port number error'
                sys.exit()
        elif opt in ("-b", "--baudrate"):
            baud = string.atoi(arg)
            print 'baud', baud
        elif opt in ("-o", "--output"):
            outputfile = arg
        else:
            print 'Wrong pararmeters, try python logtool.py -h'



    logger = logging.getLogger('RF6')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(outputfile)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    console_color = Color()

    # 'application' code
    #logger.debug('debug message')
    #logger.info('info message')
    #logger.warn('warn message')
    #logger.error('error message')
    #logger.critical('critical message')

    try:
        ser = serial.Serial(port-1, baud, timeout=0)
        #print ser
    except:
        print 'Can\'t open uart', port
        sys.exit()

    toogle_color = False
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
                if not toogle_color:
                    toogle_color = True
                    console_color.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
                    logger.info(s)
                else:
                    toogle_color = False
                    console_color.reset_color()
                    logger.info(s)
                #console.print_green_text(start_time)
                #print s
    except:
        print 'Ctrl+C pressed'
    ser.close()
    console_color.reset_color()
    print 'Exit'

if __name__ == "__main__":
   main(sys.argv[1:])   #remove the first parameter, it is the python file itself
