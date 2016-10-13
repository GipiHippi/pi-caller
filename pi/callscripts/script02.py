#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

from datetime import datetime #Anrufszeit auslesen
import plivo, plivoxml #um die plivo Api zu nutzen
import json #damit phyton den jason text filtern kann
import logging #logfile
#from ....Tokens.sec import auth_id, auth_token
import ConfigParser
import RPi.GPIO as GPIO
import io
import sys
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def parse_my_config():
    cfg = ConfigParser.ConfigParser()
    cfg.read(["numbers.conf","../numbers.conf","../../numbers.conf","../../../numbers.conf","/etc/numbers.conf"])
    numbers = {}
    for name in cfg.options("numbers"):
        numbers[name] = cfg.get("numbers",name)

    settings = {
                    "auth_id":cfg.get("settings","auth_id"),
                    "auth_token":cfg.get("settings","auth_token"),
                    "from_number":cfg.get("settings","from_number"),
                    "log_dir":cfg.get("settings","log_dir"),
                    "url":cfg.get("settings","url")
               }
    return [numbers,settings]


settings = parse_my_config()[1]
numbers = parse_my_config()[0]

if numbers is None:
    print "numbers are empty"
elif numbers == True:
    print "numbers access"


#LED
GPIO.setup(15,GPIO.OUT) #10

try:
    auth_id = parse_my_config()[1]["auth_id"]
except ConfigParser.NoOptionError:
    print "Es ist keine auth_id in numbers.conf vorhanden oder fehlerhaft."
    sys.exit()
try:
    auth_token = parse_my_config()[1]["auth_token"]
except ConfigParser.NoOptionError:
    print "Es ist keine auth_token in numbers.conf vorhanden oder fehlerhaft."
    sys.exit()
try:
    from_number = parse_my_config()[1]["from_number"]
except ConfigParser.NoOptionError:
    print "Es ist keine absender nummer in numbers.conf vorhanden oder fehlerhaft."
try:
    log_dir = parse_my_config()[1]["log_dir"]
except ConfigParser.NoOptionError:
    print "Es ist keine auth_id in numbers.conf vorhanden oder fehlerhaft."
try:
    url = parse_my_config()[1]["url"]
except ConfigParser.NoOptionError:
    print "Es ist keine url in numbers.conf vorhanden oder fehlerhaft."
    sys.exit()

#Create logFile
LOG_FILENAME = log_dir+"/"+os.environ["USER"]+"-"+datetime.now().strftime('callerlog_%Y_%m_%d.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')

p = plivo.RestAPI(auth_id, auth_token)

#location
ort = "Werk1_OG_Buero"
answer_url = url.format(ort) #url is a part of numbers.config

#Debug
logging.debug("Token: %s", auth_token)
logging.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ID: %s", auth_id)
logging.debug("numbers: %s", numbers)
logging.debug("settings: %s", settings)
logging.debug("Call script for Button {}".format(ort))

#LED on
GPIO.output(15, True)

#Call
call_params = {
    'from': from_number,
    'answer_method' : "GET", # The method used to call the answer_url
}
call_params['answer_url'] = answer_url

#call
response = None
logging.debug("try call use the following params: %s",call_params)
for key, value in numbers.iteritems():
  call_params['to'] = value
  response = p.make_call(call_params)
  logging.debug('parameter used for call to {}: {}'.format(key, call_params))
  logging.debug('response from call to {}: {}'.format(key, response))

#Guthaben Informationen
response = p.get_account()[1]
iCash = response["cash_credits"]
Cashs = "credits: "
sCash = Cashs + "   " + iCash

logging.debug('%s' % sCash)

logging.debug('**************************************')

#LED off
GPIO.output(15, False)
