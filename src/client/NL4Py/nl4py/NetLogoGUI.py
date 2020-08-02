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

import numpy as np
from py4j.java_gateway import JavaGateway, GatewayParameters
from py4j.protocol import Py4JNetworkError, Py4JJavaError
import py4j.java_gateway as jg

from .NL4PyException import deprecated

class NetLogoGUI:
    '''
    Responsible for communicating with the NetLogo controller, a Java executable
    and creates a GUI workspace controller on the server.
    
    '''
    def __init__(self, server_starter : 'nl4py.NetLogoControllerServerStarter.NetLogoControllerServerStarter' ):
        self.server_starter = server_starter
        self.java_server = self.server_starter.jg.jvm.nl4py.server.NetLogoControllerServer()
        self.server_gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True,port=server_starter.server_port))
        gs = self.java_server.newGateway()
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True,port=gs.getPort(),auto_close=True))
        self.app = self.gateway.jvm.nl4py.server.NetLogoAppController(gs)
    
    def open_model(self, path : str):
        '''Opens a NetLogo model'''
        self.path = path
        self.app.openModel(self.path)
        
    def close_model(self):
        '''Sends a signal to the server to tell the respective controller to close its'''
        '''HeadlessWorkspace object'''
        pass
        #self.app.closeModel(self.__session)
    
    def command(self, command : str):
        '''
        Sends a signal to the server to tell the respective controller to send a
        NetLogo command to its HeadlessWorkspace object
        
        '''
        self.app.command(command)
    
    def report(self, reporter : str) -> str:
        '''
        Sends a signal to the server to tell the respective controller to execute a
        reporter on its HeadlessWorkspace object
        
        '''   
        result = self.app.report(reporter.encode()).decode()
        return result

    def schedule_reporters(self, reporters : list, startAtTick : int = 0, intervalTicks : int = 1, 
                                        stopAtTick : int = -1, goCommand : str = 'go') -> list:
        '''
        Schedules a set of reporters at a start tick for an interval until a stop tick
        
        '''
        reporterArray = []
        for idx, reporter in enumerate(reporters):
            reporterArray.append(str(reporter).encode())
        ticks_reporters_results = self.app.scheduleReportersAndRun(
                                reporterArray,startAtTick,intervalTicks,stopAtTick,goCommand)
        out_ticks_reporter_results = []
        for reporters_results in ticks_reporters_results:
            out_reporter_results = []
            for result in reporters_results:
                out_reporter_results.append(result)
            out_ticks_reporter_results.append(out_reporter_results)
        return out_ticks_reporter_results
    
    def get_param_space(self) -> 'jvm.nl4py.server.bsearch.space.SearchSpace':
        '''
        Sends a signal to the server to tell the respective controller to get the
        parameter specs of its HeadlessWorkspace object
        
        '''
        return self.app.getParamList(self.path)
    
    def set_params_random(self):
        '''
        Sets the parameters randomly through the JavaGateway using
        Random parameter initialization code from BehaviorSearch
        
        '''    
        paramSpecs = self.app.getParamList(self.path).getParamSpecs()
        
        ##Using some bsearch code here thanks to Forrest Stonedahl
        for paramSpec in paramSpecs:
            if jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleDiscreteSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleContinuousSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            if jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.CategoricalSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
                if type(paramValue) != bool:#isinstance(data[i][k], bool)
                    paramValue = '"{}"'.format(paramSpec.generateRandomValue(
                                                            self.gateway.jvm.org.nlogo.api.MersenneTwisterFast()))
            if jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.ConstantSpec'):
                paramValue = paramSpec.generateRandomValue(self.gateway.jvm.org.nlogo.api.MersenneTwisterFast())
            print('NetLogo command: set ' + str(paramSpec.getParameterName()) + ' ' + str(paramValue))
            self.app.command('set ' + str(paramSpec.getParameterName()) + ' ' + str(paramValue))
            
    
    def get_param_names(self) -> list:
        '''
        Returns the names of the parameters in the model
        
        '''
        paramSpecs = self.app.getParamList(self.path).getParamSpecs()
        parameterNames = []
        ##Using some bsearch code here thanks to Forrest Stonedahl
        for paramSpec in paramSpecs:
            parameterNames.append(paramSpec.getParameterName())
        return parameterNames
    
    def get_param_ranges(self) -> list:
        '''
        Returns the parameter ranges
        
        '''
        paramSpecs = self.app.getParamList(self.path).getParamSpecs()
        paramRanges = []
        ##Using some bsearch code here thanks to Forrest Stonedahl
        for paramSpec in paramSpecs:
            paramRange = []
            if (jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleDiscreteSpec') | 
                                    jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.DoubleContinuousSpec')) :
                count = paramSpec.choiceCount()
                val_min = paramSpec.getValueFromChoice(0,count)
                val_max = paramSpec.getValueFromChoice(count - 1,count)
                step = (val_max - val_min)/(count - 1)
                paramRange = [val_min,step,val_max]
            if jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.CategoricalSpec'):
                count = paramSpec.choiceCount()
                paramRange = []
                for choice in range(0,count):
                    paramRange.append(paramSpec.getValueFromChoice(choice,count))
            if jg.is_instance_of(self.gateway,paramSpec,'bsearch.space.ConstantSpec'):
                paramRange = [paramSpec.getValueFromChoice(0,1)]
            paramRanges.append(paramRange)
        return paramRanges
    



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