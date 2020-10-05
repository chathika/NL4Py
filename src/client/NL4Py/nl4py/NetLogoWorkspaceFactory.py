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

import multiprocessing

import numpy as np
import pandas as pd
from py4j.java_gateway import JavaGateway,GatewayParameters
from py4j.java_collections import SetConverter, MapConverter, ListConverter

from .NetLogoHeadlessWorkspace import NetLogoHeadlessWorkspace

class NetLogoWorkspaceFactory:

    def __init__ (self, server_port):
        self.server_port = server_port
        self.__java_gateway = JavaGateway(gateway_parameters=GatewayParameters(
                                            auto_convert=True,port=self.server_port))
        self.java_server = self.__java_gateway.jvm.nl4py.server.NetLogoControllerServer()
        self.__all_workspaces = []

    '''Create a new Headless Workspace and get a pointer to it'''
    def newNetLogoHeadlessWorkspace(self):
        n = NetLogoHeadlessWorkspace(self.server_port)
        self.__all_workspaces.append(n)
        return n

    '''Get a list of all existing Headless Workspaces on the server'''
    def getAllExistingWorkspaces(self):
        return self.__all_workspaces

    def deleteAllExistingWorkspaces(self):
        for __workspace in self.__all_workspaces:
            __workspace.deleteWorkspace()
        self.__all_workspaces = []
    def deleteHeadlessWorkspace(self,headlessWorkspace):
        headlessWorkspace.deleteWorkspace()
        self.__all_workspaces.remove(headlessWorkspace)

    def run_experiment(self, model_name, setup_callback, setup_data, reporters, 
                                                start_at_tick, interval, stop_at_tick,go_command,num_procs):
        num_procs = multiprocessing.cpu_count() if num_procs <= 0 else num_procs
        # assemble the init strings
        # Make sure that data is either iterable or None
        try:
            iterator = iter(setup_data)
        except TypeError:
            if setup_data is not None:
                print("data is not iterable")
            else:
                #If data is neither iterable nor None, then data will just be the names (1 indexed order)
                setup_data = list(range(len(setup_data)))
        except:
            print("Unkown exception")
            pass        
        #Make init strings
        init_strings_arrays = list(map(setup_callback, setup_data))
        #Validate init strings, user may have provided an array of strings, if so convert to a single string
        init_strings = list(map(validate_init_strings, init_strings_arrays))
        
        names = [str(i) for i in range(len(setup_data))]
        names_to_init_strings = [list(a) for a in zip(names, init_strings)]
        reporterArray=[]
        for idx, reporter in enumerate(reporters):
            reporterArray.append(str(reporter).encode())
        raw_results = self.java_server.runPoolOfTasks(model_name, names_to_init_strings, reporterArray, 
                                                start_at_tick, interval, stop_at_tick, go_command, num_procs)
        results = []
        for key in raw_results:
            results.append([init_strings[int(key)], raw_results[key]])
        return results

def validate_init_strings(init_strings):
    is_iterable = True
    try:
        iterator = iter(init_strings)
    except TypeError:
        print("callback must return a string or an iterable!")
        return
    except:
        print("Unkown exception")
        pass
    if type(init_strings) != str:
        init_strings = " ".join(init_strings)
    return init_strings
