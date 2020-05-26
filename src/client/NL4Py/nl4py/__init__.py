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

import shutil
import os

from py4j.java_gateway import JavaGateway

from .NetLogoHeadlessWorkspace import NetLogoHeadlessWorkspace
from .NetLogoControllerServerStarter import NetLogoControllerServerStarter
from .NetLogoWorkspaceFactory import NetLogoWorkspaceFactory
from .NetLogoGUI import NetLogoGUI

serverStarter = NetLogoControllerServerStarter()
netlogoWorkspaceFactory = NetLogoWorkspaceFactory()

def startServer(netlogo_home):
    try:
        serverStarter.startServer(netlogo_home)
    except:
        print("Server failed to start!")
    
def stopServer():
    try:
        serverStarter.shutdownServer()
        #print("Server stopped.")
    except:
        pass
    global netlogoWorkspaceFactory 
    del netlogoWorkspaceFactory
    

def newNetLogoHeadlessWorkspace():
    '''
    Requests the NetLogoControllerServer to create a new HeadlessWorkspace and its controller and returns it
    '''
    return netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()

def getAllHeadlessWorkspaces():
    '''
    Returns a list of all live HeadlessWorkspaces
    '''
    return netlogoWorkspaceFactory.getAllExistingWorkspaces()

def deleteAllHeadlessWorkspaces():
    '''
    Deletes all existing HeadlessWorkspaces
    '''
    netlogoWorkspaceFactory.deleteAllExistingWorkspaces()

def deleteHeadlessWorkspace(headlessWorkspace):
    '''
    Deletes the headlessworkspace given as an argument
    '''
    netlogoWorkspaceFactory.deleteHeadlessWorkspace(headlessWorkspace)    

def runExperiment(model_name, callback, data=None, reporters=[], start_at_tick=0,interval=1,stop_at_tick=10000000,go_command="go",num_procs=-1):
    '''
    Creates and returns a NetLogo experiment
    '''
    return netlogoWorkspaceFactory.runExperiment(model_name, callback, data, reporters, start_at_tick,interval,stop_at_tick,go_command,num_procs)

'''Opens the NetLogo Application'''
nApp = -1
def NetLogoApp():
    global nApp
    if nApp == -1:
        nApp = NetLogoGUI(JavaGateway())
    return nApp
