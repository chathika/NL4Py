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

print('\n2.1) Creating ' + str(n) + ' NetLogo HeadlessWorkspaces with: nl4py.newNetLogoHeadlessWorkspace()\n and clearing any old workspaces with nl4py.deleteAllExistingWorkspaces()')
print('\n2.2) Opening the ' + model + ' model on the NetLogo HeadlessWorkspace with: nl4py.NetLogoHeadlessWorkspace.openModel("model")')
nl4py.deleteAllHeadlessWorkspaces() 
n = nl4py.newNetLogoHeadlessWorkspace()
n.openModel(model)

print("\n2.3) Setting the parameters to random values with nl4py.NetLogoHeadlessWorkspace.setParamsRandom()")

n.setParamsRandom()
n.command('set model-version "sheep-wolves-grass"')
print('\n2.4) Send setup command to model using: nl4py.NetLogoHeadlessWorkspace.command("setup")')

n.command("setup")

print('\n2.4) Schedule reporters to the model to report the number of sheep and wolves for each tick and their mean positions for 100 ticks,\n using: n.scheduleReportersAndRun(reporters,0,1,100,"go")')
print("\t The reporters are: reporters = ['ticks','count sheep','count wolves','mean [xcor] of sheep','mean [ycor] of sheep','mean [xcor] of wolves','mean [ycor] of wolves']")

reporters = ['ticks','not any? turtles','not any? wolves and count sheep > max-sheep','count sheep','count wolves']#,'mean [xcor] of sheep','mean [ycor] of sheep','mean [xcor] of wolves','mean [ycor] of wolves']
n.scheduleReportersAndRun(reporters,0,1,100,"go")

print("\n2.5) Periodically check the number of ticks passed and if the ticks haven't changed, close the model:")
print("ticksSoFar = n.report('ticks')\nwhile(ticksSoFar < 100 or n.report('ticks') != ticksSoFar ): ")
print("\ttime.sleep(2)")
print("\tticksSoFar = n.report('ticks')")
print("n.closeModel()")

import time
time.sleep(2) #give the workspace a second to run the commands
ticksSoFar = 0
results = []
while(ticksSoFar < 100 ):
	moreResults = n.getScheduledReporterResults()	
	if moreResults.size > 0:
		results.extend(moreResults)
	ticksSoFar = int(float(results[-1][0]))
	stop1 = str(results[-1][1]).lower()
	stop2 = str(results[-1][2]).lower()
	print(ticksSoFar)
	if ticksSoFar == 100 or stop1 == "true" or stop2 == "true":
		break;
print('\n2.6) Get back all the results from the scheduling process: result = n.getScheduledReporterResults()')
print('\t and put these results into a pandas dataframe: import pandas as pd \n pd.DataFrame(result)')
import pandas as pd
resultframe = pd.DataFrame(results)
resultframe.columns = ['ticks','stop1','stop2','sheep','wolves']#,'mean_x_sheep','mean_y_sheep','mean_x_wolves','mean_y_wolves']
print(resultframe)

print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')