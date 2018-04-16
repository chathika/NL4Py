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
from py4j.protocol import Py4JError
import subprocess
import threading
import os
import atexit
import sys
import logging
from contextlib import suppress
##############################################################################
'''Responsible for starting and stopping the NetLogo Controller Server'''
class NetLogo_Controller_Server_Starter:
    
    __gw = None# New gateway connection 
    ##server is in netlogo app folder
    
    
    def __init__(self):
        logger = logging.getLogger("py4j")
        logger.propagate = False
        self.__gw = JavaGateway()
        self.shutdownServer()
        atexit.register(self.shutdownServer)
    '''Internal method to start JavaGateway server. Will be called by starServer on seperate thread'''
    def __runServer(self): 
        __server_name = "emd.server.NetLogoControllerServer"
        nl_path = os.environ['NETLOGO_APP']
        nl_path = os.path.join(os.path.abspath(os.environ['NETLOGO_APP']),"*")
        os.pathsep
        server_path = "./server/*"
        classpath = nl_path + os.pathsep + server_path
        result = subprocess.call(["java", "-cp",  classpath , __server_name])
        print(result)
        if (result == '1'):
            raise NL4PyControllerServerException("The controller server couldn't start")
        
    '''Starts JavaGateway server'''
    def startServer(self):
        #Fire up the NetLogo Controller server through python
        thread = threading.Thread(target=self.__runServer, args=())
        thread.start()
        
    '''Send shutdown signal to the JavaGateway server. No further communication is possible unless server is restarted'''
    def shutdownServer(self):
        logger = logging.getLogger("py4j")
        logger.propagate = False
        print('Shutting down old server instances...')
        __bridge = self.__gw.entry_point
        try:
            self.__gw.shutdown()
            __bridge.shutdownServer()
        except:
            pass