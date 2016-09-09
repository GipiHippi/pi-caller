#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

#import sh
import plivo
import time
import subprocess
import logging #logfile
import RPi.GPIO as GPIO
import datetime #Anrufszeit auslesen
import os.path


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Buttons
GPIO.setup(14,GPIO.IN) #8
GPIO.setup(18,GPIO.IN) #12
GPIO.setup(24,GPIO.IN) #18
GPIO.setup(8,GPIO.IN)  #24
GPIO.setup(1,GPIO.IN)  #28
GPIO.setup(16,GPIO.IN) #36

#LEDs
GPIO.setup(15,GPIO.OUT) #10
GPIO.setup(23,GPIO.OUT) #16
GPIO.setup(25,GPIO.OUT) #22
GPIO.setup(7,GPIO.OUT)  #26
GPIO.setup(12,GPIO.OUT) #32
GPIO.setup(20,GPIO.OUT) #38

#variablen deklaration
last_key_status1 = False
last_key_status2 = False
last_key_status3 = False
last_key_status4 = False
last_key_status5 = False
last_key_status6 = False

key_status1 = False
key_status2 = False
key_status3 = False
key_status4 = False
key_status5 = False
key_status6 = False

#LEDs ein aus
GPIO.output(15, True)
GPIO.output(23, True)
GPIO.output(25, True)
GPIO.output(7, True)
GPIO.output(12, True)
GPIO.output(20, True)
time.sleep(5)
GPIO.output(15, False)
GPIO.output(23, False)
GPIO.output(25, False)
GPIO.output(7, False)
GPIO.output(12, False)
GPIO.output(20, False)


day_of_year = time.localtime().tm_yday

LOG_FILENAME = 'log/LogFile_' + str(day_of_year)
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')

while True:
    GPIO.output(15, False)
    GPIO.output(23, False)
    GPIO.output(25, False)
    GPIO.output(7, False)
    GPIO.output(12, False)
    GPIO.output(20, False)
    time.sleep(0.005)
    key_status1 = GPIO.input(14)
    key_status2 = GPIO.input(18)
    key_status3 = GPIO.input(24)
    key_status4 = GPIO.input(8)
    key_status5 = GPIO.input(1)
    key_status6 = GPIO.input(16)

    if key_status1 and (key_status1 != last_key_status1):
        print("Button 1 Pressed")
        logging.debug('Button 1 Pressed')
        GPIO.output(15, True)
        subprocess.Popen("callscripts/save/script01.py") #subprocess.Popen("swfdump /tmp/filename.swf -d")
        last_key_status1 = key_status1
    if key_status2 and (key_status2 != last_key_status2):
        print("Button 2 Pressed")
        logging.debug('Button 2 Pressed')
        GPIO.output(23, True)
        subprocess.Popen("callscripts/save/script02.py")
        last_key_status2 = key_status2
    if key_status3 and (key_status3 != last_key_status3):
        print("Button 3 Pressed")
        logging.debug('Button 3 Pressed')
        GPIO.output(25, True)
        subprocess.Popen("callscripts/save/script03.py")
        last_key_status3 = key_status3
    if key_status4 and (key_status4 != last_key_status4):
        print("Button 4 Pressed")
        logging.debug('Button 4 Pressed')
        GPIO.output(7, True)
        subprocess.Popen("callscripts/save/script04.py")
        last_key_status4 = key_status4
    if key_status5 and (key_status5 != last_key_status5):
        print("Button 5 Pressed")
        logging.debug('Button 5 Pressed')
        GPIO.output(12, True)
        subprocess.Popen("callscripts/save/script01.py")
        last_key_status5 = key_status5
    if key_status6 and (key_status6 != last_key_status6):
        print("Button 6 Pressed")
        logging.debug('Button 6 Pressed')
        GPIO.output(20, True)
        subprocess.Popen("callscripts/save/script06.py")
        last_key_status6 = key_status6

    if key_status1 or key_status2 or key_status3 or key_status4:
        logging.debug('..button still pressed')
