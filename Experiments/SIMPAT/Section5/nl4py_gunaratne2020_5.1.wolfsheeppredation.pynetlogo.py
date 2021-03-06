### This file measures the execution time by NL4Py to run 200 runs of the
### Ethnocentrism.nlogo model for 1000 ticks or until stop condition is met
### To run provide the location of your NetLogo installation as a commandline argument
### Example: >>>python nl4py_gunaratne2018_5.3.2.py "C:/Program Files/NetLogo 6.0.2"
import time
import sys

import pyNetLogo

n = pyNetLogo.NetLogoLink(gui=False, netlogo_home = sys.argv[1], netlogo_version = '6.0')
modelRuns = 100
ticks_to_run = 100
n.load_model(r"Models/Wolf Sheep Predation.nlogo")

def is_running(netlogo): 
    ticks = int(float(netlogo.report("ticks")))
    stop1 = str(netlogo.report("not any? turtles")).lower()  
    stop2 = str(netlogo.report("not any? wolves and count sheep > max-sheep")).lower()  
    return ticks != 100 and stop1 != "true" and stop2 != "true"

for i in range(0,modelRuns):
    n.command("set initial-number-sheep random-float 250")
    n.command("set initial-number-wolves random-float 250")
    n.command("set grass-regrowth-time random-float 100")
    n.command("set sheep-gain-from-food random-float 50")
    n.command("set wolf-gain-from-food random 100")
    n.command("set sheep-reproduce random-float 20")
    n.command("set wolf-reproduce random-float 20")
    n.command("set show-energy? false")
    n.command('set model-version "sheep-wolves-grass"')
    n.command("setup")
    n.command("repeat {} [go]".format(ticks_to_run))
    while is_running(n):
        time.sleep(0.001)
    r1 = n.report('count sheep')
    r2 = n.report('count wolves')

