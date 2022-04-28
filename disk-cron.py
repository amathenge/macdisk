#!/usr/bin/env python3

import sqlite3
from datetime import datetime
import cred
import json
import http.client
import urllib.parse

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
msg += 'Mount Point: {}'.format(data['mountpoint'])

jsondata = {
    "SenderId": cred.SenderId,
    "Is_Unicode": False,
    "Is_Flash": False,
    "SchedTime": "",
    "GroupId": "",
    "ServiceId": "",
    "CoRelator": "",
    "LinkId": "",
    "MobileNumbers": cred.MobileNumbers,
    "Message": msg,
    "ApiKey": cred.ApiKey,
    "ClientId": cred.ClientId
}

jsondata = json.dumps(jsondata)

headers = {
    "content-type": "application/json",
    "cache-control": "no-cache"
}

conn = http.client.HTTPSConnection("api.uwaziimobile.com")
conn.request("POST", "/api/v2/SendSMS", body=jsondata, headers=headers)
res = conn.getresponse()
data = res.read()
conn.close()

