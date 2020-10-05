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
import socket

from py4j.protocol import Py4JNetworkError
from py4j.java_gateway import JavaGateway, GatewayParameters, is_instance_of

from .NL4PyException import NL4PyControllerServerException, deprecated

class NetLogoHeadlessWorkspace:
    '''
    Responsible for communicating with the NetLogo controller Java executable
    '''
    
    def __init__(self, server_port : int):
        '''
        Returns a session id for this controller to be used for further use of this ABM
        and creates a headless workspace controller on the server.

        :param server_port: server port
        '''

        server_gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True,port=server_port))
        self.java_server = server_gateway.jvm.nl4py.server.NetLogoControllerServer()
        #self.server_gateway = JavaGateway(gateway_parameters=GatewayParameters(
        #                                    auto_convert=True,port=server_port))
        gs = self.java_server.newGateway()
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(
                                            auto_convert=True,port=gs.getPort(),auto_close=True))
        self.hwc = self.gateway.jvm.nl4py.server.HeadlessWorkspaceController(gs)

    def open_model(self, path : str):
        '''
        Opens a NetLogo model
        '''
        try:
            self.__path = path
            self.hwc.openModel(self.__path)
        except Py4JNetworkError as e:
            raise NL4PyControllerServerException(('Looks like the server is unreachable! Maybe '
                            'the socket is busy? Trying running nl4py.stopServer() and trying again.'))
    
    def close_model(self):
        '''
        Sends a signal to the server to tell the respective controller to close its
        HeadlessWorkspace object
        '''
        self.hwc.closeModel()

    def command(self, command : str):
        '''
        Sends a signal to the server to tell the respective controller to send a
        NetLogo command to its HeadlessWorkspace object
        '''
        self.hwc.command(command)
    
    def report(self, reporter : str) -> str:
        '''
        Sends a signal to the server to tell the respective controller to execute a
        reporter on its HeadlessWorkspace object
        '''
        result = eval(self.hwc.report(reporter.encode()).decode())
        return result

    def schedule_reporters(self, reporters : list, startAtTick : int = 0, intervalTicks : int = 1, 
                                        stopAtTick : int = -1, goCommand : str = 'go') -> list:
        '''
        Schedules a set of reporters at a start tick for an interval until a stop tick
        '''
        reporterArray = []
        for idx, reporter in enumerate(reporters):
            reporterArray.append(str(reporter).encode())
        ticks_reporters_results = self.hwc.scheduleReportersAndRun(
                                reporterArray,startAtTick,intervalTicks,stopAtTick,goCommand)
        out_ticks_reporter_results = []
        for reporters_results in ticks_reporters_results:
            out_reporter_results = []
            for result in reporters_results:
                out_reporter_results.append(result)
            out_ticks_reporter_results.append(out_reporter_results)
        return out_ticks_reporter_results

    def refresh(self):
        '''
        Sends a signal to the server to tell the respective controller to create a
        new instance of its HeadlessWorkspace object
        '''
        self.hwc.refresh()
    
    def export_view(self, filename : str):
        '''
        Sends a signal to the server to tell the respective controller to export the view
        of its HeadlessWorkspace object
        '''
        self.hwc.exportView(filename)

     
    def get_param_space(self):
        '''
        Sends a signal to the server to tell the respective controller to get the
        parameter specs of its HeadlessWorkspace object
        '''
        return self.hwc.getParamList(self.__path)
    
    def set_params_random(self):
        '''
        Sets the parameters randomly through the JavaGateway using
        Random parameter initialization code from BehaviorSearch
        '''
        paramSpecs = self.hwc.getParamList(self.__path).getParamSpecs()        
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            if is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleDiscreteSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleContinuousSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if is_instance_of(self.gateway,paramSpec,'bsearch.space.CategoricalSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
                if type(paramValue) != bool:
                    paramValue = '"{}"'.format(paramSpec.generateRandomValue(
                                                        self.gateway.jvm.org.nlogo.api.MersenneTwisterFast()))
            if is_instance_of(self.gateway,paramSpec,'bsearch.space.ConstantSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            print('NetLogo command: set ' + str(paramSpec.getParameterName()) + ' ' + str(paramValue))
            self.hwc.command('set ' + str(paramSpec.getParameterName()) + ' ' + str(paramValue))
            
    def get_param_names(self) -> list:
        '''
        Returns the names of the parameters in the model
        '''
        paramSpecs = self.hwc.getParamList(self.__path).getParamSpecs()
        parameterNames = []
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            parameterNames.append(paramSpec.getParameterName())
        return parameterNames
    
    def get_param_ranges(self) -> list:
        '''
        Returns the parameter ranges
        '''
        paramSpecs = self.hwc.getParamList(self.__path).getParamSpecs()
        paramRanges = []
        ##Using some bsearch code here thanks to Forrest Stonedahl and the NetLogo team
        for paramSpec in paramSpecs:
            paramRange = []
            if (is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleDiscreteSpec') | 
                                is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleContinuousSpec')) :
                count = paramSpec.choiceCount()
                val_min = paramSpec.getValueFromChoice(0,count)
                val_max = paramSpec.getValueFromChoice(count - 1,count)
                step = (val_max - val_min)/(count - 1)
                paramRange = [val_min,step,val_max]
            if is_instance_of(self.gateway,paramSpec,'bsearch.space.CategoricalSpec'):
                count = paramSpec.choiceCount()
                paramRange = []
                for choice in range(0,count):
                    paramRange.append(paramSpec.getValueFromChoice(choice,count))
            if is_instance_of(self.gateway,paramSpec,'bsearch.space.ConstantSpec'):
                paramRange = [paramSpec.getValueFromChoice(0,1)]
            paramRanges.append(paramRange)
        return paramRanges
    
    def deleteWorkspace(self):
        '''
        Kills the Workspace and its controller on the server
        '''
        self.hwc.removeControllerFromStore()
        self.gateway.close()
    
    @deprecated('Alias left for backward compatibility. Use open_model() since version 1.0.0.')
    def openModel(self, path):
        self.open_model(path)

    @deprecated('Alias left for backward compatibility. Use close_model() since version 1.0.0.')
    def closeModel(self):
        self.close_model()

    @deprecated(('Alias left for backward compatibility. Use schedule_reporters(reporters, startAtTick=0, '
                                'intervalTicks=1, stopAtTick=-1, goCommand=\'go\') since version 1.0.0.'))
    def scheduleReportersAndRun(self, reporters, startAtTick=0, intervalTicks=1, stopAtTick=-1, goCommand='go'):
        return self.schedule_reporters(reporters, startAtTick, intervalTicks, stopAtTick, goCommand)
    
    @deprecated('Alias left for backward compatibility. Use export_view(filename) since version 1.0.0.')
    def exportView(self, filename):
        self.export_view(filename)

    @deprecated('scheduleReportersAndRun(...) returns result since version 1.0.0.')
    def awaitScheduledReporterResults(self):
        pass

    @deprecated('scheduleReportersAndRun(...) returns result since version 1.0.0.')
    def getScheduledReporterResults (self):
        pass

    @deprecated('Alias left for backward compatibility. Use getParamSpace() since version 1.0.0.')
    def getParamSpace(self):
        return self.get_param_space()

    @deprecated('Alias left for backward compatibility. Use setParamsRandom() since version 1.0.0.')
    def setParamsRandom(self):
        self.set_params_random()

    @deprecated('Alias left for backward compatibility. Use getParamNames() since version 1.0.0.')
    def getParamNames(self):
        return self.get_param_names()

    @deprecated('Alias left for backward compatibility. Use getParamRanges() since version 1.0.0.')
    def getParamRanges(self):
        return self.get_param_ranges()