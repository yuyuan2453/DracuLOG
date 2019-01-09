# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 17:03:40 2018

                     __.......__
                  .-:::::::::::::-.
                .:::''':::::::''':::.
              .:::'     `:::'     `:::. 
         .'\  ::'   ^^^  `:'  ^^^   '::  /`.
        :   \ ::   _.__       __._   :: /   ;
       :     \`: .' ___\     /___ `. :'/     ; 
      :       /\   (_|_)\   /(_|_)   /\       ;
      :      / .\   __.' ) ( `.__   /. \      ;
      :      \ (        {   }        ) /      ; 
       :      `-(     .  ^"^  .     )-'      ;
        `.       \  .'<`-._.-'>'.  /       .'
          `.      \    \;`.';/    /      .'
       jgs  `._    `-._       _.-'    _.'
             .'`-.__ .'`-._.-'`. __.-'`.
           .'       `.         .'       `.
         .'           `-.   .-'           `.

@author: peppe
"""

import time
import serial
import sys
import glob
import argparse
import random
import string
import numpy as np
import matplotlib.pyplot as plt

vers='20190109'
parser = argparse.ArgumentParser(description='Welcome to Draculog v.' + vers + ' help menu. Draculog is a simple software data logger for Keithley 6487 picoammeter.')
parser.add_argument("-slp", "--sleeptime", type=float ,action='store', nargs='?', const=1.0, default=1.0,metavar='[seconds]',
                    help="Sleeptime during one measure and another, in seconds.")
parser.add_argument("-p","--plot", action="store_true",    #will store false otherwise
                    help="Plot when data acquisition end.")
parser.add_argument("--nosave", action="store_true",    #will store false otherwise
                    help=argparse.SUPPRESS)
args = parser.parse_args()


def save__to__(arr,file):
    with open(file,'w') as f:
        for i in range(0,len(arr)):
            line=str(arr[i][0])+ ' ' +str(arr[i][1])
            f.write(line+'\n')
    
def plotter(arr):
    plt.figure('currentmeasure',figsize=(10,10))
    plt.scatter(np.transpose(arr)[1],np.transpose(arr)[0]*10**9,s=1)
    plt.ylabel('Current [nA]')
    plt.xlabel('Time [s]')
    plt.title('draculog'+ timestr + alphaid + '.dat')
    plt.show()
    plt.close



COMPORT='COM5'

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port=COMPORT,
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

print(''' 
Welcome to
                                                                                        
      ##### ##                                              ###                          
   /#####  /##                                               ###                         
 //    /  / ###                                               ##                         
/     /  /   ###                                              ##                         
     /  /     ###                                             ##                         
    ## ##      ## ###  /###     /###     /###   ##   ####     ##      /###     /###      
    ## ##      ##  ###/ #### / / ###  / / ###  / ##    ###  / ##     / ###  / /  ###  /  
    ## ##      ##   ##   ###/ /   ###/ /   ###/  ##     ###/  ##    /   ###/ /    ###/   
    ## ##      ##   ##       ##    ## ##         ##      ##   ##   ##    ## ##     ##    
    ## ##      ##   ##       ##    ## ##         ##      ##   ##   ##    ## ##     ##    
    #  ##      ##   ##       ##    ## ##         ##      ##   ##   ##    ## ##     ##    
       /       /    ##       ##    ## ##         ##      ##   ##   ##    ## ##     ##    
  /###/       /     ##       ##    /# ###     /  ##      /#   ##   ##    ## ##     ##    
 /   ########/      ###       ####/ ## ######/    ######/ ##  ### / ######   ########    
/       ####         ###       ###   ## #####      #####   ##  ##/   ####      ### ###   
#                                                                                   ###  
 ##                                                                           ####   ### 
                                                                            /######  /#  
                                                                            /     ###/   
                                                                            v.''' + vers + '''           
 
                               A Keithley 6487 SCPI controller and data logger.
                                
                                
 ''')


if ser.isOpen() == True:
    print('Welcome. Connection with port ' + COMPORT + ' established.')


input("Press Enter to START. Press Ctrl + C when you are done.")

i=0
arr=[]
ser.write(b'*RST\r\n')
timestr = time.strftime("-%Y%m%d_%H%M%S")
sleeptime=args.sleeptime
print('Reset..OK')
ser.write(b'FORMat:ELEMents READing, TIME\r\n')
ser.write(b'SYSTem:TIME:RESet\r\n')
ser.write(b'TRACe:TSTamp:FORMat:ABS\r\n')
print('Data formatting..OK')
ser.write(b'CONF:CURR\r\n')
print('Arm and trig conf, zero check..OK')
print('Keitley 6587 ready.')


while True:
    try:
        ser.write(b'READ?\r\n')
        time.sleep(sleeptime)
        c=ser.readline().decode('utf-8').split(',')
        c=[float(read) for read in c]# read line and convert byte object to utf-8 encoded string
        print('%.3e , %.2f'%(c[0],round(c[1],2)))
        arr.append(c)

    except KeyboardInterrupt:
        alphaid=random.choice(string.ascii_letters)
        if args.nosave == False:
            print('All done, saving to ' + 'draculog'+ timestr + alphaid + '.dat...')
            arr=np.array(arr)
            save__to__(arr,'draculog'+ timestr + alphaid + '.dat')
        if args.plot == True:
            plotter(arr)
        ser.write(b'ABORt\r\n')
        ser.close()
        print('Goodbye!')
        sys.exit(0)

