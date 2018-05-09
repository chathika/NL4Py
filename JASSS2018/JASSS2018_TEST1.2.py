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
def runModel(workspace_):
	workspace_.command('stop')
	workspace_.command('set initial-number-sheep random 250')
	workspace_.command('set initial-number-wolves random 250')
	workspace_.command('set grass-regrowth-time random 100')
	workspace_.command('set sheep-gain-from-food random 50')
	workspace_.command('set wolf-gain-from-food random 100')
	workspace_.command('set sheep-reproduce (random 20) + 1')
	workspace_.command('set wolf-reproduce random 20')
	workspace_.command('set model-version "sheep-wolves-grass"') # make sure we run the right version of the model 
	reporters = ["ticks", "not any? turtles", "not any? wolves and count sheep > max-sheep", "count sheep", "count wolves"]
	workspace_.command("setup")
	workspace_.scheduleReportersAndRun(reporters, 0,1,100, "go")
def doNRuns(runsNeeded, threadCount_):
	model = "./Wolf Sheep Predation.nlogo"
	startTime = int(round(time.time() * 1000))
	runsDone = 0
	wolfsheepcounts = []
	workspacesRunning = []
	threadCount = threadCount_
	runningWorkspacesCount = int(runsNeeded - runsDone if (runsNeeded - runsDone) <= threadCount else threadCount)
	for i in range(0,int(runningWorkspacesCount)):
		n = nl4py.newNetLogoHeadlessWorkspace()
	for workspace in nl4py.getAllHeadlessWorkspaces():
		workspace.openModel(model)
		runModel(workspace)
	runsStarted = len(nl4py.getAllHeadlessWorkspaces())
	while(runsDone != runsNeeded):
		for workspace in nl4py.getAllHeadlessWorkspaces():
			workspaceResults = workspace.getScheduledReporterResults()
			if len(workspaceResults) > 0:
				ticks = int(float(workspaceResults[-1][0]))
				stop1 = str(workspaceResults[-1][1]).lower() == "true"
				stop2 = str(workspaceResults[-1][2]).lower() == "true"
				if (ticks == 100) or stop1 or stop2:
					wolfsheepcounts.append(workspaceResults)
					runsDone = runsDone + 1
					if(runsDone == runsNeeded):
						break
					if(runsStarted != runsNeeded):
						runsStarted = runsStarted + 1
						runModel(workspace)
	stopTime = int(round(time.time() * 1000))
	totalTime = stopTime - startTime
	print(totalTime)
	return totalTime
print("\n1 Starting the NetLogoControllerServer with: nl4py.startServer()\n")
nl4py.startServer()
time.sleep(2)
allTimes = []
import pandas as pd
for j in range(0,11):
	for i in [100]:
		for threadCount in [8]:
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
