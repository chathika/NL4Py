'''NL4Py, A NetLogo controller for Python
Copyright (C) 2018  Chathika Gunaratne

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from .NetLogo_HeadlessWorkspace import NetLogo_HeadlessWorkspace
from .NetLogo_Controller_Server_Starter import NetLogo_Controller_Server_Starter
from .NetLogoWorkspaceFactory import NetLogoWorkspaceFactory

import six.moves.urllib.request as urlrq
#import urllib
import shutil
import os
if not os.path.exists("./server/"):
    os.makedirs("./server/")

print("Downloading the NetLogo Controller Server jar file...")
url = 'https://github.com/chathika/NL4Py/raw/master/bin/NetLogoControllerServer.jar'
# Download the file from `url` and save it locally under `file_name`:
try:
    response = urlrq.urlopen(url)
    out_file = open('./server/NetLogoControllerServer.jar', 'wb')
    shutil.copyfileobj(response, out_file)
    out_file.flush()
    out_file.close()
except:
    print("cannot download dependencies")
print("Downloading the Py4j jar file...")
url = 'https://github.com/chathika/NL4Py/raw/master/lib/py4j0.10.6.jar'
# Download the file from `url` and save it locally under `file_name`:
try:
    response = urlrq.urlopen(url)
    out_file = open('./server/py4j0.10.6.jar', 'wb')
    shutil.copyfileobj(response, out_file)
    out_file.flush()
    out_file.close()
except:
    print("cannot download dependencies")
    
print("Dependencies installed successfully!")
NLCSStarter = NetLogo_Controller_Server_Starter()
print("Starting up server...")
NLCSStarter.startServer()
print("Server started!")

netlogoWorkspaceFactory = NetLogoWorkspaceFactory()