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
	workspace_.command('set model-version "sheep-wolves-grass"') # make sure we run the right version of the model 
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
	while(runsDone != runsNeeded):
#		print(runsDone)
		time.sleep(0.5)
		for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
			try:
				workspaceResults = workspace.getScheduledReporterResults()
				if len(workspaceResults) > 0:
					ticks = int(float(workspaceResults[-1][0]))
					stop1 = str(workspaceResults[-1][1]).lower() == "true"
					stop2 = str(workspaceResults[-1][2]).lower() == "true"
					if (ticks == 100) or stop1 or stop2:
						sheepCount.append(workspace.report("count sheep"))
						wolfCount.append(workspace.report("count wolves"))
						nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces().remove(workspace)
						workspace.deleteWorkspace()
						workspace = None
						runsDone = runsDone + 1
						print(runsDone, str(ticks), stop1, stop2)
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
					print("restarted")
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
import pandas as pd
for j in range(0,11):
	for i in [10000,12000,13000,14000,15000]:
		for threadCount in [16]:
			print("Runs ", i, "Threads " , threadCount)
			timeTaken = doNRuns(i, threadCount)
			allTimes.append([i,threadCount,timeTaken])
			print(allTimes)
			p = pd.DataFrame(allTimes)
			p.to_csv("AllTimes_WolfSheepPredation.csv")
			try:
				nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces()
			except:
				pass
print(allTimes)
print("DONE____________________________________________________ALL DONE____________________________________________________")
print(allTimes)
print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
