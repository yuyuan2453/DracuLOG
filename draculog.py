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

vers=time.strftime("%Y%m%d")
parser = argparse.ArgumentParser(description='Welcome to Draculog v.' + vers + ' help menu. Draculog is a simple software data logger for Keithley 6487 picoammeter.')
parser.add_argument("-s", "--sleeptime", type=float ,action='store', nargs='?', const=1.0, default=1.0,metavar='[seconds]',
                    help="Sleeptime during one measure and another, in seconds.")
parser.add_argument("-p","--plot", action="store_true",    #will store false otherwise
                    help="Plot at acquisition's end.")
args = parser.parse_args()


def save__to__(arr,file):
    with open(file,'w') as f:
        for i in range(0,len(arr)):
            line=str(arr[i][0])+ ' ' +str(arr[i][1])
            f.write(line+'\n')
    
def plotter(arr):
    plt.figure('averagesignal',figsize=(10,10))
    plt.scatter(np.transpose(arr)[1],np.transpose(arr)[0]*10**9,s=1)
    plt.ylabel('Current [nA]')
    plt.xlabel('Time [s]')
    plt.title('draculog'+ timestr + alphaid + '.dat')
    plt.show()
    plt.close



COMPORT='COM4'

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

ser.write(b'*RST\r\n')
ser.write(b'FORMat:ELEMents READing, TIME\r\n')
ser.write(b'TRACe:TSTamp:FORMat ABS\r\n')
print('Keitley 6587 ready.')


input("Press Enter to START acquisition. Press Ctrl + C when you are done.")
ser.write(b'CONF:CURR\r\n')

i=0
arr=[]

timestr = time.strftime("-%Y%m%d_%H%M%S")
sleeptime=args.sleeptime
while True:
    try:
        ser.write(b'READ?\r\n')
        time.sleep(sleeptime)
        c=ser.readline().decode('utf-8').split(',')
        c=[float(read) for read in c]# read line and convert byte object to utf-8 encoded string
        if i==0:
            i+=1
            t0=c[1]
            c[1]=0.0
            print('%.3e , %.2f'%(c[0],round(c[1],2)))
        else:
            c[1]=c[1]-t0
            print('%.3e , %.2f'%(c[0],round(c[1],2)))
        arr.append(c)


    except KeyboardInterrupt:
        alphaid=random.choice(string.ascii_letters)
        print('All done, saving to ' + 'draculog'+ timestr + alphaid + '.dat.')
        print('Goodbye!')
        arr=np.array(arr)
        save__to__(arr,'draculog'+ timestr + alphaid + '.dat')
        if args.plot == True:
            plotter(arr)
        ser.write(b'ABORt\r\n')
        ser.close()
        sys.exit(0)
