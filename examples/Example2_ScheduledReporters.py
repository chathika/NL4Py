########Demonstration of NL4Py#################
#This example schedules reporters for 100 ticks or until stop
# for the Wolf Sheep Predation Sample Model
#example usage: python Example2_ScheduledReporters.py
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 

print("\n1) Starting the NetLogoControllerServer with: nl4py.startServer()\n")

nl4py.startServer()

import sys

print('\n2) Starting the model runs... ')

n = 1

model = "./Wolf Sheep Predation.nlogo"

print('\n2.1) Creating ' + str(n) + ' NetLogo HeadlessWorkspaces with: nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()\n and clearing any old workspaces with nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces()')
print('\n2.2) Opening the ' + model + ' model on the NetLogo HeadlessWorkspace with: nl4py.NetLogoHeadlessWorkspace.openModel("model")')
nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces() 
n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
n.openModel(model)

print("\n2.3) Setting the parameters to random values with nl4py.NetLogoHeadlessWorkspace.setParamsRandom()")

n.setParamsRandom()

print('\n2.4) Send setup command to model using: nl4py.NetLogo_HeadlessWorkspace.command("setup")')

n.command("setup")

print('\n2.4) Schedule reporters to the model to report the number of sheep and wolves for each tick and their mean positions for 100 ticks,\n using: n.scheduleReportersAndRun(reporters,0,1,100,"go")')
print("\t The reporters are: reporters = ['ticks','count sheep','count wolves','mean [xcor] of sheep','mean [ycor] of sheep','mean [xcor] of wolves','mean [ycor] of wolves']")

reporters = ['ticks','count sheep','count wolves','mean [xcor] of sheep','mean [ycor] of sheep','mean [xcor] of wolves','mean [ycor] of wolves']
n.scheduleReportersAndRun(reporters,0,1,100,"go")

print("\n2.5) Periodically check the number of ticks passed and if the ticks haven't changed, close the model:")
print("ticksSoFar = n.report('ticks')\nwhile(ticksSoFar < 100 or n.report('ticks') != ticksSoFar ): ")
print("\ttime.sleep(2)")
print("\tticksSoFar = n.report('ticks')")
print("n.closeModel()")

import time
time.sleep(2) #give the workspace a second to run the commands
ticksSoFar = n.report('ticks')
while(ticksSoFar < 100 ):	
	print(n.report('ticks'))
	ticksSoFar = n.report('ticks')
	time.sleep(2)
	if(n.report('ticks') == ticksSoFar):
		#n.closeModel()
		break
print('\n2.6) Get back all the results from the scheduling process: result = n.getScheduledReporterResults()')
print('\t and put these results into a pandas dataframe: import pandas as pd \n pd.DataFrame(result)')

result = n.getScheduledReporterResults()
import pandas as pd
resultframe = pd.DataFrame(result)

print(resultframe)

print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')