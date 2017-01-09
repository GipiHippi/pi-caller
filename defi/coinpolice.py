#!/usr/bin/env python
# -*- coding: utf-8 -*-
#enable debugging

import plivo, plivoxml #um die plivo Api zu nutzen #sudo pip install plivo
import smtplib
import ConfigParser  #sudo apt-get install python-configparser
import io
import sys
import os
import socket


def parse_my_config():
    cfg = ConfigParser.ConfigParser()
    configpath = "/opt/lemt/defi/callerscripts/conf/numbers.conf"
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

if numbers is None:
    print "numbers are empty"
elif numbers == True:
    print "numbers access"

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

p = plivo.RestAPI(auth_id, auth_token)

#Guthaben Informationent
response = p.get_account()[1]
iCash = response["cash_credits"]
Cashs = "credits: "
sCash = Cashs + "   " + iCash

smtpUser = 'TheDoctor@lemt.ch'

toAdd = 'spg@lemt.ch'
fromAdd = smtpUser
host = socket.gethostname()

subject = 'ALERT from Defi'
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
body = 'Hey G' + '\n' + 'Guthabe betreagt ' + ('%s' % sCash) + '\n\n'+ 'From: ' + host


#troubleshooting
#print header + '\n' + body

s = smtplib.SMTP('mail0004',25)

#Formatieren
s.ehlo()
s.starttls()
s.ehlo()

#s.login(smtpUser, smtpPass)
s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

s.quit()
