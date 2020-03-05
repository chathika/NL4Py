########Demonstration of NL4Py#################
#This example schedules reporters for 100 ticks or until stop
# for the Wolf Sheep Predation Sample Model
#example usage: python Example2_ScheduledReporters.py netlogo_home
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 
import sys
import pandas as pd
import time
print("\n1) Starting the NetLogoControllerServer with: nl4py.startServer()\n")

nl4py.startServer(sys.argv[1])



print('\n2) Starting the model runs... ')

n = 10

model = "./Wolf Sheep Predation.nlogo"

print('\n2.1) Creating ' + str(n) + ' NetLogo HeadlessWorkspaces with: workspace = nl4py.newNetLogoHeadlessWorkspace()\n and clearing any old workspaces with nl4py.deleteAllHeadlessWorkspaces()')
print('\n2.2) Opening the ' + model + ' model on the NetLogo HeadlessWorkspace with: workspace.openModel("model")')

for i in range(n):
    workspace = nl4py.newNetLogoHeadlessWorkspace()
    workspace.openModel(model)
    print("\n2.3) Setting the parameters to random values with workspace.setParamsRandom()")
    workspace.setParamsRandom()
    workspace.command('set model-version "sheep-wolves-grass"')
    print('\n2.4) Send setup command to model using: workspace.command("setup")')
    print('\n2.4) Schedule reporters to the model to report the ticks passed, the model\'s two stop conditions and number of sheep and wolves for each tick for 100 ticks,\n using: workspace.scheduleReportersAndRun(reporters,0,1,100,"go")')
    print("\t The reporters are: reporters = ['ticks','not any? turtles','not any? wolves and count sheep > max-sheep','count sheep','count wolves']")

reporters = ['ticks','not any? turtles','not any? wolves and count sheep > max-sheep','count sheep','count wolves']
results = pd.DataFrame()
reps = 3

for rep in range(0,reps):
    for workspace in nl4py.getAllHeadlessWorkspaces():
        workspace.command("setup")
        workspace.scheduleReportersAndRun(reporters,0,1,100,"go")
    for idx, workspace in enumerate(nl4py.getAllHeadlessWorkspaces()):
        print('\n2.6) Wait and get back all the results from the scheduling process: result = workspace.awaitScheduledReporterResults():')
        print("\tresults = n.awaitScheduledReporterResults()")
        result = workspace.awaitScheduledReporterResults()
        print(workspace.report("ticks"))
        result = pd.DataFrame(result, columns = reporters)
        result["Workspace"] = idx
        result["Repetition"] = rep
        print(result)
        results = results.append(result)
    
print('\t...and put these results into a pandas dataframe: import pandas as pd \n pd.DataFrame(result)')
results = results.set_index(["Workspace","Repetition"])
print(results)
print(workspace.report("ticks"))
print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')