#!/usr/bin/python

# http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
# http://ryrobes.com/python/running-python-scripts-as-a-windows-service/
# http://stackoverflow.com/questions/23550067/deploy-flask-app-as-windows-service

from flask import Flask,g,request
import sqlite3
import ConfigParser
import sys
import os

# http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
# pywin32-219.win32-py2.7.exe
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import servicemanager

app = Flask("simpleServer")

C_database=''
C_password=''

c = ConfigParser.SafeConfigParser()
if os.path.isfile("c:/data/simpleAccess/simpleServer/run.cfg"):
  c.read('c:/data/simpleAccess/simpleServer/run.cfg')
  C_database = c.get('config', 'database')
  C_password = c.get('config', 'password')
else:
  print("config run.cfg not found")
  sys.exit(1)


class aservice(win32serviceutil.ServiceFramework):

  _svc_name_ = "simpleServer"
  _svc_display_name_ = "simple access server"
  _svc_description_ = "Control access to devices"

  def __init__(self, args):
    win32serviceutil.ServiceFramework.__init__(self,args)
    self.hWaitStop = win32event.CreateEvent(None,0,0,None)

  def SvcStop(self):
    self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
    self.ReportServiceStatus(win32service.SERVICE_STOPPED)

  def SvcDoRun(self):
    import servicemanager
    servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, ''))
    self.main()

  def main(self):
    app.run(host='0.0.0.0')

def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(C_database)
    return db

def insert(table, fields=(), values=()):
  # g.db is the database connection
  cur = get_db().cursor()
  query = 'INSERT INTO %s (%s) VALUES (%s)' % (
    table,
    ', '.join(fields),
    ', '.join(['?'] * len(values))
  )
  cur.execute(query, values)
  get_db().commit()
  id = cur.lastrowid
  cur.close()
  return id

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# list all the devices
@app.route("/device")
def deviceList():
  devList = []
  cur = get_db().cursor()
  for device in query_db("select * from device"):
    devList.append( "%d:%s" % (device[0], device[1] ))

  return ",".join( devList)

# return information on one device
@app.route("/device/<id>")
def deviceInfo(id):
  info = query_db("select * from device where id='%s'" % id)[0]
  return "%d,%s,%s" % info

# return users that are registered to this device
@app.route("/device/<deviceid>/user")
def deviceUser(deviceid):
  users = []
  for user in query_db("select userAccess.user,user.name  from user join userAccess on user.id=userAccess.user where userAccess.device=%s" % deviceid):
    users.append( "%s:%s" % user )
  return ",".join(users)

# return the access level for a user on a device
@app.route("/device/<deviceid>/user/<userid>")
@app.route("/user/<userid>/device/<deviceid>")
def deviceAccess(deviceid,userid):
  access = query_db("select level from userAccess where device=%s and user=%s" % (deviceid,userid))
  if len(access) > 0:
    return  str(access[0][0])
  else:
    return "0"

@app.route("/device/<deviceid>/code/<code>")
def deviceCode(deviceid,code):
  access = query_db("select userAccess.level from userAccess join user on user.id=userAccess.user where user.code='%s' and userAccess.device=%s" % (code,deviceid))
  if len(access) > 0:
    return  str(access[0][0])
  else:
    return "0"

# return all users
@app.route("/user")
def userList():
  userList = []
  for user in query_db("select * from user"):
    userList.append("%d:%s" % (user[0], user[1]))
  return ",".join(userList)


@app.route("/user/code/<code>")
def userCodeInfo(code):
  info = query_db("select name from user where code='%s'" % code)
  return "%s" % info[0]

# return info on a userid
@app.route("/user/<userid>")
def userInfo(userid):
  info = query_db("select id,name from user where id=%s" % userid)[0]
  return "%d,%s" % info

# return a list of devices a userid has access to
@app.route("/user/<userid>/device")
def userDeviceList(userid):
  devices = []
  for device in query_db("select device from userAccess where user=%s" % userid):
    devices.append( str(device[0]))
  return ",".join(devices)

@app.route("/update/<password>/add/user/<name>/<code>")
def addUser(password,name,code):
  if password == PASSWORD:
    id = insert("user", ['name','code'], [name,code])
    return str(id)
  else:
    return "-1"

@app.route("/update/<password>/add/device/<name>/<description>")
def addDevice(password,name,code):
  if password == C_password:
    id = insert("device", ['name','description'], [name,description])
    return str(id)
  else:
    return "-1"

@app.route("/update/<password>/add/access/<userid>/<deviceid>/<level>")
def addAccess(password,userid,deviceid,level):
  if password == C_password:
    id = insert("userAccess", ['user','device','level'], [userid,deviceid,level])
    return str(id)
  else:
    return "-1"

#app.run(host='127.0.0.1', debug=True)
if __name__ == "__main__":
  win32serviceutil.HandleCommandLine(aservice)
