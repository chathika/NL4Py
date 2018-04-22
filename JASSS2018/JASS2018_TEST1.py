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


def doNRuns(n):
	model = "./Fire.nlogo"
	nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces() 
	startTime = int(round(time.time() * 1000))

	for i in range(0,int(n)):
		n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
		n.openModel(model)
		

	for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
		workspace.setParamsRandom()


	for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
		workspace.command("setup")
		workspace.command("go")
	result = []
	for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
		result.append(workspace.report("burned-trees"))
	stopTime = int(round(time.time() * 1000))

	totalTime = stopTime - startTime
	print(result)
	return totalTime
print("\n1) Starting the NetLogoControllerServer with: nl4py.startServer()\n")
nl4py.startServer()

allTimes = []
for i in range(1,5):
	timeTaken = doNRuns(math.pow(10,i))
	allTimes.append(timeTaken)

print("DONE____________________________________________________ALL DONE____________________________________________________")
print(allTimes)
	
print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
