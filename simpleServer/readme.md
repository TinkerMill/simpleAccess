<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">Overview</a>
<ul>
<li><a href="#sec-1-1">install</a></li>
<li><a href="#sec-1-2">User Access</a>
<ul>
<li><a href="#sec-1-2-1">starting the utility</a></li>
<li><a href="#sec-1-2-2">verify access</a></li>
</ul>
</li>
<li><a href="#sec-1-3">API Usage</a>
<ul>
<li><a href="#sec-1-3-1">device list</a></li>
<li><a href="#sec-1-3-2">device information</a></li>
<li><a href="#sec-1-3-3">device user list</a></li>
<li><a href="#sec-1-3-4">device user access</a></li>
<li><a href="#sec-1-3-5">device access via dongle code</a></li>
<li><a href="#sec-1-3-6">user list</a></li>
<li><a href="#sec-1-3-7">user info</a></li>
<li><a href="#sec-1-3-8">user device list</a></li>
<li><a href="#sec-1-3-9">user device access</a></li>
</ul>
</li>
<li><a href="#sec-1-4">Updating the Database</a>
<ul>
<li><a href="#sec-1-4-1">add a user</a></li>
<li><a href="#sec-1-4-2">add a device</a></li>
<li><a href="#sec-1-4-3">add device access</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>

# Overview<a id="sec-1" name="sec-1"></a>

The simple server is used to query for access on a device.  This is meant as a
very simple interface that easy easily accessible to many different device types
(arduino, pi..etc)  as such the return format is kept very simple so it is
easy for those devices to parse the output without a lot of extra libraries or cpu.

The rest syntax is built in a way to allow you to walk through the data.

## install<a id="sec-1-1" name="sec-1-1"></a>

Steps to install the software
-   for the server to run as a windows service, you'll need pywin32, which you can
    download from [here](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/)  I used the pywin32-219.win32-py2.7.exe  version
-   make sure flask is installed:  pip install flask
-   currently the configuration file location is hard coded in the the server.py
    program.  update the path to point to the run.cfg file.
-   update run.cfg and point the database to a place that exists.
-   if you change the password make sure you update the client to use that password.
-   If you make changes to the schema, there is a cleardb.bat script you can run
    from the directory that contains server.py.  This will DELETE the current database
    and recreate it with the schema.sql file.
-   the schema.sql file is the schema of the database.  Update this if you want to make
    any changes
-   When you are ready to run the software as a service, change to the directory that
    contains server.py  and run: python server.py install
-   once the service is installed you can also start and stop the service by running:
    python server.py start , or , python server.py stop

## User Access<a id="sec-1-2" name="sec-1-2"></a>

user access is done through the adduser.py script which is located within the server
directory.

    adduser.py <user's_full_name> <device_id> <level 0=none 1=user 2=trainer> <trainer's_id> <optional_badge_id>

The adduser script reads run.cfg to figure out the serial port and serial port speed
at which to scan for the badge code.  Once you run the adduser command with the
above options, it'll then ask you to scan the badge of the user you are entering
access for.

if you specify the optional_badge_id the serial port won't be used to scan the badge, and
it'll use that value as the badge code.

### starting the utility<a id="sec-1-2-1" name="sec-1-2-1"></a>

first make sure the client isn't running, since they can't share the serial
connection.
-   start->run: cmd
-   cd \\
-   cd data
-   cd simpleAccess
-   cd simpleServer
-   adduser.py "Jon Doe" 0 1 0

### verify access<a id="sec-1-2-2" name="sec-1-2-2"></a>

once you have users added, you can run the listuser.py script to list all the users
in the database, and what level of access they have.

## API Usage<a id="sec-1-3" name="sec-1-3"></a>

The simple server has no access (currently) beyond a rest based API.

### device list<a id="sec-1-3-1" name="sec-1-3-1"></a>

This will return a list of all devices.  the format is a comma separated list of
device id : device name: **0:laser cutter,1:3d printer**

    curl http://localhost:5000/device

### device information<a id="sec-1-3-2" name="sec-1-3-2"></a>

this will return information on the device in a comma separated list: **1,3d printer,fancy 3d printer**

    curl http://localhost:5000/device/<deviceid>

### device user list<a id="sec-1-3-3" name="sec-1-3-3"></a>

this will return a list of all user IDs that have access to the device.  The format
of the results are userid:username in a comma separated list.

    curl http://localhost:5000/device/<deviceid>/user

### device user access<a id="sec-1-3-4" name="sec-1-3-4"></a>

this will return the access a userid has to a device.  The format is
just a single number of the access level.

    curl http://localhost:5000/device/<deviceid>/user/<userid>

### device access via dongle code<a id="sec-1-3-5" name="sec-1-3-5"></a>

this is the important function, this will allow you to supply the device id
and the dongle code, and find out if that dongle has access to the device. The format
of the result is a number indicating the access level.

    curl http://localhost:5000/device/<deviceid>/code/<code>

### user list<a id="sec-1-3-6" name="sec-1-3-6"></a>

this will list out all the users.  The format is a comma separated list of
user id:user name: **0:matt,1:ron**

    curl http://localhost:5000/user

### user info<a id="sec-1-3-7" name="sec-1-3-7"></a>

this will return information on the user in a comma separated list: **0,matt**

    curl http://localhost:5000/user/<userid>

### user device list<a id="sec-1-3-8" name="sec-1-3-8"></a>

this will return a list of all the devices a user has access to.  The format is a
comma separated list of device id(s).

    curl http://localhost:5000/user/<userid>/device

### user device access<a id="sec-1-3-9" name="sec-1-3-9"></a>

this will return the access level a user has to a device.

    curl http://localhost:5000/user/<userid>/device/<deviceid>

## Updating the Database<a id="sec-1-4" name="sec-1-4"></a>

This will go away in the future, but for now, this is how you can easily add records.

### add a user<a id="sec-1-4-1" name="sec-1-4-1"></a>

    curl http://localhost:5000/update/a/add/user/<name>/<badgecode>

### add a device<a id="sec-1-4-2" name="sec-1-4-2"></a>

    curl http://localhost:5000/update/a/add/device/<name>/<description>

### add device access<a id="sec-1-4-3" name="sec-1-4-3"></a>

    curl http://localhost:5000/update/a/add/access/<userid>/<deviceid>/<levelofaccess>
