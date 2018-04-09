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

import py4j
from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
import subprocess
import threading
import os
import atexit
import sys


'''Responsible for communicating with the NetLogo controller, a Java executable'''
class NetLogo_HeadlessWorkspace:
    __bridge = None
    __gateway = None 
    __session = None
    __path = None

    def __init__(self):
        self.__gateway = JavaGateway()# New gateway connection
        self.__bridge = self.__gateway.entry_point
    
    #######################################################
    ###Below are public functions of the NL4Py interface###
    #######################################################
    
    '''Opens a NetLogo model and creates a headless workspace controller on the server'''
    '''Returns a session id for this controller to be used for further use of this ABM'''
    def openModel(self, path):
        #try:
        self.__path = path
        self.__session = self.__bridge.openModel(path)
        #except Py4JNetworkError, e:
            #raise NL4PyControllerServerException("Did you copy the NetLogoControllerServer.jar into your NetLogo/app folder? Or maybe the socket is busy? Trying running NL4Py.NLCSStarter.shutdownServer()"), None, sys.exc_info()[2]
    '''Sends a signal to the server to tell the respective controller to close its'''
    '''HeadlessWorkspace object'''
    def closeModel(self):
        self.__bridge.closeModel(self.__session)
    '''Sends a signal to the server to tell the respective controller to create a'''
    '''new instance of its HeadlessWorkspace object'''
    def refresh(self):
        self.__bridge.refresh(self.__session)
    '''Sends a signal to the server to tell the respective controller to export the view'''
    ''' of its HeadlessWorkspace object'''
    def exportView(self, filename):
        self.exportView(self.__session, filename)
    '''Sends a signal to the server to tell the respective controller to send a'''
    '''NetLogo command to its HeadlessWorkspace object'''
    def command(self, command):
        self.__bridge.command(self.__session,command)
    '''Sends a signal to the server to tell the respective controller to execute a'''
    '''reporter on its HeadlessWorkspace object'''
    def report(self, command):
        result = self.__bridge.report(self.__session, command)
        return result
    '''Sends a signal to the server to tell the respective controller to get the'''
    '''parameter specs of its HeadlessWorkspace object'''
    def getParamSpace(self):
        return self.__bridge.getParamList(self.__session,self.__path)
    #An extra helpful method:
    '''Sets the parameters randomly through the JavaGateway using'''
    '''Random parameter initialization code from BehaviorSearch'''
    def setParamsRandom(self):
        paramSpecs = self.__bridge.getParamList(self.__session, self.__path).getParamSpecs()
        
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            if py4j.java_gateway.is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleDiscreteSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if py4j.java_gateway.is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleContinuousSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if py4j.java_gateway.is_instance_of(self.__gateway,paramSpec,"bsearch.space.CategoricalSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
                if type(paramValue) != bool:#isinstance(data[i][k], bool)
                    paramValue = '"{}"'.format(paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast()))
            if py4j.java_gateway.is_instance_of(self.__gateway,paramSpec,"bsearch.space.ConstantSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            print("NetLogo command: set " + str(paramSpec.getParameterName()) + " " + str(paramValue))
            self.__bridge.command(self.__session, "set " + str(paramSpec.getParameterName()) + " " + str(paramValue))