#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

#import sh
import plivo
import time
import subprocess
import logging #logfile
import logging.handlers
import RPi.GPIO as GPIO
import datetime #Anrufszeit auslesen
import os


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

scriptpath = os.path.dirname(__file__)

#initialize logging
# create console handler and set level to info
# Set up a specific logger with our desired output level
logger = logging.getLogger('defi_logger')
logger.setLevel(logging.INFO)

#handler = logging.StreamHandler()
#handler.setLevel(logging.DEBUG)
#formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
#handler.setFormatter(formatter)
#logger.addHandler(handler)

# create rotating logfile handler
# Add the log message handler to the logger
LOG_FILENAME ="/var/log/defi/defilog"
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=200000, backupCount=5)
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info("defi alarm started")
logger.info("using log file : %s", LOG_FILENAME)

while True:
    time.sleep(0.05)
    key_status1 = GPIO.input(14)
    key_status2 = GPIO.input(18)
    key_status3 = GPIO.input(24)
    key_status4 = GPIO.input(8)
    key_status5 = GPIO.input(1)
    key_status6 = GPIO.input(16)

    if key_status1 != last_key_status1:
        if key_status1:
            logger.info("Button 1 Pressed")
            GPIO.output(15, True)
            try:
                callerscript = scriptpath + "/callerscripts/script01.py"
                logger.info("calling %s", callerscript )
                subprocess.call(callerscript)
            except:
                logger.error('%s not found', callerscript)
        else:
            GPIO.output(15, False)
            logger.debug("Button 1 released")
        last_key_status1 = key_status1

    if key_status2 != last_key_status2:
        if key_status2:
            logger.info("Button 1 Pressed")
            GPIO.output(23, True)
            try:
                callerscript = scriptpath + "/callerscripts/script02.py"
                logger.info("calling %s", callerscript )
                subprocess.call(callerscript)
            except:
                logger.error('%s not found', callerscript)
        else:
            GPIO.output(23, False)
            logger.debug("Button 2 released")
        last_key_status2 = key_status2

    if key_status3 != last_key_status3:
        if key_status3:
            logger.info("Button 3 Pressed")
            GPIO.output(25, True)
            try:
                callerscript = scriptpath + "/callerscripts/script03.py"
                logger.info("calling %s", callerscript )
                subprocess.call(callerscript)
            except:
                logger.error('%s not found', callerscript)
        else:
            GPIO.output(25, False)
            logger.debug("Button 3 released")
        last_key_status3 = key_status3

    if key_status4 != last_key_status4:
        if key_status4:
            logger.info("Button 4 Pressed")
            GPIO.output(7, True)
            try:
                callerscript = scriptpath + "/callerscripts/script04.py"
                logger.info("calling %s", callerscript )
                subprocess.call(callerscript)
            except:
                logger.error('%s not found', callerscript)
        else:
            GPIO.output(7, False)
            logger.debug("Button 4 released")
        last_key_status4 = key_status4

    if key_status5 != last_key_status5:
        if key_status5:
            logger.info("Button 5 Pressed")
            GPIO.output(12, True)
            try:
                callerscript = scriptpath + "/callerscripts/script05.py"
                logger.info("calling %s", callerscript )
                subprocess.call(callerscript)
            except:
                logger.error('%s not found', callerscript)
        else:
            GPIO.output(12, False)
            logger.debug("Button 5 released")
        last_key_status5 = key_status5

    if key_status6 != last_key_status6:
        if key_status6:
            logger.info("Button 6 Pressed")
            GPIO.output(20, True)
            try:
                callerscript = scriptpath + "/callerscripts/script06.py"
                logger.info("calling %s", callerscript )
                subprocess.call(callerscript)
            except:
                logger.error('%s not found', callerscript)
        else:
            GPIO.output(20, False)
            logger.debug("Button 6 released")
        last_key_status6 = key_status6
