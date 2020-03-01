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

    def runExperiment(self, model_name, callback, names, data=None, num_procs=-1):
        results_dict = {}
        pool = self.__java_gateway.entry_point.createWorkspacePool(model_name, len(names),num_procs)
        for idx in range(len(names)):
            # Try to schedule and execute workers as available
            ws = pool.getFreeWorkspace() #blocking method. Server will wait if there is no free workspace at the moment
            ws.setRunName(str(names[idx]))
            config = data
            try:
                config = data[idx]
            except:
                pass
            #results_dict[str(names[idx])] = {"config":config}
            if data == None:
                data = names
            try:
                callback(ws,data[idx])
            except Exception as e:
                callback(ws,names[idx])
                print("NL4Py WARNING: data must be a list or iterable of equal length to names!")
            ws.notifyWhenDone()
        #Wait for pool to finish execution of all configurations and get results
        all_results = pool.awaitResults()
        #for result_name in all_results.keys():
        #    results_dict[result_name]["results"] = all_results[result_name]
        return all_results

##############################################################################