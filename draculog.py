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
import glob,os
import argparse
import random
import string
import numpy as np
import matplotlib.pyplot as plt

vers='20190111'
parser = argparse.ArgumentParser(description='Welcome to Draculog v.' + vers + ' help menu. Draculog is a simple software data logger for Keithley 6487 picoammeter.')
parser.add_argument("-slp", "--sleeptime", type=float ,action='store', nargs='?', const=1.0, default=1.0,metavar='[seconds]',
                    help="Sleeptime during one measure and another, in seconds.")
parser.add_argument("-rg", "--manualrange", type=float ,action='store', nargs='?', const=0.02, default=-1,metavar='[upper range]',
                    help="Manual range will be set to on. Available upper range values: 2e-2,2e-3,...,2e-9. If '--manualrange' is called without argument will be set to 20mA.")
parser.add_argument("-p","--plot", action="store_true",    #will store false otherwise
                    help="Plot when data acquisition end.")
parser.add_argument("--nosave", action="store_true",    #will store false otherwise
                    help=argparse.SUPPRESS)
args = parser.parse_args()


def save__to__(arr,file,append=False):
    if append==False:
        with open(file,'w') as f:
            for i in range(0,len(arr)):
                line=str(arr[i][0])+ ' ' +str(arr[i][1])
                f.write(line+'\n')
    else:
        with open(file,'a') as f:
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
if args.manualrange!=-1.0:
    range_flag=0.0
    for dex in range(2,10):
        if args.manualrange==2*10**(-dex):
            ser.write(bytes('CURR:RANG '+str(args.manualrange)+'\r\n', encoding= 'utf-8'))
            print('Upper range set to '+str(args.manualrange)+'A.. OK')
            range_flag=1.0
    if range_flag==0.0:
        print('''
 █     █░ ▄▄▄       ██▀███   ███▄    █  ██▓ ███▄    █   ▄████  ▐██▌ 
▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒ ██ ▀█   █ ▓██▒ ██ ▀█   █  ██▒ ▀█▒ ▐██▌ 
▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██▒▓██  ▀█ ██▒▒██░▄▄▄░ ▐██▌ 
░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██░▓██▒  ▐▌██▒░▓█  ██▓ ▓██▒ 
░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒▒██░   ▓██░░██░▒██░   ▓██░░▒▓███▀▒ ▒▄▄  
░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░▓  ░ ▒░   ▒ ▒  ░▒   ▒  ░▀▀▒ 
  ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░░ ░░   ░ ▒░ ▒ ░░ ░░   ░ ▒░  ░   ░  ░  ░ 
  ░   ░    ░   ▒     ░░   ░    ░   ░ ░  ▒ ░   ░   ░ ░ ░ ░   ░     ░ 
    ░          ░  ░   ░              ░  ░           ░       ░  ░   
  ''')
        print("Warning!: Forbidden upper range value. Autorange will be set on.")
else:
    print('Autorange..OK')
print('Keitley 6587 ready.')


i=1 #loop iteration
j=0 #backup number
BACKUPAFTER=100;
alphaid=random.choice(string.ascii_letters)

while True:
    try:
        ser.write(b'READ?\r\n')
        time.sleep(sleeptime)
        c=ser.readline().decode('utf-8').split(',')
        c=[float(read) for read in c]# read line and convert byte object to utf-8 encoded string
        print('%.3e , %.2f'%(c[0],round(c[1],2)))
        arr.append(c)
        if args.nosave == False and i%BACKUPAFTER==0:
            print('Backing-up to ' + 'draculog'+ timestr + alphaid + '_backup.dat...')
            arr_backup=np.array(arr)
            if j==0:
                save__to__(arr_backup,'draculog'+ timestr + alphaid + '_backup.dat')  
            else:
                save__to__(arr_backup[BACKUPAFTER*j:BACKUPAFTER*(j+1)],'draculog'+ timestr + alphaid + '_backup.dat',append=True) 
            j+=1
        i+=1

    except KeyboardInterrupt:
        if args.nosave == False:
            print('All done, saving to ' + 'draculog'+ timestr + alphaid + '.dat...')
            arr=np.array(arr)
            save__to__(arr,'draculog'+ timestr + alphaid + '.dat')
        if args.plot == True:
            plotter(arr)
        ser.write(b'ABORt\r\n')
        ser.close()
        print('Goodbye!')
        ## If backup file exists, delete it ##
        if os.path.isfile('draculog'+ timestr + alphaid + '_backup.dat'):
            os.remove('draculog'+ timestr + alphaid + '_backup.dat')
        else:
            print("Error: Backup file not found.")
        sys.exit(0)
