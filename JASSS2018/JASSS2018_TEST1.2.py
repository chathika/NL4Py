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
def openModelAndRun(workspace_, model_):
	workspace_.openModel(model_)
	workspace_.setParamsRandom()
	reporters = ["ticks", "not any? turtles", "not any? wolves and count sheep > max-sheep"]
	workspace_.command("setup")
	workspace_.scheduleReportersAndRun(reporters, 0,1,100, "go")
def doNRuns(runsNeeded, threadCount_):
	model = "./Wolf Sheep Predation.nlogo"
	startTime = int(round(time.time() * 1000))
	runsDone = 0
	sheepCount = []
	wolfCount = []
	workspacesRunning = []
	threadCount = threadCount_

	runningWorkspacesCount = int(runsNeeded - runsDone if (runsNeeded - runsDone) <= threadCount else threadCount)
	for i in range(0,int(runningWorkspacesCount)):
		n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
	for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
		openModelAndRun(workspace, model)
	runsStarted = len(nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces())
#	time.sleep(0.05)
	while(runsDone < runsNeeded):
#		print(runsDone)
		for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
			try:
				workspaceResults = workspace.getScheduledReporterResults()
				if len(workspaceResults) > 0:
					if workspaceResults[0][0] == 100 or workspaceResults[0][1] or workspaceResults[0][2]:
						sheepCount.append(workspace.report("count sheep"))
						wolfCount.append(workspace.report("count wolves"))
						nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces().remove(workspace)
						workspace.deleteWorkspace()
						workspace = None
						runsDone = runsDone + 1
						if(runsDone == runsNeeded):
							break
						if(runsStarted != runsNeeded):
							runsStarted = runsStarted + 1
							replacement = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
							openModelAndRun(replacement,model)
			except:
				print("exception")
				nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces().remove(workspace)
				workspace.deleteWorkspace()
				if(runsStarted != runsNeeded):
					runsStarted = runsStarted + 1
					replacement = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
					openModelAndRun(replacement,model)
	stopTime = int(round(time.time() * 1000))
	totalTime = stopTime - startTime
#	print(sheepCount)
#	print(wolfCount)
	print(runsDone)
	wolfCount = []
	sheepCount = []
	return totalTime
print("\n1 Starting the NetLogoControllerServer with: nl4py.startServer()\n")
nl4py.startServer()
time.sleep(2)
allTimes = []
for j in range(0,5):
	for i in range(10,16):
		for threadCount in [1,2,4,8,16]:
			print("Runs ", i*1000, "Threads " , threadCount)
			timeTaken = doNRuns(i*1000, threadCount)
			allTimes.append([i,threadCount,timeTaken])
			print(allTimes)
			try:
				nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces()
			except:
				pass
print(allTimes)
import pandas as pd
p = pd.DataFrame(allTimes)
p.to_csv("AllTimes_WolfSheepPredation.csv")
print("DONE____________________________________________________ALL DONE____________________________________________________")
print(allTimes)
print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
