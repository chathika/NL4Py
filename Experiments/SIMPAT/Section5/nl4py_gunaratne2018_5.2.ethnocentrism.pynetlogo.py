### This file measures the execution time by PyNetLogo to run 200 runs of the
### Ethnocentrism.nlogo model for 1000 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.2.2.py "C:/Program Files/NetLogo 6.0.2"
import time
import sys

import pyNetLogo

n = pyNetLogo.NetLogoLink(gui=False, netlogo_home = sys.argv[1], netlogo_version = '6.0')
modelRuns = 100
ticks_to_run = 1000
n.load_model(r"Models/Ethnocentrism.nlogo")

def is_running(netlogo): 
    ticks = int(float(netlogo.report("ticks")))
    return ticks != ticks_to_run

for i in range(0,modelRuns):
    n.command("set mutation-rate random-float 1")
    n.command("set initial-PTR random-float 1")
    n.command("set death-rate random-float 1")
    n.command("set cost-of-giving random-float 1")
    n.command("set immigrants-per-day random 100")
    n.command("set gain-of-receiving random-float 1")
    n.command("set immigrant-chance-cooperate-with-same random-float 1")
    n.command("set immigrant-chance-cooperate-with-different random-float 1")
    n.command("setup-full")
    n.command("repeat {} [go]".format(ticks_to_run))
    while is_running(n):
        time.sleep(0.001)
    r1 = n.report('count turtles with [shape = "circle"]')
    r2 = n.report('count turtles with [shape = "circle 2"]')
    r3 = n.report('count turtles with [shape = "square"]')
    r4 = n.report('count turtles with [shape = "square 2"]')
