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
	burnedTreesCount = []
	workspacesRunning = []
	threadCount = 8
	while runsDone != runsNeeded:
		runningWorkspacesCount = int(runsNeeded - runsDone if (runsNeeded - runsDone) <= threadCount else threadCount)
		for i in range(0,int(runningWorkspacesCount)):
			n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
		workspacesRunning = nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces()
		for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
			workspace.openModel(model)
			workspace.setParamsRandom()
			reporters = ["ticks", "not any? turtles"]
			workspace.command("setup")
			workspace.scheduleReportersAndRun(reporters, 0,1,10000, "go")
		while len(workspacesRunning) != 0:
			time.sleep(0.05)
			for workspace in workspacesRunning:
				try:
					workspaceResults = workspace.getScheduledReporterResults()
				except:
					workspacesRunning.remove(workspace)
					workspace.deleteWorkspace()
				if len(workspaceResults) > 0:
					if workspaceResults[0][0] == 1000 or workspaceResults[0][1]:
						burnedTreesCount.append(workspace.report("burned-trees"))
						workspacesRunning.remove(workspace)
						workspace.deleteWorkspace()
		runsDone = runsDone + runningWorkspacesCount
	stopTime = int(round(time.time() * 1000))
	totalTime = stopTime - startTime
#	print(burnedTreesCount)
	burnedTreesCount = []
	return totalTime
print("\n1 Starting the NetLogoControllerServer with: nl4py.startServer()\n")
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
#		time.sleep(5)
	allTimes.append(timeIteration)
	print(allTimes)
print(allTimes)
import pandas as pd
p = pd.DataFrame(allTimes)
p.to_csv("AllTimes_Fire.csv")
print("DONE____________________________________________________ALL DONE____________________________________________________")
print(allTimes)
print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
