### This file measures the execution time by NL4Py to run 200 runs of the
### Ethnocentrism.nlogo model for 1000 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.2.1.py "C:/Program Files/NetLogo 6.0.2"
import time
startTime = int(round(time.time() * 1000))
import nl4py
import sys
nl4py.startServer(sys.argv[1])
workspaces = []
modelRuns = 200
for i in range(0,modelRuns):
    n = nl4py.newNetLogoHeadlessWorkspace()
    n.openModel("Models/Ethnocentrism.nlogo")
    n.command("set mutation-rate random-float 1")
    n.command("set initial-PTR random-float 1")
    n.command("set death-rate random-float 1")
    n.command("set cost-of-giving random-float 1")
    n.command("set immigrants-per-day random 100")
    n.command("set gain-of-receiving random-float 1")
    n.command("set immigrant-chance-cooperate-with-same random-float 1")
    n.command("set immigrant-chance-cooperate-with-different random-float 1")
    n.command("setup-full")
    n.command("repeat 1000 [go]")
    workspaces.append(n)
while len(workspaces) > 0:
    for workspace in workspaces:
        #Check if workspaces are stopped
        ticks = int(float(workspace.report("ticks")))
        if ticks == 1000:
            r1 = workspace.report('count turtles with [shape = "circle"]')
            r2 = workspace.report('count turtles with [shape = "circle 2"]')
            r3 = workspace.report('count turtles with [shape = "square"]')
            r4 = workspace.report('count turtles with [shape = "square 2"]')
            print(str(modelRuns - len(workspaces))+" "+str(r1)+" "+str(r2)+" "+str(r3)+" "+str(r4)+" "+str(ticks))
            workspaces.remove(workspace)
stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
print(totalTime)
with open("output/5.2_output.csv", "a") as myfile:
        myfile.write('Ethnocentrism,' + str(modelRuns) + ',NL4Py,' + str(totalTime) + '\n')
nl4py.stopServer()
