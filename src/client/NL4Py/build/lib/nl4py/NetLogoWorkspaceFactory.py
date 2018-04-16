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

#!pip install py4j
#import NetLogo_Controller_Server_Starter
from .NetLogo_HeadlessWorkspace import NetLogo_HeadlessWorkspace
#import NL4PyControllerServerException
from py4j.java_gateway import JavaGateway

class NetLogoWorkspaceFactory:
    __all_workspaces = []
    __java_gateway = None
    def __init__ (self):
        self.__java_gateway = JavaGateway()
        return
    '''Create a new Headless Workspace and get a pointer to it'''
    def newNetLogoHeadlessWorkspace(self):
        n = NetLogo_HeadlessWorkspace(self.__java_gateway)
        self.__all_workspaces.append(n)
        return n

    '''Get a list of all existing Headless Workspaces on the server'''
    def getAllExistingWorkspaces(self):
        return self.__all_workspaces

    def deleteAllExistingWorkspaces(self):
        for __workspace in self.__all_workspaces:
            __workspace.deleteWorkspace()
        self.__all_workspaces = []
##############################################################################