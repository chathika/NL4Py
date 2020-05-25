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
from .NetLogoHeadlessWorkspace import NetLogoHeadlessWorkspace
import multiprocessing
#import NL4PyControllerServerException
from py4j.java_gateway import JavaGateway,GatewayParameters
from py4j.java_collections import SetConverter, MapConverter, ListConverter
import copy 
import numpy as np
import pandas as pd

class NetLogoWorkspaceFactory:
    __all_workspaces = []
    __session_workspaces_dict = {}
    __java_gateway = None
    def __init__ (self):
        self.__java_gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
        return
    '''Create a new Headless Workspace and get a pointer to it'''
    def newNetLogoHeadlessWorkspace(self):
        n = NetLogoHeadlessWorkspace(self.__java_gateway)
        self.__all_workspaces.append(n)
        self.__session_workspaces_dict[n.getSession()] = n
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

    def runReportersOnWorkspaces(self, workspaces, reporters, startAtTick, intervalTicks, stopAtTick, goCommand):
        sessions = [workspace.getSession() for workspace in workspaces]
        results_allws_allticks = self.__java_gateway.entry_point.runReportersOnWorkspaces(sessions,reporters, startAtTick,intervalTicks,stopAtTick,goCommand)
        results_dictionary = {}
        for session in results_allws_allticks.keys():
            ws = self.__session_workspaces_dict[session]
            results_dictionary[ws] = []
            for result_ws_tick in results_allws_allticks[session]:
                try:
                    results_dictionary[ws].append(copy.deepcopy(eval(result_ws_tick)))
                except:
                    results_dictionary[ws].append(result_ws_tick)
                    pass
        return results_dictionary
    
    def runExperiment(self, model_name, callback, data, reporters, start_at_tick, interval, stop_at_tick,go_command,num_procs):
        num_procs = multiprocessing.cpu_count() if num_procs <= 0 else num_procs
        # assemble the init strings
        # Make sure that data is either iterable or None
        try:
            iterator = iter(data)
        except TypeException:
            if data is not None:
                print("data is not iterable")
            else:
                #If data is neither iterable nor None, then data will just be the names (1 indexed order)
                data = list(range(len(data)))
        except:
            print("Unkown exception")
            pass
        
        #Make init strings
        init_strings_arrays = list(map(callback, data))
        #Validate init strings, user may have provided an array of strings, if so convert to a single string
        init_strings = list(map(validate_init_strings, init_strings_arrays))
        
        names = [str(i) for i in range(len(data))]
        names_to_init_strings = [list(a) for a in zip(names, init_strings)]
        names_to_init_strings_chunks = np.array_split(names_to_init_strings,num_procs)
        ## namesToInitStringsChunks [[[1,"nl commands"],[2,"nl commands"],...],[[[num_procs+1,"nl commands"],[num_procs+2,"nl commands"],...]],[[]],...[[]]] -> dim[num_procs, n/num_procs ,2]
        pool = self.__java_gateway.entry_point.initPool(model_name, num_procs, names_to_init_strings_chunks, reporters, start_at_tick, interval, stop_at_tick, go_command)
        all_results = pool.run()
        results_dict = {}
        for result_name in sorted(list(map(int,all_results.keys()))):
            results_dict[result_name] = []
            results_dict[result_name].append(init_strings_arrays[result_name])
            results_dict[result_name].append(all_results[str(result_name)])
        all_results = pd.DataFrame.from_dict(results_dict,orient="index",columns=["Setup", "Results"])
        return all_results

def validate_init_strings(init_strings):
    is_iterable = True
    try:
        iterator = iter(init_strings)
    except TypeException:
        print("callback must return a string or an iterable!")
        return
    except:
        print("Unkown exception")
        pass
    if type(init_strings) != str:
        init_strings = " ".join(init_strings)
    return init_strings

##############################################################################