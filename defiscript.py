#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

import plivo
import time
import subprocess
import logging #logfile
import logging.handlers
import RPi.GPIO as GPIO
import datetime #Anrufszeit auslesen
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define button and led channels
dict_buttons = {1:14, 2:18, 3:24, 4:6, 5:1, 6:16}
dict_leds = {1:15, 2:23, 3:25, 4:7, 5:12, 6:20}

#Buttons
GPIO.setup(dict_buttons[1],GPIO.IN) #8
GPIO.setup(dict_buttons[2],GPIO.IN) #12
GPIO.setup(dict_buttons[3],GPIO.IN) #18
GPIO.setup(dict_buttons[4],GPIO.IN)  #24
GPIO.setup(dict_buttons[5],GPIO.IN)  #28
GPIO.setup(dict_buttons[6],GPIO.IN) #36

#LEDs
GPIO.setup(dict_leds[1],GPIO.OUT) #10
GPIO.setup(dict_leds[2],GPIO.OUT) #16
GPIO.setup(dict_leds[3],GPIO.OUT) #22
GPIO.setup(dict_leds[4],GPIO.OUT)  #26
GPIO.setup(dict_leds[5],GPIO.OUT) #32
GPIO.setup(dict_leds[6],GPIO.OUT) #38

#LEDs ein aus
for key, value in dict_leds.items():
    GPIO.output(value, True)
time.sleep(5)
for key, value in dict_leds.items():
    GPIO.output(value, False)

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


def button_pressed(channel):
    #get button number from channel
	bt_nr = dict_buttons.keys()[dict_buttons.values().index(channel)]
	logger.info("Button " + bt_nr + " pressed.")
	GPIO.output(dict_leds[bt_nr], True)  //led on
	# wait 0.3 seconds and test input again to avoid false alarms
	time.sleep(.300)
	if GPIO.input(channel)
		try:
			callerscript = scriptpath + "/callerscripts/script0" +bt_nr + ".py"
			logger.info("calling %s", callerscript )
			subprocess.call(callerscript)
		except:
			logger.error('%s not found', callerscript)
	else
		logger.info("no callerscript called, button pressed not long enough!")
	GPIO.output(dict_leds[bt_nr], False)  //led off

def button_pressed(channel):
    #get button number from channel
	bt_nr = dict_buttons.keys()[dict_buttons.values().index(channel)]
	logger.info("Button " + bt_nr + " released (1:14, 2:18, 3:24, 4:8, 5:1 6:16)")


GPIO.add_event_detect(dict_buttons[1], GPIO.RISING, callback=button_pressed)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_buttons[2], GPIO.RISING, callback=button_pressed)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_buttons[3], GPIO.RISING, callback=button_pressed)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_buttons[4], GPIO.RISING, callback=button_pressed)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_buttons[5], GPIO.RISING, callback=button_pressed)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_buttons[6], GPIO.RISING, callback=button_pressed)  # add rising edge detection on a channel

GPIO.add_event_detect(dict_leds[1], GPIO.FALLING, callback=button_released)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_leds[2], GPIO.FALLING, callback=button_released)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_leds[3], GPIO.FALLING, callback=button_released)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_leds[4], GPIO.FALLING, callback=button_released)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_leds[5], GPIO.FALLING, callback=button_released)  # add rising edge detection on a channel
GPIO.add_event_detect(dict_leds[6], GPIO.FALLING, callback=button_released)  # add rising edge detection on a channel

try:
    print "DefiAlarm started.."
    while True:
		pass
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
