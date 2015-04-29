import serial
import sqlite3
import sys
import ConfigParser
import pdb
import os

c = ConfigParser.SafeConfigParser()
if os.path.isfile('c:/data/simpleAccess/simpleServer/run.cfg'):
  c.read('c:/data/simpleAccess/simpleServer/run.cfg')
  C_database    = c.get('config', 'database')
else:
  print("config run.cfg not found")
  sys.exit(1)

db  = sqlite3.connect(C_database)

with db:
  cur = db.cursor()
  cur.execute("select * from user" )
  rows = cur.fetchall()

  for row in rows:
      print( "\nid: %s\t\tname:%s\t\tbadge:%s" % row)
      cur.execute("select device.name,device.id,userAccess.level from userAccess join device on device.id=userAccess.device where userAccess.user=%s" % row[0])
      for row2 in cur.fetchall():
        print("\tname:%s deviceid:%s access:%s" % row2)
