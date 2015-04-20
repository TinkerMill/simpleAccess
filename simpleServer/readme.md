<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">Overview</a>
<ul>
<li><a href="#sec-1-1">Usage</a>
<ul>
<li><a href="#sec-1-1-1">device list</a></li>
<li><a href="#sec-1-1-2">device information</a></li>
<li><a href="#sec-1-1-3">device user list</a></li>
<li><a href="#sec-1-1-4">device user access</a></li>
<li><a href="#sec-1-1-5">user list</a></li>
<li><a href="#sec-1-1-6">user info</a></li>
<li><a href="#sec-1-1-7">user device list</a></li>
<li><a href="#sec-1-1-8">user device access</a></li>
</ul>
</li>
<li><a href="#sec-1-2">Updating the Database</a>
<ul>
<li><a href="#sec-1-2-1">add a user</a></li>
<li><a href="#sec-1-2-2">add a device</a></li>
<li><a href="#sec-1-2-3">add device access</a></li>
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

## Usage<a id="sec-1-1" name="sec-1-1"></a>

### device list<a id="sec-1-1-1" name="sec-1-1-1"></a>

This will return a list of all devices.  the format is a comma separated list of
device id : device name: **0:laser cutter,1:3d printer**

    curl http://localhost:5000/device

### device information<a id="sec-1-1-2" name="sec-1-1-2"></a>

this will return information on the device in a comma separated list: **1,3d printer,fancy 3d printer**

    curl http://localhost:5000/device/<deviceid>

### device user list<a id="sec-1-1-3" name="sec-1-1-3"></a>

this will return a list of all user IDs that have access to the device.  The format
of the results are userid:username in a comma separated list.

    curl http://localhost:5000/device/<deviceid>/user

### device user access<a id="sec-1-1-4" name="sec-1-1-4"></a>

this will return the access a userid has to a device.  The format is
just a single number of the access level.

    curl http://localhost:5000/device/<deviceid>/user/<userid>

### user list<a id="sec-1-1-5" name="sec-1-1-5"></a>

this will list out all the users.  The format is a comma separated list of
user id:user name: **0:matt,1:ron**

    curl http://localhost:5000/user

### user info<a id="sec-1-1-6" name="sec-1-1-6"></a>

this will return information on the user in a comma separated list: **0,matt**

    curl http://localhost:5000/user/<userid>

### user device list<a id="sec-1-1-7" name="sec-1-1-7"></a>

this will return a list of all the devices a user has access to.  The format is a
comma separated list of device id(s).

    curl http://localhost:5000/user/<userid>/device

### user device access<a id="sec-1-1-8" name="sec-1-1-8"></a>

this will return the access level a user has to a device.

    curl http://localhost:5000/user/<userid>/device/<deviceid>

## Updating the Database<a id="sec-1-2" name="sec-1-2"></a>

This will go away in the future, but for now, this is how you can easily add records.

### add a user<a id="sec-1-2-1" name="sec-1-2-1"></a>

    curl http://localhost:5000/update/a/add/user/<name>/<badgecode>

### add a device<a id="sec-1-2-2" name="sec-1-2-2"></a>

    curl http://localhost:5000/update/a/add/device/<name>/<description>

### add device access<a id="sec-1-2-3" name="sec-1-2-3"></a>

    curl http://localhost:5000/update/a/add/access/<userid>/<deviceid>/<levelofaccess>