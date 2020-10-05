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
import traceback

from py4j.java_gateway import JavaGateway

from .NetLogoHeadlessWorkspace import NetLogoHeadlessWorkspace
from .NetLogoControllerServerStarter import NetLogoControllerServerStarter
from .NetLogoWorkspaceFactory import NetLogoWorkspaceFactory
from .NetLogoGUI import NetLogoGUI
from .NL4PyException import deprecated

SERVER_PORT = 25333

def initialize(netlogo_home):
    '''
    initializes nl4py, creating the NetLogoControllerServerStarter.
    
    :param netlogo_home: str path to netlog
    '''
    global server_starter
    server_starter = NetLogoControllerServerStarter(netlogo_home,SERVER_PORT)
    global netlogoWorkspaceFactory
    netlogoWorkspaceFactory = NetLogoWorkspaceFactory(SERVER_PORT)

def create_headless_workspace():
    '''
    Requests the NetLogoControllerServer to create a new HeadlessWorkspace and its controller and returns it
    '''
    return netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()

def get_all_headless_workspaces():
    '''
    Returns a list of all live HeadlessWorkspaces
    '''
    return netlogoWorkspaceFactory.getAllExistingWorkspaces()

def delete_all_headless_workspaces():
    '''
    Deletes all existing HeadlessWorkspaces
    '''
    netlogoWorkspaceFactory.deleteAllExistingWorkspaces()
    
def delete_headless_workspace(headlessWorkspace):
    '''
    Deletes the headlessworkspace given as an argument
    '''
    netlogoWorkspaceFactory.deleteHeadlessWorkspace(headlessWorkspace)

def run_experiment(model_name, setup_callback, setup_data=None, reporters=[], start_at_tick=0,interval=1,stop_at_tick=10000000,go_command="go",num_procs=-1):
    '''
    Runs and returns result of a NetLogo experiment
    '''
    return netlogoWorkspaceFactory.run_experiment(model_name, setup_callback, setup_data, reporters, start_at_tick,interval,stop_at_tick,go_command,num_procs)

def netlogo_app():
    '''
    Opens the NetLogo Application
    '''
    nApp = NetLogoGUI(server_starter)
    return nApp



@deprecated("Please use initialize(netlogo_home)")
def startServer(netlogo_home):
    initialize(netlogo_home)

@deprecated("Global shutdown not required anymore.")
def stopServer():
    pass

@deprecated('Alias left for backward compatibility. Use create_headless_workspace() since version 1.0.0.')
def newNetLogoHeadlessWorkspace():
    return create_headless_workspace()

@deprecated('Alias left for backward compatibility. Use get_all_headless_workspaces() since version 1.0.0.')
def getAllHeadlessWorkspaces():
    return get_all_headless_workspaces()
    
@deprecated('Alias left for backward compatibility. Use delete_headless_workspace() since version 1.0.0.')
def deleteHeadlessWorkspace(headlessWorkspace):
    delete_headless_workspace(headlessWorkspace)
    
@deprecated('Alias left for backward compatibility. Use delete_all_headless_workspaces() since version 1.0.0.')
def deleteAllHeadlessWorkspaces():
    deleteAllHeadlessWorkspaces()

@deprecated('Alias left for backward compatibility. Use netlogo_app() since version 1.0.0.')
def NetLogoApp():
    return netlogo_app()