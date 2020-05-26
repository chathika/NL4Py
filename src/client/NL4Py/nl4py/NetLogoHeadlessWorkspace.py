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

import os

from py4j.protocol import Py4JNetworkError
from py4j.java_gateway import JavaGateway, GatewayParameters, is_instance_of

from .NL4PyControllerServerException import NL4PyControllerServerException

class NetLogoHeadlessWorkspace:
    '''Internal class: Responsible for communicating with the NetLogo controller, a Java executable'''
    
    def __init__(self):
        '''
        Returns a session id for this controller to be used for further use of this ABM
        and creates a headless workspace controller on the server
        '''
        self.__gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
        self.__bridge = self.__gateway.entry_point
        self.__session = self.__bridge.newHeadlessWorkspaceController()
    
    #######################################################
    ###Below are public API functions of the NL4Py interface###
    #######################################################
    
    
    def openModel(self, path):
        '''
        Opens a NetLogo model
        '''
        try:
            self.__path = path
            self.__bridge.openModel(self.__session,self.__path)
        except Py4JNetworkError as e:
            raise NL4PyControllerServerException("Looks like the server is unreachable! Maybe the socket is busy? Trying running nl4py.stopServer() and trying again.")
        
    
    def closeModel(self):
        '''
        Sends a signal to the server to tell the respective controller to close its
        HeadlessWorkspace object
        '''
        self.__bridge.closeModel(self.__session)
    
    def refresh(self):
        '''
        Sends a signal to the server to tell the respective controller to create a
        new instance of its HeadlessWorkspace object
        '''
        self.__bridge.refresh(self.__session)
    
    def exportView(self, filename):
        '''
        Sends a signal to the server to tell the respective controller to export the view
        of its HeadlessWorkspace object
        '''
        self.__bridge.exportView(self.__session, filename)
    
    def command(self, command):
        '''
        Sends a signal to the server to tell the respective controller to send a
        NetLogo command to its HeadlessWorkspace object
        '''
        self.__bridge.command(self.__session, command)
    
    def report(self, reporter):
        '''
        Sends a signal to the server to tell the respective controller to execute a
        reporter on its HeadlessWorkspace object
        '''
        result = self.__bridge.report(self.__session, reporter)
        return result
    
    def scheduleReportersAndRun(self, reporters, startAtTick=0, intervalTicks=1, stopAtTick=-1, goCommand="go"):
        '''
        Schedules a set of reporters at a start tick for an interval until a stop tick
        '''
        self.__reporters_length = len(reporters)
        reporterArray = []#self.__gateway.new_array(self.__gateway.jvm.java.lang.String,len(reporters))
        for idx, reporter in enumerate(reporters):
            reporterArray.append(str(reporter))
            #reporterArray[idx] = reporter
        self.__bridge.scheduleReportersAndRun(self.__session, reporterArray,startAtTick,intervalTicks,stopAtTick,goCommand)
    
    def awaitScheduledReporterResults(self):
        '''
        Waits for completion of scheduled reporters and returns result as Python list.
        '''
        bytes_result =  self.__bridge.awaitScheduledReporterResults(self.__session)
        decoded_results = []
        for bytes_results_in_tick in bytes_result:
            decoded_results_in_tick = []
            for bytes_result_in_tick in bytes_results_in_tick:
                decoded_results_in_tick.append(NetLogoHeadlessWorkspace.decodeServerResult(bytes_result_in_tick))
            decoded_results.append(decoded_results_in_tick)
        return decoded_results
    
    def getScheduledReporterResults (self):
        '''
        Gets back results from scheduled reporters as a Python list
        returns None if simulation has not finished yet.
        '''
        bytes_result = self.__bridge.getScheduledReporterResults(self.__session)
        if self.__reporters_length == 0:
            return bytes_result
        decoded_results = []
        for bytes_results_in_tick in bytes_result:
            decoded_results_in_tick = []
            for bytes_result_in_tick in bytes_results_in_tick:
                decoded_results_in_tick.append(NetLogoHeadlessWorkspace.decodeServerResult(bytes_result_in_tick))
            decoded_results.append(decoded_results_in_tick)
        return decoded_results
    def pause(self):
        self.__bridge.pause(self.__session)
    def unpause(self):
        self.__bridge.unpause(self.__session)
    
    def getParamSpace(self):
        '''
        Sends a signal to the server to tell the respective controller to get the
        parameter specs of its HeadlessWorkspace object
        '''
        return self.__bridge.getParamList(self.__session,self.__path)
    
    def setParamsRandom(self):
        '''
        Sets the parameters randomly through the JavaGateway using
        Random parameter initialization code from BehaviorSearch
        '''
        paramSpecs = self.__bridge.getParamList(self.__session, self.__path).getParamSpecs()        
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            if is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleDiscreteSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleContinuousSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if is_instance_of(self.__gateway,paramSpec,"bsearch.space.CategoricalSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
                if type(paramValue) != bool:#isinstance(data[i][k], bool)
                    paramValue = '"{}"'.format(paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast()))
            if is_instance_of(self.__gateway,paramSpec,"bsearch.space.ConstantSpec"):
                paramValue = paramSpec.generateRandomValue(self.__gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            print("NetLogo command: set " + str(paramSpec.getParameterName()) + " " + str(paramValue))
            self.__bridge.command(self.__session, "set " + str(paramSpec.getParameterName()) + " " + str(paramValue))
            

    def getParamNames(self):
        '''
        Returns the names of the parameters in the model
        '''
        paramSpecs = self.__bridge.getParamList(self.__session, self.__path).getParamSpecs()
        parameterNames = []
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            parameterNames.append(paramSpec.getParameterName())
        return parameterNames
    
    def getParamRanges(self):
        '''
        Returns the parameter ranges
        '''
        paramSpecs = self.__bridge.getParamList(self.__session, self.__path).getParamSpecs()
        paramRanges = []
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            paramRange = []
            if (is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleDiscreteSpec") | is_instance_of(self.__gateway,paramSpec,"bsearch.space.DoubleContinuousSpec")) :
                count = paramSpec.choiceCount()
                val_min = paramSpec.getValueFromChoice(0,count)
                val_max = paramSpec.getValueFromChoice(count - 1,count)
                step = (val_max - val_min)/(count - 1)
                paramRange = [val_min,step,val_max]
            if is_instance_of(self.__gateway,paramSpec,"bsearch.space.CategoricalSpec"):
                count = paramSpec.choiceCount()
                paramRange = []
                for choice in range(0,count):
                    paramRange.append(paramSpec.getValueFromChoice(choice,count))
            if is_instance_of(self.__gateway,paramSpec,"bsearch.space.ConstantSpec"):
                paramRange = [paramSpec.getValueFromChoice(0,1)]
            paramRanges.append(paramRange)
        return paramRanges
    
    
    def deleteWorkspace(self):
        '''
        Kills the Workspace and its controller on the server
        '''
        self.__bridge.removeControllerFromStore(self.__session)

    def getSession(self):
        return self.__session

    def decodeServerResult(result_bytes):
        result = result_bytes.decode()
        try:
            result = float(result)
        except ValueError:
            pass
        return result