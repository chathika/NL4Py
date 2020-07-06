### This file measures the execution time by NL4Py to run 200 runs of the
### Wolf Sheep Predation.nlogo model for 100 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.3.1.py "C:/Program Files/NetLogo 6.0.2"
import time
import sys

import nl4py

nl4py.initialize(sys.argv[1])
workspace = nl4py.newNetLogoHeadlessWorkspace()
modelRuns = 100
ticks_to_run = 100
workspace.openModel("Models/Wolf Sheep Predation.nlogo")

def is_running(workspace):
    ticks = int(float(workspace.report("ticks")))
    stop1 = str(workspace.report("not any? turtles")).lower()  
    stop2 = str(workspace.report("not any? wolves and count sheep > max-sheep")).lower()  
    return ticks != ticks_to_run and stop1 != "true" and stop2 != "true"

for i in range(0,modelRuns):
    workspace.command("set initial-number-sheep random-float 250")
    workspace.command("set initial-number-wolves random-float 250")
    workspace.command("set grass-regrowth-time random-float 100")
    workspace.command("set sheep-gain-from-food random-float 50")
    workspace.command("set wolf-gain-from-food random 100")
    workspace.command("set sheep-reproduce random-float 20")
    workspace.command("set wolf-reproduce random-float 20")
    workspace.command("set show-energy? false")
    workspace.command('set model-version "sheep-wolves-grass"')
    workspace.command("setup")
    workspace.command("repeat {} [go]".format(ticks_to_run))
    while is_running(workspace):
        time.sleep(0.001)
    r1 = workspace.report('count sheep')
    r2 = workspace.report('count wolves')
