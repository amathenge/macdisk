#!/usr/bin/env python3

import sqlite3
import os
from datetime import datetime

debug = False

now = datetime.now()
now = now.strftime('%Y-%m-%d %H:%M:%S')

def showdata(data):
  dict_data = {}
  dict_data['runid'] = data[0]
  dict_data['filesystem'] = data[1]
  dict_data['blocks'] = data[2]
  dict_data['blocks_used'] = data[3]
  dict_data['blocks_available'] = data[4]
  dict_data['used_percent'] = data[5]
  dict_data['mountpoint'] = data[6]
  print(dict_data)

db = sqlite3.connect('/home/andrew/src/python/disk/disk.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

data = os.popen('df -k').read()
data = data.split('\n')
del data[0]
inserted = False
for row in data:
  row = row.split()
  if len(row) == 6:
    filesystem = row[0]
    blocks = int(row[1])
    blocks_used = int(row[2])
    blocks_available = int(row[3])
    used_percent = row[4]
    mountpoint = row[5]

    if debug:
      showdata((now,filesystem,blocks,blocks_used,blocks_available,used_percent,mountpoint))

    sql = 'insert into disk (runid, filesystem, blocks, blocks_used, blocks_available, used_percent, mountpoint) values (?, ?, ?, ?, ?, ?, ?)'
    cur.execute(sql, (now, filesystem, blocks, blocks_used, blocks_available, used_percent, mountpoint))
    inserted = True

if inserted:
  db.commit()

'''
columns in disk.db (table = disk)
id, runid, filesystem, blocks, blocks_used, blocks_available, used_percent, mountpoint
'''
