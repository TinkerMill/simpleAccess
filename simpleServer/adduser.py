import serial
import sqlite3
import sys

ser = serial.Serial("com13", "19200")
db  = sqlite3.connect("db.db")
message = ""


if len(sys.argv) != 4:
	print("adduser.py <username> <level 0=none 1=user 2=trainer> <trainerid>")
	sys.exit()

username = sys.argv[1]
level = sys.argv[2]
trainer = sys.argv[3]

# so the first time we scan we get 1 thing of junk
# the next scans we get 2 things of junk
print("Scan Badge")
message = ser.readline()[1:-2].strip()
while len(message) != 12:
  print("Scan Badge")
  message = ser.readline()[2:-2].strip()

with db:
	cur = db.cursor()
	cur.execute("select * from user where code='%s'" % message)
	
	rows = cur.fetchall()
	
	# if the user already exists then update the record
	if len(rows) > 0:
		for row in rows:
			print row[0]
			cur.execute("update userAccess set level=%s where user=%s" % (level, row[0]) )
	else:
		cur.execute("insert into user (name, code) values ('%s', '%s');" % ( username, message) )
		lid = cur.lastrowid
		cur.execute("insert into userAccess(user, device, level, trainer, datecreated, datemodified) values(%s,0,%s,%s,datetime('now'),datetime('now'));" % (lid,level,trainer))