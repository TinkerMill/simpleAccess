import ConfigParser
import sys
import os
from threading import Thread
import wx
import wx.lib.newevent
import wx.html
import time
import requests
import serial

# http://sourceforge.net/p/pyserial/code/HEAD/tree/trunk/pyserial/examples/wxTerminal.py
# http://wxpython.org/Phoenix/docs/html/events_overview.html

c = ConfigParser.SafeConfigParser()
if os.path.isfile("run.cfg"):
  c.read('run.cfg')
  C_server = c.get('config', 'server')
  C_serial = c.get('config', 'serial')
else:
  print("config run.cfg not found")
  sys.exit(1)

s,serialrx = wx.lib.newevent.NewEvent()

class simpleFrame(wx.Frame):
  def __init__(self,parent,ID,title):
    wx.Frame.__init__(self, parent,ID,title)
    self.html = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
    self.Bind(  serialrx, self.serial)
    self.t = Thread(target=self.readSerial)
    self.t.start()

  def serial(self, evt):
    # evt.attr  is the data sent via the serial read, hopefully its the badge code
    # in this static example i'm just setting the badge code to abcde
    usercode = "abcde"

    # now i'm talking to the server to figure out if the badge code has access to this
    # device which i've hard coded as 0

    code = requests.get( url="%s/device/0/code/%s" % ( C_server, usercode) )

    # now i'm updating the html on the screen with the status
    self.html.SetPage("<center><h1>Level is: %s</h1></center>" % code.text)

  def readSerial(self):
    #
    # DUMMY CODE, put actual code to read serial port here, and when it gets stuff
    # send an event to check access in the serial function and update the gui
    #
    while True:
      evt = s(attr1="event data here")
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
