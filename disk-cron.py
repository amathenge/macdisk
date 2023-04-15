#!/usr/bin/env python3
'''
    should be run by cron at intervals (e.g., 2 times per day)
    example:
        0 8,18 * * * /home/andrew/src/python/macdisk/disk-cron.py
    
    This module will send an SMS to the recipients with the disk utilization
    on the server. Disk utilization is stored in a sqlite3 database (disk.db).
    The database is normally in the folder /home/andrew/src/python/disk
    The database has a table: disk (see disk.py for table structure)
'''

import sqlite3
from datetime import datetime
import cred
import json
import http.client
import urllib.parse
import cred
from sms import sendSMS

now = datetime.now()

db = sqlite3.connect('/home/andrew/src/python/disk/disk.db')
db.row_factory = sqlite3.Row
cur = db.cursor()
sql = "select * from disk where runid = (select max(runid) from disk) and filesystem like '%root%'"
cur.execute(sql)
data = cur.fetchone()

msg = 'Disk Utilization on Mac server:\n'
msg += 'Timestamp: {}\n'.format(data['runid'])
msg += 'Filesystem: {}\n'.format(data['filesystem'])
msg += 'Total Blocks: {}\n'.format(data['blocks'])
msg += 'Used Blocks: {}\n'.format(data['blocks_used'])
msg += 'Available Blocks: {}\n'.format(data['blocks_available'])
msg += 'Percentage used: {}\n'.format(data['used_percent'])
msg += 'Mount Point: {}'.format(data['mount_point'])

response = sendSMS(msg, cred.recipients)

# code below is the old Uwazii Mobile API
# --------------------------------------
#
#jsondata = {
#    "SenderId": cred.SenderId,
#    "Is_Unicode": False,
#    "Is_Flash": False,
#    "SchedTime": "",
#    "GroupId": "",
#    "ServiceId": "",
#    "CoRelator": "",
#    "LinkId": "",
#    "MobileNumbers": cred.MobileNumbers,
#    "Message": msg,
#    "ApiKey": cred.ApiKey,
#    "ClientId": cred.ClientId
#}
#
#jsondata = json.dumps(jsondata)
#
#headers = {
#    "content-type": "application/json",
#    "cache-control": "no-cache"
#}
#
#conn = http.client.HTTPSConnection("api.uwaziimobile.com")
#conn.request("POST", "/api/v2/SendSMS", body=jsondata, headers=headers)
#res = conn.getresponse()
#data = res.read()
#conn.close()
#
