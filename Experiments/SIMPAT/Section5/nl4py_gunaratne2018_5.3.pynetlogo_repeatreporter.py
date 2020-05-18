import os
import sys, traceback
from multiprocessing import Pool
import multiprocessing
import pyNetLogo

netlogo_path = str(sys.argv[1])
runsNeeded = int(sys.argv[2])
ticksNeeded = int(sys.argv[3])

def initializer(modelfile):
    global netlogo
    netlogo = pyNetLogo.NetLogoLink(gui=False, netlogo_home = netlogo_path, netlogo_version = '6.0')
    netlogo.load_model(modelfile)

def run_simulation(runId):
    # Same netlogo commands as used for the NL4Py evaluation
    netlogo.command("random-seed " + str(runId))
    netlogo.command("set mutation-rate 0.005")
    netlogo.command("set death-rate 0.1")
    netlogo.command("set immigrants-per-day 1")
    netlogo.command("set immigrant-chance-cooperate-with-same 0.5")
    netlogo.command("set immigrant-chance-cooperate-with-different 0.5")
    netlogo.command("set initial-PTR 0.12")
    netlogo.command("set cost-of-giving 0.01")
    netlogo.command("set gain-of-receiving 0.03")
    netlogo.command('setup-empty')
    measures = ['ticks','count turtles']
    results = netlogo.repeat_report(measures, ticksNeeded)
    return results   

if __name__ == '__main__':
    modelfile = os.path.abspath('./Models/Ethnocentrism.nlogo')
    names = list(range(runsNeeded))
    with Pool(multiprocessing.cpu_count(), initializer=initializer, initargs=(modelfile,)) as pool:
        results = []
        for result in pool.map(run_simulation, names):
            results.append(result)