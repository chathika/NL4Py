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

from .NetLogoHeadlessWorkspace import NetLogoHeadlessWorkspace
from .NetLogoControllerServerStarter import NetLogoControllerServerStarter
from .NetLogoWorkspaceFactory import NetLogoWorkspaceFactory
from .NetLogoGUI import NetLogoGUI
from py4j.java_gateway import JavaGateway
import six.moves.urllib.request as urlrq
#import urllib
import shutil
import os
if not os.path.exists("./nl4pyServer/"):
    os.makedirs("./nl4pyServer/")

print("Downloading the NetLogo Controller Server jar file...")
url = 'https://github.com/chathika/NL4Py/raw/master/bin/NetLogoControllerServer.jar'
# Download the file from `url` and save it locally under `file_name`:
#Create a context that doesn't require a certificate for download (some mac instances complain without this)
import ssl
context = ssl._create_unverified_context()
try:
    response = urlrq.urlopen(url, context=context)
    out_file = open('./nl4pyServer/NetLogoControllerServer.jar', 'wb')
    shutil.copyfileobj(response, out_file)
    out_file.flush()
    out_file.close()
except:
    print("cannot download dependencies")
print("Downloading the Py4j jar file...")
url = 'https://github.com/chathika/NL4Py/raw/master/lib/py4j0.10.6.jar'
# Download the file from `url` and save it locally under `file_name`:
try:
    response = urlrq.urlopen(url, context=context)
    out_file = open('./nl4pyServer/py4j0.10.6.jar', 'wb')
    shutil.copyfileobj(response, out_file)
    out_file.flush()
    out_file.close()
except:
    print("cannot download dependencies")
    
print("Dependencies installed successfully! \nStart the NetLogoControllerServer using nl4py.startServer()")
serverStarter = NetLogoControllerServerStarter()
def startServer():
    try:
        serverStarter.startServer()
        print("Server started.")
    except:
        print("Server failed to start!")
def stopServer():
    try:
        serverStarter.shutdownServer()
        #print("Server stopped.")
    except:
        pass
#print("Starting up server...")
#NLCSStarter.startServer()
#print("Server started!")

netlogoWorkspaceFactory = NetLogoWorkspaceFactory()
'''Requests the NetLogoControllerServer to create a new HeadlessWorkspace and its controller and returns it'''
def newNetLogoHeadlessWorkspace():
    return netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
'''Returns a list of all live HeadlessWorkspaces'''
def getAllHeadlessWorkspaces():
    return netlogoWorkspaceFactory.getAllExistingWorkspaces()
'''Deletes all existing HeadlessWorkspaces'''
def deleteAllHeadlessWorkspaces():
    netlogoWorkspaceFactory.deleteAllExistingWorkspaces()
'''deletes the headlessworkspace given as an argument'''
def deleteHeadlessWorkspace(headlessWorkspace):
    netlogoWorkspaceFactory.deleteHeadlessWorkspace(headlessWorkspace)    
'''Opens the NetLogo Application'''
nApp = -1
def NetLogoApp():
    global nApp
    if nApp == -1:
        nApp = NetLogoGUI(JavaGateway())
    return nApp
