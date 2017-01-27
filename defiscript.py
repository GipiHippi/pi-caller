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

heartbeat_sent = False
def heartbeat():
  global heartbeat_sent
  curr_hour =  datetime.datetime.now().hour
  if curr_hour == 4 and not heartbeat_sent:
    logger.info("still alive..")
    heartbeat_sent = True
  if curr_hour > 4:
    heartbeat_sent = False
  return


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define button and led channels
dict_buttons = {1:14, 2:18, 3:24, 4:8, 5:1, 6:16}
dict_leds = {1:15, 2:23, 3:25, 4:7, 5:12, 6:20}

#Buttons
GPIO.setup(dict_buttons[1],GPIO.IN)
GPIO.setup(dict_buttons[2],GPIO.IN)
GPIO.setup(dict_buttons[3],GPIO.IN)
GPIO.setup(dict_buttons[4],GPIO.IN)
GPIO.setup(dict_buttons[5],GPIO.IN)
GPIO.setup(dict_buttons[6],GPIO.IN)
#LEDs
GPIO.setup(dict_leds[1],GPIO.OUT)
GPIO.setup(dict_leds[2],GPIO.OUT)
GPIO.setup(dict_leds[3],GPIO.OUT)
GPIO.setup(dict_leds[4],GPIO.OUT)
GPIO.setup(dict_leds[5],GPIO.OUT)
GPIO.setup(dict_leds[6],GPIO.OUT)

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

#I/O test (LED ein aus)
logger.info("testing led's...")
for key, value in dict_buttons.items():
    logger.info("button %d is on bcm channel %d", key, value)
for key, value in dict_leds.items():
    logger.info("led %d is on bcm channel %d", key, value)
    GPIO.output(value, True)
time.sleep(5)
for key, value in dict_leds.items():
    GPIO.output(value, False)

#check forever...
while True:
    heartbeat()
    time.sleep(0.05)
    key_status1 = GPIO.input(dict_buttons[1])
    key_status2 = GPIO.input(dict_buttons[2])
    key_status3 = GPIO.input(dict_buttons[3])
    key_status4 = GPIO.input(dict_buttons[4])
    key_status5 = GPIO.input(dict_buttons[5])
    key_status6 = GPIO.input(dict_buttons[6])

    if key_status1 != last_key_status1:
        if key_status1:
	    logger.info("Button 1 pressed")
	    #wait some time and verify input to avoid false alarms
	    time.sleep(0.2)
	    key_status1 = GPIO.input(dict_buttons[1])
	    if not key_status1:
	        logger.info("False Alarm detected on Button 1, ignoring..")
		continue
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
            logger.info("Button 2 Pressed")
             #wait some time and verify input to avoid false alarms
            time.sleep(0.2)
            key_status1 = GPIO.input(dict_buttons[2])
            if not key_status1:
                logger.info("False Alarm detected on Button 2, ignoring..")
                continue
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
	    #wait some time and verify input to avoid false alarms
            time.sleep(0.2)
            key_status1 = GPIO.input(dict_buttons[3])
            if not key_status1:
                logger.info("False Alarm detected on Button 3, ignoring..")
                continue

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
	    #wait some time and verify input to avoid false alarms
            time.sleep(0.2)
            key_status1 = GPIO.input(dict_buttons[4])
            if not key_status1:
                logger.info("False Alarm detected on Button 4, ignoring..")
                continue
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
            #wait some time and verify input to avoid false alarms
            time.sleep(0.2)
            key_status1 = GPIO.input(dict_buttons[5])
            if not key_status1:
                logger.info("False Alarm detected on Button 5, ignoring..")
                continue
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
	    #wait some time and verify input to avoid false alarms
            time.sleep(0.2)
            key_status1 = GPIO.input(dict_buttons[6])
            if not key_status1:
                logger.info("False Alarm detected on Button 6, ignoring..")
                continue
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
