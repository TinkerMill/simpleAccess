import serial
import sqlite3
import sys
import ConfigParser
import pdb
import os
import serial.tools.list_ports

c = ConfigParser.SafeConfigParser()
if os.path.isfile('c:/data/simpleAccess/simpleServer/run.cfg'):
  c.read('c:/data/simpleAccess/simpleServer/run.cfg')
  C_database    = c.get('config', 'database')
  #C_serial      = c.get('config', 'serial')
  C_serialspeed = c.get('config', 'serialspeed')
  C_debug       = c.getboolean('config','debug')
else:
  print("config run.cfg not found")
  sys.exit(1)

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if p[1][0:8] == "SparkFun":
      C_serial = p[0]


if not C_debug:
  ser = serial.Serial(C_serial, C_serialspeed)

db  = sqlite3.connect(C_database)
message = ""


if len(sys.argv) != 5:
  print("adduser.py <username> <device> <level 0=none 1=user 2=trainer> <trainerid>")
  sys.exit()

username = sys.argv[1]
device   = sys.argv[2]
level    = sys.argv[3]
trainer  = sys.argv[4]

if not C_debug:
  # so the first time we scan we get 1 thing of junk
  # the next scans we get 2 things of junk
  print("Scan Badge")
  message = ser.readline()[1:-2].strip()
  while len(message) != 12:
    print("Scan Badge")
    message = ser.readline()[2:-2].strip()
else:
  message = "04001D486839"

#pdb.set_trace()

# create the user if they don't already exist
with db:
  cur = db.cursor()

  # if the user already exists then update the record
  cur.execute("select * from user where code='%s'" % message)
  lid = cur.fetchall()
  if len(lid) == 0:
    cur.execute("insert into user (name, code) values ('%s', '%s');" % ( username, message) )
    lid = cur.lastrowid
  else:
    lid = lid[0][0]


  cur.execute("delete from userAccess where user=%s and device=%s" % (lid, device))
  cur.execute("insert into userAccess(user, device, level, trainer, datecreated, datemodified) values(%s,%s,%s,%s,datetime('now'),datetime('now'));" % (lid,device,level,trainer))



# pdb.set_trace()
