########Demonstration of NL4Py#################
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 
import sys
import time
import math

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
    for i in range(0,threadCount):
        workspace = nl4py.newNetLogoHeadlessWorkspace()
        workspace.openModel('./Wolf Sheep Predation.nlogo')
        simulate(workspace)
        runsStarted = runsStarted + 1
    while (runsDone < runsNeeded):
        for workspace in nl4py.getAllHeadlessWorkspaces():
            newResults = workspace.getScheduledReporterResults()
            if len(newResults) > 0:
                allResults.extend(newResults)
                runsDone = runsDone + 1
                if runsStarted < runsNeeded:
                    simulate(workspace)
                    runsStarted = runsStarted + 1
    stopTime = int(round(time.time() * 1000))
    return (stopTime - startTime)

with open("Times_Comparison_Threads.csv", "a+") as myfile:
	myfile.write('model,runs,threads,connector,time.ms\n')
nl4py.startServer("C:/Program Files/NetLogo 6.0.3")
for j in range(0,10):
	for modelRuns in [5000,10000,15000]:
		for threadCount in [1,4,8,16]:
			timeTaken = measureExecutionTime(modelRuns,threadCount)
			print(timeTaken)
			with open("Times_Comparison_Threads.csv", "a+") as myfile:
				myfile.write('Wolf Sheep Predation,' + str(modelRuns) + ',' + str(threadCount) + ',NL4Py,' + str(timeTaken) + '\n')
			nl4py.deleteAllHeadlessWorkspaces()
nl4py.stopServer()
