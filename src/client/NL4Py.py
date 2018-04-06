#!pip install py4j
from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
import subprocess
import threading
import os
import atexit
##############################################################################
'''Responsible for starting and stopping the NetLogo Controller Server'''
class NetLogo_Controller_Server_Starter:
    
    __gw = JavaGateway()# New gateway connection 
    ##server is in netlogo app folder
    __server_name = "C:/Program Files/NetLogo 6.0.2/app/NetLogoControllerServer.jar"
    
    def __init__(self):
        atexit.register(self.shutdownServer)
    '''Internal method to start JavaGateway server. Will be called by starServer on seperate thread'''
    def __runServer(self): 
        
        env = dict(os.environ)
        env['JAVA_OPTS'] = ''
        print(subprocess.call(['java', '-jar', self.__server_name]))
    
    '''Starts JavaGateway server'''
    def startServer(self):
        #Fire up the NetLogo Controller server through python
        thread = threading.Thread(target=self.__runServer, args=())
        thread.start()
        
    '''Send shutdown signal to the JavaGateway server. No further communication is possible unless server is restarted'''
    def shutdownServer(self):
        print('Shutting Down Server')
        self.__gw.shutdown(True)
    
    
##############################################################################

'''Responsible for communicating with the NetLogo controller, a Java executable'''
class NetLogo_HeadlessWorkspace:
    __bridge = None
    __gateway = None 
    __session = None
    def __init__(self):
        self.__gateway = JavaGateway()# New gateway connection
        self.__bridge = self.__gateway.entry_point
    
    #######################################################
    ###Below are public functions of the NL4Py interface###
    #######################################################
    
    '''Opens a NetLogo model and creates a headless workspace controller on the server'''
    '''Returns a session id for this controller to be used for further use of this ABM'''
    def openModel(self, path):
        try:
            self.__session = self.__bridge.openModel(path)
        except Py4JNetworkError:
            raise NL4PyControllerServerException("Did you copy the NetLogoControllerServer.jar into your NetLogo/app folder?")
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
    def getParamSpace(self, path):
        self.__bridge.getParamList(self.__session,path)
    #An extra helpful method:
    '''Sets the parameters randomly through the JavaGateway using'''
    '''Random parameter initialization code from BehaviorSearch'''
    def setParamsRandom(self, model_string):
        paramSpecs = self.__bridge.getParamList(self.__session, model_string).getParamSpecs()
        
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
            
class NL4PyControllerServerException(Exception):
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"{0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements
        

NLCSStarter = NetLogo_Controller_Server_Starter()

NLCSStarter.startServer()