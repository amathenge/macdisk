'''
    Show possible power outage data.

    cron job runs at 30 minutes (for filesystem usage). So, we can check the
    database and locate where difference > 30 minutes
'''
import os
from datetime import datetime
import sqlite3

database = '/home/andrew/src/python/disk/disk.db'
db = sqlite3.connect(database)
db.row_factory = sqlite3.Row
cur = db.cursor()

sql = 'select runid, max(id) from disk group by runid order by max(id) asc'
cur.execute(sql)
data = cur.fetchall()
prev = None
cur = None

def gettimediff(p, c):
    ptime = datetime.strptime(p['runid'], '%Y-%m-%d %H:%M:%S')
    ctime = datetime.strptime(c['runid'], '%Y-%m-%d %H:%M:%S')
    timediff = ctime - ptime
    return int(timediff.total_seconds() / 60)

for row in data:
    prev = cur
    cur = row
    if prev is not None:
        timediff = gettimediff(prev,cur)
        # only show where timediff > 30
        if timediff > 30:
            print(f'prev: {prev["runid"]} and cur: {cur["runid"]} = diff: {timediff}')

db.close()
