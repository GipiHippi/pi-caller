#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

import datetime #Anrufszeit auslesen
import plivo, plivoxml #um die plivo Api zu nutzen
import json #damit phyton den jason text filtern kann
import logging #logfile
import RPi.GPIO as GPIO

#diese Script ist noch leer solage es keine 6en Alarm button im werk 1, 2 oder 3 gibt

#LED
GPIO.setup(12,GPIO.OUT) #32

#LED aus
GPIO.output(12, False)
