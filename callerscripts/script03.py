#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

from datetime import datetime #Anrufszeit auslesen
import plivo, plivoxml #um die plivo Api zu nutzen
import json #damit phyton den jason text filtern kann
import logging #logfile
import logging.handlers
import ConfigParser
import io
import sys
import os


scriptpath = os.path.dirname(__file__)

def parse_my_config():
    cfg = ConfigParser.ConfigParser()
    configpath = scriptpath + "/conf/numbers.conf"
    cfg.read(configpath)

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



#initialize logging
# create console handler and set level to info
# Set up a specific logger with our desired output level
logger = logging.getLogger('defi_logger')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create rotating logfile handler
# Add the log message handler to the logger
LOG_FILENAME ="/var/log/defi/defilog"
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=200000, backupCount=5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

if numbers is None:
    logger.error("numbers are empty")
elif numbers == True:
    logger.info("numbers access")

try:
    auth_id = parse_my_config()[1]["auth_id"]
except ConfigParser.NoOptionError:
    logger.error("Es ist keine auth_id in numbers.conf vorhanden oder fehlerhaft.")
    sys.exit()
try:
    auth_token = parse_my_config()[1]["auth_token"]
except ConfigParser.NoOptionError:
    logger.error("Es ist keine auth_token in numbers.conf vorhanden oder fehlerhaft.")
    sys.exit()
try:
    from_number = parse_my_config()[1]["from_number"]
except ConfigParser.NoOptionError:
    logger.error("Es ist keine absender nummer in numbers.conf vorhanden oder fehlerhaft.")
try:
    log_dir = parse_my_config()[1]["log_dir"]
except ConfigParser.NoOptionError:
    logger.error("Es ist keine auth_id in numbers.conf vorhanden oder fehlerhaft.")
try:
    url = parse_my_config()[1]["url"]
except ConfigParser.NoOptionError:
    logger.error("Es ist keine url in numbers.conf vorhanden oder fehlerhaft.")
    sys.exit()

p = plivo.RestAPI(auth_id, auth_token)

#location
ort = "Werk1_EG_Werkstatt"
answer_url = url.format(ort) #url is a part of numbers.config

#Call
call_params = {
    'from': from_number,
    'answer_method' : "GET", # The method used to call the answer_url
}
call_params['answer_url'] = answer_url

#call
response = None
logger.debug("try call use the following params: %s",call_params)
for key, value in numbers.iteritems():
  call_params['to'] = value
  response = p.make_call(call_params)
  logger.debug('parameter used for call to {}: {}'.format(key, call_params))
  logger.debug('response from call to {}: {}'.format(key, response))

#Guthaben Informationent
response = p.get_account()[1]
iCash = response["cash_credits"]
Cashs = "credits: "
sCash = Cashs + "   " + iCash

#Debug
logger.info("Token: %s", auth_token)
logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ID: %s", auth_id)
logger.info("numbers: %s", numbers)
logger.info("settings: %s", settings)
logger.info("Call script for Button {}".format(ort))
logger.info('%s' % sCash)
logger.info('**************************************')
