from os import environ
import sys
import multiprocessing
import nl4py

netlogo_path = str(sys.argv[1])
runsNeeded = int(sys.argv[2])
ticksNeeded = int(sys.argv[3])
# Replace argument to startServer(...) with the location of your NetLogo installation 
nl4py.startServer(netlogo_path)

import time
def ethnocentrism_setup_callback(data):
    # Same netlogo commands as used for the PyNetLogo evaluation
    setup_commands = []
    setup_commands.append("random-seed " + str(data))
    #setup_commands.append("set mutation-rate 0.005")
    setup_commands.append("set death-rate 0.1")
    setup_commands.append("set immigrants-per-day 1")
    setup_commands.append("set immigrant-chance-cooperate-with-same 0.5")
    setup_commands.append("set immigrant-chance-cooperate-with-different 0.5")
    setup_commands.append("set initial-PTR 0.12")
    setup_commands.append("set cost-of-giving 0.01")
    setup_commands.append("set gain-of-receiving 0.03")
    setup_commands.append('setup-empty')
    return setup_commands

def testRunExperiment(runsNeeded,ticksNeeded):
    # Make sure we start n headless workspaces to compare to n IPCluster engines running PyNetLogo
    modelname = "./Models/Ethnocentrism.nlogo"
    measures = ['ticks','count turtles']
    data = list(range(runsNeeded))
    results = nl4py.runExperiment(model_name = modelname, callback=ethnocentrism_setup_callback,data=data,reporters=measures, start_at_tick=0,interval=1,stop_at_tick=ticksNeeded,go_command="go",num_procs=multiprocessing.cpu_count())    
    return results

results = testRunExperiment(runsNeeded,ticksNeeded)
nl4py.stopServer()