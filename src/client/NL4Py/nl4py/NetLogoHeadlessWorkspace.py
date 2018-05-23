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

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
from py4j.protocol import Py4JJavaError

from .NL4PyControllerServerException import NL4PyControllerServerException
import py4j.java_gateway as jg
import py4j.java_collections as jcol
import subprocess
import threading
import os
import atexit
import sys
import time
import numpy as np
'''Internal class: Responsible for communicating with the NetLogo controller, a Java executable'''
class NetLogoHeadlessWorkspace:
    __bridge = None
    __gateway = None 
    __session = None
    __path = None
    __reporters_length = 0
    '''and creates a headless workspace controller on the server'''
    '''Returns a session id for this controller to be used for further use of this ABM'''
    def __init__(self, java_gateway):
        self.__gateway = java_gateway# New gateway connection
        self.__bridge = self.__gateway.entry_point
        self.__session = self.__bridge.newHeadlessWorkspaceController()
    #######################################################
    ###Below are public functions of the NL4Py interface###
    #######################################################
    
    '''Opens a NetLogo model'''
    def openModel(self, path):
        try:
            self.__path = path
            self.__bridge.openModel(self.__session,self.__path)
        except Py4JNetworkError as e:
            raise NL4PyControllerServerException("Looks like the server is unreachable! Maybe the socket is busy? Trying running nl4py.stopServer() and trying again.")#, None, sys.exc_info()[2])
        #except Py4JJavaError as e:
        #    raise NL4PyControllerServerException("Looks like the server couldn't find NetLogo. Perhaps you didn't set the NETLOGO_APP environment variable? Try setting it on your system and restarting Python.")#, None, sys.exc_info()[2])
        #Also, just in case, check if this model actually exists and responds
        #try: 
        #    self.getParamRanges()
        #except AttributeError as e:
        #    raise NL4PyControllerServerException("There doesn't seem to be a NetLogo model under that name! Please recheck the .nlogo model path.")
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
        self.__bridge.command(self.__session, command)
    '''Sends a signal to the server to tell the respective controller to execute a'''
    '''reporter on its HeadlessWorkspace object'''
    def report(self, command):
        result = self.__bridge.report(self.__session, command)
        return result
    '''Schedules a set of reporters at a start tick for an interval until a stop tick'''
    def scheduleReportersAndRun(self, reporters, startAtTick=0, intervalTicks=1, stopAtTick=-1, goCommand="go"):
        self.__reporters_length = len(reporters)
        reporterArray = self.__gateway.new_array(self.__gateway.jvm.java.lang.String,len(reporters))
        for idx, reporter in enumerate(reporters):
            reporterArray[idx] = reporter
        self.__bridge.scheduleReportersAndRun(self.__session,reporterArray,startAtTick,intervalTicks,stopAtTick,goCommand)
    '''Gets back results from scheduled reporters as a Java Array'''
    def getScheduledReporterResults (self):
        time.sleep(1)
        result = self.__bridge.getScheduledReporterResults(self.__session)
        if self.__reporters_length == 0:
            return result
        ticks_returned = len(result) / self.__reporters_length        
        result = np.reshape(np.ravel(list(result), order='F'),(int(self.__reporters_length),int(ticks_returned)),order='F').transpose()
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
            if jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleDiscreteSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleContinuousSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.CategoricalSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
                if type(paramValue) != bool:#isinstance(data[i][k], bool)
                    paramValue = '"{}"'.format(paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast()))
            if jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.ConstantSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            print("NetLogo command: set " + str(paramSpec.getParameterName()) + " " + str(paramValue))
            self.__bridge.command(self.__session, "set " + str(paramSpec.getParameterName()) + " " + str(paramValue))
            
    '''Returns the names of the parameters in the model'''
    def getParamNames(self):
        paramSpecs = self.__bridge.getParamList(self.__session, self.__path).getParamSpecs()
        
        parameterNames = []
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            parameterNames.append(paramSpec.getParameterName())
        return parameterNames
    
    '''Returns the parameter ranges'''
    def getParamRanges(self):
        paramSpecs = self.__bridge.getParamList(self.__session, self.__path).getParamSpecs()
        paramRanges = []
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            paramRange = []
            if (jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleDiscreteSpec") | jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleContinuousSpec")) :
                count = paramSpec.choiceCount()
                val_min = paramSpec.getValueFromChoice(0,count)
                val_max = paramSpec.getValueFromChoice(count - 1,count)
                step = (val_max - val_min)/(count - 1)
                paramRange = [val_min,step,val_max]
            if jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.CategoricalSpec"):
                count = paramSpec.choiceCount()
                paramRange = []
                for choice in range(0,count):
                    paramRange.append(paramSpec.getValueFromChoice(choice,count))
            if jg.is_instance_of(self.__gateway,paramSpec,"bsearch.space.ConstantSpec"):
                paramRange = [paramSpec.getValueFromChoice(0,1)]
            paramRanges.append(paramRange)
        return paramRanges
    
    '''Kills the Workspace and its controller on the server'''
    def deleteWorkspace(self):
        self.__bridge.removeControllerFromStore(self.__session)
        #self.__gateway.close()