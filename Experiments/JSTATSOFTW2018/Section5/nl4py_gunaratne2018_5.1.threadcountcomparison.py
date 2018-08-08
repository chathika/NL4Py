### This code compares execution time of NL4Py to run 1, 4, 8, and 16 parallel 
### NetLogo headless workspaces of the Wolf Sheep Predation model for 5000,
### 10000, and 15000 total model runs for 100 simulation ticks each. 
### ABM parameters are initialized to random values.
### Each parallel workspaces vs model runs combination is repeated 10 times 
### to account for different execution times under different parameter settings.
### To run: python nl4py_gunaratne2018_5.1.threadcountcomparison.py "path_to_netlogo"

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 
import sys
import time
import math
import os

def simulate(workspace_):
    workspace_.command("stop")
    #Set the input parameters
    workspace_.command("set initial-number-sheep random-float 250")
    workspace_.command("set initial-number-wolves random-float 250")
    workspace_.command("set grass-regrowth-time random-float 100")
    workspace_.command("set sheep-gain-from-food random-float 50")
    workspace_.command("set wolf-gain-from-food random 100")
    workspace_.command("set sheep-reproduce random-float 20")
    workspace_.command("set wolf-reproduce random-float 20")
    workspace_.command("set show-energy? false")
    workspace_.command('set model-version "sheep-wolves-grass"')
    workspace_.command('setup')
    workspace_.scheduleReportersAndRun(["ticks",'count sheep','count wolves'], 0,1,100,"go")    

def measureExecutionTime(runsNeeded,threadCount):
    startTime = int(round(time.time() * 1000))    
    runsDone = 0
    runsStarted = 0
    allResults = []
    # Create and reuse threadCount number of workspaces
    for i in range(0,threadCount):
        workspace = nl4py.newNetLogoHeadlessWorkspace()
        workspace.openModel('models/Wolf Sheep Predation.nlogo')
        simulate(workspace)
        runsStarted = runsStarted + 1
    # repeat until runsNeeded is satisfied
    while (runsDone < runsNeeded):
        # check if workspaces are done. If so, get results and
        #  start another model run on the workspace, keeping the 
        #  number of workspaces constant
        for workspace in nl4py.getAllHeadlessWorkspaces():
            newResults = workspace.getScheduledReporterResults()
            # getScheduledReporterResults() is non-blocking 
            # and can return an empty list if the model is 
            # still running. Check that the model is done by 
            # checking if the list is not empty.
            if len(newResults) > 0:
                allResults.extend(newResults)
                runsDone = runsDone + 1
                if runsStarted < runsNeeded:
                    # start another simulation if required.
                    simulate(workspace)
                    runsStarted = runsStarted + 1
    stopTime = int(round(time.time() * 1000))
    return (stopTime - startTime)
outputFile = "output/5.1_output.csv"
with open(outputFile, "a+") as myfile:
    myfile.write('model,runs,threads,connector,time.ms\n')
    # Start up the NetLogoControllerServer
    nl4py.startServer(str(sys.argv[1]))
    # Repeat to account for ABM stochasticity and random parameters
    for j in range(0,5):
        # Repeat for total model runs
        for modelRuns in [50,100,150]:
            # Repeat for different thread counts
            for threadCount in [1,4,8,16]:
                timeTaken = measureExecutionTime(modelRuns,threadCount)
                print(timeTaken)
                myfile.write('Wolf Sheep Predation,' + str(modelRuns) + ',' + str(threadCount) + ',NL4Py,' + str(timeTaken) + '\n')
                myfile.flush()
                # make sure the server is clean before next evaluation.
                nl4py.deleteAllHeadlessWorkspaces()
# Release resources
myfile.close()
nl4py.stopServer()
