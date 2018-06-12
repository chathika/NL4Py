########Demonstration of NL4Py#################
#This example takes two commandline arguments n and model
#n : number of concurrent model runs required.
#model: path to model file
#example usage: python NRunsOfAModel.py 100 "/path/to/model.nlogo"
###############################################

import nl4py 
import time
import sys

nl4py.startServer()
n = 200
model = "./Fire.nlogo"
nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces() 
for i in range(0,int(n)):
	n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
	
	
for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
	workspace.openModel(model)
	workspace.setParamsRandom()

for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
	workspace.command("setup")
	workspace.command("repeat 100 [go]")

runningWorkspaces = nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces()
while(len(runningWorkspaces) > 0 ):
	time.sleep(2)	
	for workspace in runningWorkspaces:
		ticksSoFar = int(workspace.report('ticks'))
		stopCondition = workspace.report('not any? turtles')
		if(ticksSoFar == 100 or stopCondition):
			print(str(ticksSoFar) + "," +  str(workspace.report("(burned-trees / (initial-trees + 0.0001))* 100")))
			runningWorkspaces.remove(workspace)
			#workspace.deleteWorkspace()
			
print(nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces())
nl4py.stopServer()

