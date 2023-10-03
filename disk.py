'''
    NOTE: did not include the python shebang because we should use the venv python

    run "df -k" to check disk space on the server. Put the results of this into 
    a sqlite database [disk.db]

    disk.db [Table = disk]:
        runid = datetime primary key
        filesystem = varchar(32)
        block = integer
        blocks_used = integer
        blocks_available = integer
        used_percent = integer
        mount_point = varchar(16)

    To get a list of ID's (max) from the database for each runid, run:
        select runid, max(id) from disk group by runid order by id desc limit 10;
    that gives you to the last 10 runid's

    If you want to see how many they are, you can even do something like this:
        select count(*) from (select runid, max(id) from disk);
    this gives you the total number of times this program ran.

    NOTE: EACH TIME THE PROGRAM RUNS, IT CREATES 7 ROWS IN THE DISK TABLE

'''


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
    mount_point = row[5]

    if debug:
      showdata((now,filesystem,blocks,blocks_used,blocks_available,used_percent,mount_point))

    sql = 'insert into disk (runid, filesystem, blocks, blocks_used, blocks_available, used_percent, mount_point) values (?, ?, ?, ?, ?, ?, ?)'
    cur.execute(sql, (now, filesystem, blocks, blocks_used, blocks_available, used_percent, mount_point))
    inserted = True

if inserted:
  db.commit()
