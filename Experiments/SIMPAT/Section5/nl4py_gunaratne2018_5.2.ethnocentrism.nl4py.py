### This file measures the execution time by NL4Py to run 200 runs of the
### Ethnocentrism.nlogo model for 1000 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.2.1.py "C:/Program Files/NetLogo 6.0.2"
import time
import sys

startTime = int(round(time.time() * 1000))

import nl4py

nl4py.initialize(sys.argv[1])
workspace = nl4py.newNetLogoHeadlessWorkspace()
modelRuns = 10
ticks_to_run = 1000
workspace.openModel("Models/Ethnocentrism.nlogo")

def is_running(workspace):
    ticks = int(float(workspace.report("ticks")))
    return ticks != ticks_to_run

for i in range(0,modelRuns):
    workspace.command("set mutation-rate random-float 1")
    workspace.command("set initial-PTR random-float 1")
    workspace.command("set death-rate random-float 1")
    workspace.command("set cost-of-giving random-float 1")
    workspace.command("set immigrants-per-day random 100")
    workspace.command("set gain-of-receiving random-float 1")
    workspace.command("set immigrant-chance-cooperate-with-same random-float 1")
    workspace.command("set immigrant-chance-cooperate-with-different random-float 1")
    workspace.command("setup-full")
    workspace.command("repeat {} [go]".format(ticks_to_run))
    while is_running(workspace):
        time.sleep(0.001)
    r1 = workspace.report('count turtles with [shape = "circle"]')
    r2 = workspace.report('count turtles with [shape = "circle 2"]')
    r3 = workspace.report('count turtles with [shape = "square"]')
    r4 = workspace.report('count turtles with [shape = "square 2"]')
    
stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
with open("output/5.2_output.csv", "a") as myfile:
        myfile.write('Ethnocentrism,' + str(modelRuns) + ',NL4Py,' + str(totalTime) + '\n')
print(totalTime)
