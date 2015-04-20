#!/usr/bin/python

# http://flask.pocoo.org/docs/0.10/patterns/sqlite3/

from flask import Flask,g
import sqlite3

app = Flask("simpleServer")

DATABASE = 'db.db'
PASSWORD = 'a'

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
        db = g._database = sqlite3.connect(DATABASE)
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

# return all users
@app.route("/user")
def userList():
  userList = []
  for user in query_db("select * from user"):
    userList.append("%d:%s" % (user[0], user[1]))
  return ",".join(userList)

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
  if password == PASSWORD:
    id = insert("device", ['name','description'], [name,description])
    return str(id)
  else:
    return "-1"

@app.route("/update/<password>/add/access/<userid>/<deviceid>/<level>")
def addAccess(password,userid,deviceid,level):
  if password == PASSWORD:
    id = insert("userAccess", ['user','device','level'], [userid,deviceid,level])
    return str(id)
  else:
    return "-1"


if __name__ == "__main__":
  app.run(debug=True)
