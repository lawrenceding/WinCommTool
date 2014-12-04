#!/usr/bin/python
# Filename : helloworld.py
# "python -m serial.tools.list_ports" can be used to list all avaliable ports
import sys, getopt  #import this to check the input from console as the parameters of this script
import serial
from Color import *
from datetime import datetime
import string   #convert from string to integer
import logging  
import time
import glob

def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def main(argv):
    port = 1
    baud = 115200
    outputfile = 'log.log'
    print 'CommTool V0.2'
    try:
        opts, args = getopt.getopt(argv,"hlp:o:b:",["help","list","port=","baudrate=","output="])
    except getopt.GetoptError:
        print 'Wrong arguments, try: python logtool.py -h'
        sys.exit(2)

    #parse the parameters input form console
    for opt, arg in opts:
        # print opt, args #debug only  
        if opt in ("-h", "--help"):
            print 'Usage: python logtool.py [OPTION]... [FILE]...'
            print 'python logtool.py -p <port> -b <baudrate> -o <logfile>'
            print 'If the <args> are not set, the default values are used:'
            print 'port = 1, baudrate = 115200, logfile = log.log'
            print 'Example: '
            print 'python logtool.py -p 2'
            print 'python logtool.py -p 1 -b 9600'
            print 'python logtool.py -p 1 -b 9600 -o mylog.log'
            print ''
            print 'Mandatory arguments to long options are mandatory for short options too.'
            print '-p, --port                       Uart port number'
            print '-b, --baudrate                   Baudrate for selected port'
            print '-o, --output                     Output file for storing the log'
            print '-h, --help                       Help doc'
            print '-l, --list                       List avaliable com ports'
            print ''
            print 'python -m serial.tools.list_ports    --show the avaliable uart ports'
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
        elif opt in ("-l", "--list"):
			print(serial_ports())
			sys.exit(2)
        else:
            print 'Wrong pararmeters, try: python logtool.py -h'

    print 'Ctrl+C to exit'

    logger = logging.getLogger('LOG')
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
                    time.sleep(0.001)
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
                # console_color.print_green_text(start_time)
                # print s
    except:
        print 'Ctrl+C pressed'
    ser.close()
    console_color.reset_color()
    print 'Exit'

if __name__ == "__main__":
	main(sys.argv[1:])   #remove the first parameter, it is the python file itself
