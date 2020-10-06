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
import logging
import psutil
import math
import platform
import glob
import pkg_resources
import socket

from py4j.java_gateway import JavaGateway, launch_gateway, GatewayParameters

class NetLogoControllerServerStarter:
    '''
    Responsible for starting and stopping the NetLogo Controller Server
    '''

    def __init__(self, netlogo_home : str,server_port : int = 25333):
        '''
        path to NetLogo installation's root folder
        '''
        self.netlogo_home = netlogo_home
        self.SERVER_PATH = pkg_resources.resource_filename('nl4py', 'nl4pyServer/')
        self.server_port = server_port
        self.init_server()
        self.jg = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True,port=self.server_port))
    
    def init_server(self) -> int: 
        '''
        Internal method to start a new JavaGateway server. Will be on seperate thread using Py4J.

        :returns: int port to listen on for new JavaGateway server. 
        '''

        py4j_jar_path = glob.glob(os.path.join(self.SERVER_PATH, "py4j*.jar"))[0]
        __server_name = "nl4py.server.NetLogoControllerServer"
        nl_path = ""
        if self.netlogo_home == None:
            #Following is legacy for 0.3.0 support and is deprecated with 0.3.1
            try:
                nl_home = os.environ['NETLOGO_HOME']
                if(platform.system() == "Darwin"):
                    nl_path = os.path.join(nl_home,"Java")
                else:
                    nl_path = os.path.join(nl_home,"app")
            except KeyError:            
                try:
                    nl_path = os.environ['NETLOGO_APP']
                except KeyError:
                    #looks like the NETLOGO_APP variable isn't set... 
                    #Trying to use os dependent defaults
                    print("NETLOGO_APP was not set, trying to find NetLogo .jar files")
                    if(platform.system() == "Windows"):
                        nl_path = "C:/Program Files/NetLogo 6.0.2/app"
                    if(platform.system() == "Darwin"):
                        nl_path = "/Applications/NetLogo 6.0.2/Java"
                    pass
                pass
        else:
            if(platform.system() == "Darwin"):
                nl_path = os.path.join(self.netlogo_home,"Java")
            else:
                nl_path = os.path.join(self.netlogo_home,"app")
        if len(glob.glob(os.path.join(nl_path,"netlogo-[0-9]*.jar"))) == 0:
            print("NetLogo not found! Please provide netlogo_home directory to nl4py.initialize()")
            return
        else:
            ver_info = os.path.split(glob.glob(os.path.join(nl_path,"netlogo-[0-9]*.jar"))[0])[-1].split(".")
            major = float(ver_info[0].split("-")[-1])
            minor = float("0." + ver_info[1])
            major_minor = major + minor
            if major_minor < 6.1:
                os.environ['NL4Py_NetLogo_Ver'] = "6.1"
                self.SERVER_PATH = os.path.join(self.SERVER_PATH,"NetLogo6.0")
            else: 
                os.environ['NL4Py_NetLogo_Ver'] = "6.0"
                self.SERVER_PATH = os.path.join(self.SERVER_PATH,"NetLogo6.1")
        nl_docs = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"docs")
        nl_extensions = "-Dnetlogo.extensions.dir=" + os.path.join(nl_path,"extensions")
        nl_models = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"models")
        if(platform.system() == "Darwin"):
            nl_docs = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"../docs")
            nl_extensions = "-Dnetlogo.extensions.dir=" + os.path.join(nl_path,"../extensions")
            nl_models = "-Dnetlogo.docs.dir=" + os.path.join(nl_path,"../models")
        nl_path = os.path.join(os.path.abspath(nl_path),"*")
        server_path = os.path.join(os.path.abspath(self.SERVER_PATH),"NetLogoControllerServer.jar")
        xmx = psutil.virtual_memory().available / 1024 / 1024 / 1024
        xms = "-Xms" + str(int(math.floor(xmx - 2))) + "G"
        xmx = "-Xmx" + str(int(math.floor(xmx))) + "G"
        preferHeadless = "-Dorg.nlogo.preferHeadless=true" #important for levelspace
        classpath = os.pathsep.join([server_path, nl_path])
        #Py4j uses port 25333 by default, check if available before connecting
        if not is_port_in_use(self.server_port):
            port = launch_gateway(classpath=classpath, port = self.server_port,
                    javaopts=[preferHeadless,nl_docs,nl_extensions,nl_models,xmx,"-XX:-UseGCOverheadLimit"], die_on_exit=True, java_path='java'
                    )
   
    
    def shutdown_server(self):
        '''
        Send shutdown signal to the JavaGateway server. No further communication is possible unless server is restarted
        '''
        if(self.jg != None):    
            try:
                logging.disable(logging.CRITICAL)
                self.jg.shutdownServer()
                self.jg.close(keep_callback_server=False, close_callback_server_connections=True)
                self.jg = None
            except Exception as e:
                pass

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0