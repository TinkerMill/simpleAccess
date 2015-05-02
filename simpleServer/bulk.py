import serial
import sqlite3
import sys
import ConfigParser
import pdb
import os

db  = sqlite3.connect("db.db")

for row in open("d.csv"):
  r = row.split(',')
  username = r[0]
  message  = r[8]
  device   = 0 #laser
  trainer  = 0 # bulk load ron
  level    = 1 # default access

  if len(message) <= 10:
    continue

  print "adding", username, message
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
