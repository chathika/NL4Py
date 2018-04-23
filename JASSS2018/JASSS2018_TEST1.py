########Demonstration of NL4Py#################
#This example takes two commandline arguments n and model
#n : number of concurrent model runs required.
#model: path to model file
#example usage: python NRunsOfAModel.py 100 "/path/to/model.nlogo"
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 
import sys
import time
import math


def doNRuns(runsNeeded):
	model = "./Fire.nlogo"
	startTime = int(round(time.time() * 1000))
	runsDone = 0
	while runsDone != runsNeeded:
		workspaceCount = int(runsNeeded - runsDone if (runsNeeded - runsDone) <= 256 else 256)
		for i in range(0,workspaceCount):
			n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
		for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
			workspace.openModel(model)
			workspace.setParamsRandom()
		for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
			workspace.command("setup")
			workspace.command("go")
		result = []
		for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
			result.append(workspace.report("burned-trees"))
		runsDone = runsDone + workspaceCount
		nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces() 
	stopTime = int(round(time.time() * 1000))
	totalTime = stopTime - startTime
	print(result)
	result = []
	return totalTime
print("\n1) Starting the NetLogoControllerServer with: nl4py.startServer()\n")
nl4py.startServer()
time.sleep(2)
allTimes = []
for j in range(0,30):
	timeIteration = []
	for i in range(1,11):
		timeTaken = doNRuns(math.pow(2,i))
		timeIteration.append(timeTaken)
		print(timeTaken)
		nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces() 
		time.sleep(5)
	allTimes.append(timeIteration)
	print(allTimes)
print(allTimes)
import pandas as pd
pd.DataFrame(allTimes)
pd.to_csv("AllTimes_Fire.csv")

print("DONE____________________________________________________ALL DONE____________________________________________________")
print(allTimes)
print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
