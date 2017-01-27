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
import datetime

def send_alert_mail(toAdd, text):
  smtpUser = 'TheDoctor@lemt.ch'
  host = socket.gethostname()
  subject = 'ALERT from Defi'
  header = 'To: ' + toAdd + '\n' + 'From: ' + smtpUser + '\n' + 'Subject: ' + subject
  intro = 'Alarm from Defi: ' + host + '\n\n'
  s = smtplib.SMTP('mail0004',25)
  s.ehlo()
  s.starttls()
  s.sendmail(smtpUser, toAdd, header + '\n\n' + intro +  '\n\n' + text)
  s.quit()
  return

def parse_my_config():
    cfg = ConfigParser.ConfigParser()
    configpath = "/opt/lemt/pi-caller/callerscripts/conf/numbers.conf"
    cfg.read(configpath)

    settings = {
                    "auth_id":cfg.get("settings","auth_id"),
                    "auth_token":cfg.get("settings","auth_token"),
                    "from_number":cfg.get("settings","from_number"),
                    "log_dir":cfg.get("settings","log_dir"),
                    "alert_mail_address":cfg.get("settings","alert_mail_address"),
                    "url":cfg.get("settings","url")
               }
    return settings
def check_plivo_account(auth_id, auth_token):
  p = plivo.RestAPI(auth_id, auth_token)
  #Guthaben Informationent
  response = p.get_account()[1]
  return float(response["cash_credits"])

def get_last_heatbeat():
  infile = r"/var/log/defi/defilog"
  found_lines = []
  search_string= "still alive.."

  with open(infile) as f:
    f = f.readlines()
  for line in f:
    if search_string in line:
      found_lines.append(line)
  last_heartbeat_str = found_lines[len(found_lines) -1][0:23] #format 2017-01-27 14:55:42,935
  return datetime.datetime.strptime(last_heartbeat_str, '%Y-%m-%d %H:%M:%S,%f')


settings = parse_my_config()
auth_id = settings["auth_id"]
auth_token = settings["auth_token"]
alert_mail_address = settings["alert_mail_address"]

account_balance = check_plivo_account(auth_id, auth_token)
last_heartbeat = get_last_heatbeat()
time_since_last_heartbeat = datetime.datetime.now() - last_heartbeat

day = datetime.timedelta(says=1)

if account_balance < 10:
  text =  "Guthaben im Plivo Account ist zu niedrig. Bitte umgehend aufladen\n\nAktueller Stand: %s)" % account_balance
  send_alert_mail(alert_mail_address, text)
if time_since_last_heartbeat > day:
  text = "Defialarm scheint auf diesem Gerät nicht mehr zu funktionieren. Bitte umgehend prüfen und logfiles kontrollieren!\n\n Letztes Lebenszeichen war am %s" % last_heartbeat
  send_alert_mail(alert_mail_address, text)


