import ConfigParser
import sys
import os
from threading import Thread
import wx
import wx.lib.newevent
import wx.html2
import datetime
import time
import requests
import serial
import serial.tools.list_ports

# http://sourceforge.net/p/pyserial/code/HEAD/tree/trunk/pyserial/examples/wxTerminal.py
# http://wxpython.org/Phoenix/docs/html/events_overview.html
# http://wiki.wxpython.org/Timer
# wxFormBuilder

levels = ['No Access', 'User', 'Trainer']
C_serial = False
C_code = False
C_log = False

c = ConfigParser.SafeConfigParser()
if os.path.isfile("run.cfg"):
  c.read('run.cfg')
  C_server = c.get('config', 'server')
  C_serial_speed  = c.get('config', 'serialspeed')
  C_timeout = 60 * c.getint('config','timeout')
  C_log = c.get('config', 'logfile')
else:
  print("config run.cfg not found")
  sys.exit(1)

# find the port that has the sparkfun device connected to it
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if p[1][0:8] == "SparkFun":
      C_serial = p[0]

if not C_serial:
  print("No valid usb serial device found")
  sys.exit()

s,serialrx = wx.lib.newevent.NewEvent()

def log(message):
  with open(C_log, 'a') as the_file:
    the_file.write(str(datetime.datetime.now()) + ":" + message + "\n")

class simpleFrame(wx.Frame):
  def __init__(self,parent,ID,title):
    wx.Frame.__init__(self, parent,ID,title, size=wx.Size(300,200) )
    self.ser = serial.Serial(C_serial, C_serial_speed)
    self.EnableCloseButton(False)
    self.timeleft = 0
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
    self.Bind(  serialrx, self.serial)
    self.t = Thread(target=self.readSerial)
    self.t.start()
    self.SetSizer(self.sizer)
    self.Layout()
    self.Centre( wx.BOTH )

    self.timer = wx.Timer(self, 100)
    wx.EVT_TIMER(self, 100, self.ontimer)


  def ontimer(self,evt):
    self.guitime.SetValue( self.timeleft )
    self.timeleft = self.timeleft - 1

    self.m_statusBar1.SetStatusText("User is: %s Time Left: %d minutes" % (self.userName , self.timeleft/60) )

    if self.timeleft < 0:
      self.logoutfunc(False)

  def logoutfunc(self,evt):
    self.timer.Stop()
    log("%s stopped using device" % self.userName)
    self.ser.write('user:-1')
    self.sizer.Clear(True)
    self.sizer.AddSpacer( ( 0, 30), 1, wx.EXPAND, 5 )
    self.sizer.Add( wx.StaticText( self, wx.ID_ANY, u"Scan Badge to login" ),wx.ALL|wx.ALIGN_CENTER,5)
    self.m_statusBar1.SetStatusText("Scan Badge to login")
    self.userName = False
    self.Layout()

  def serial(self, evt):
    global C_code
    usercode = evt.attr1
    # print("got %s" % usercode)
    print( "%s/device/0/code/%s" % ( C_server, usercode) )
    code = requests.get( url="%s/device/0/code/%s" % ( C_server, usercode) )
    code = int(code.text)
    C_code = code

    self.m_statusBar1.SetStatusText("Level is: %s" % levels[code])

    # if they have access to the machine
    if code > 0:
      self.userName = requests.get( url="%s/user/code/%s" % ( C_server, usercode) )
      self.userName = str(self.userName.text)
      self.ser.write('%s:1' % self.userName)
      log("%s started using device" % self.userName)


      self.timeleft = C_timeout
      self.sizer.Clear(True)
      self.logout = wx.Button(self, wx.ID_ANY, u"Logout", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
      self.timertext  = wx.StaticText( self, wx.ID_ANY, u"Time Left" )
      self.guitime = wx.Gauge( self, wx.ID_ANY, C_timeout , wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)

      self.sizer.AddSpacer( ( 0, 30), 1, wx.EXPAND, 5 )
      self.sizer.Add(self.timertext, wx.ALL|wx.ALIGN_CENTER,5)
      self.sizer.Add(self.guitime,  wx.ALL|wx.ALIGN_CENTER,5)
      self.sizer.AddSpacer( ( 0, 20), 1, wx.EXPAND, 5 )
      self.sizer.Add(self.logout, wx.ALL|wx.ALIGN_CENTER,5)
      self.sizer.AddSpacer( ( 0, 20), 1, wx.EXPAND, 5 )
      self.guitime.SetValue(self.timeleft)
      self.logout.Bind( wx.EVT_BUTTON, self.logoutfunc)
      self.Layout()
      self.timer.Start(1000)
    else:
      self.ser.write('user:-1')

  def readSerial(self):
    while True:
      message = self.ser.readline()[2:-4].strip()
      evt = s(attr1=message)
      wx.PostEvent(self,evt)
      time.sleep(5)
  def onClose(self,event):
    self.t.stop()

class simpleApp(wx.App):
  def OnInit(self):
    frame = simpleFrame(None, -1, 'Access')
    frame.Show(True)
    return True



app = simpleApp(0)
app.MainLoop()
