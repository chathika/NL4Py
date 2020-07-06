### This file measures the execution time by PyNetLogo to run 200 runs of the
### Fire.nlogo model for 100 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.1.2.py "C:/Program Files/NetLogo 6.0.2"
import time
import sys

import pyNetLogo

n = pyNetLogo.NetLogoLink(gui=False, netlogo_home = sys.argv[1], netlogo_version = '6.0')
modelRuns = 100
ticks_to_run = 100
n.load_model(r"Models/Fire.nlogo")
def is_running(netlogo): 
    return (float(netlogo.report("ticks")) != ticks_to_run 
            and str(netlogo.report("not any? turtles")).lower() != "true")

for i in range(0,modelRuns):    
    n.command("set density random 99")
    n.command("setup")
    n.command("repeat {} [go]".format(ticks_to_run))
    while is_running(n):
        time.sleep(0.001)
    r1 = n.report("burned-trees")

