import os
import sys
import multiprocessing
import nl4py

netlogo_path = os.path.join(str(sys.argv[1]))
runsNeeded = int(sys.argv[2])
ticksNeeded = int(sys.argv[3])
# Replace argument to startServer(...) with the location of your NetLogo installation 

def initializer(modelfile):
    global netlogo
    netlogo = nl4py.newNetLogoHeadlessWorkspace()
    netlogo.openModel(modelfile)

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
    netlogo.scheduleReportersAndRun(measures, stopAtTick=ticksNeeded)
    results = netlogo.awaitScheduledReporterResults()
    return results   

if __name__ == '__main__':
    nl4py.startServer(netlogo_path)
    modelfile = os.path.abspath('./Models/Ethnocentrism.nlogo')
    names = list(range(runsNeeded))
    with multiprocessing.Pool(multiprocessing.cpu_count(), initializer=initializer, initargs=(modelfile,)) as pool:
        results = []
        for result in pool.map(run_simulation, names):
            results.append(result)
    nl4py.stopServer()