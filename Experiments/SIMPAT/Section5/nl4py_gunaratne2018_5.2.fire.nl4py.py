### This file measures the execution time by NL4Py to run 200 runs of the
### Fire.nlogo model for 100 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.1.1.py "C:/Program Files/NetLogo 6.0.2"

import time
import sys

startTime = int(round(time.time() * 1000))

import nl4py

nl4py.initialize(sys.argv[1])
workspace = nl4py.newNetLogoHeadlessWorkspace()
modelRuns = 100
ticks_to_run = 100
workspace.openModel("Models/Fire.nlogo")
def is_running(workspace): 
    #print("{} {}".format(float(workspace.report("ticks")) ,
    #         str(workspace.report("not any? turtles")).lower()))
    return (float(workspace.report("ticks")) != ticks_to_run 
            and str(workspace.report("not any? turtles")).lower() != "true")

for i in range(0,modelRuns):
    workspace.command("set density random 99")
    workspace.command("setup")
    workspace.command("repeat {} [go]".format(ticks_to_run))
    while is_running(workspace):
        time.sleep(0.001)
    r1 = workspace.report("burned-trees")

stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
with open("output/5.2_output.csv", "a") as myfile:
    myfile.write('Fire,' + str(modelRuns) + ',NL4Py,' + str(totalTime) +  "\n")
print(totalTime)
