
'''
code follows that on https://pynetlogo.readthedocs.io/en/latest/_docs/SALib_multiprocessing.html#Running-the-experiments-in-parallel-using-a-Process-Pool
as accessed on 18th May. 2020
'''
import os
import sys
import multiprocessing
import pyNetLogo

netlogo_path = str(sys.argv[1])
model_path = str(sys.argv[2])
runs_needed = int(sys.argv[3])
ticks_needed = int(sys.argv[4])

def initializer(model_path):
    global netlogo
    netlogo = pyNetLogo.NetLogoLink(gui=False, netlogo_home = netlogo_path, netlogo_version = '6.0')
    netlogo.load_model(model_path)

def run_simulation_fire(runId):
    # Same netlogo commands as used for the NL4Py evaluation
    netlogo.command("random-seed " + str(runId))
    netlogo.command("set density 57")
    netlogo.command('setup')
    measures = ['ticks','burned-trees']
    results = netlogo.repeat_report(measures, ticks_needed)
    return results   

def run_simulation_ethnocentrism(runId):
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
    netlogo.command('setup-full')
    measures = ['ticks','count turtles']
    results = netlogo.repeat_report(measures, ticks_needed)
    return results   

def run_simulation_wsp(runId):
    # Same netlogo commands as used for the NL4Py evaluation
    netlogo.command("random-seed " + str(runId))
    netlogo.command("set model-version \"sheep-wolves\"")
    netlogo.command("set initial-number-sheep 100")
    netlogo.command("set initial-number-wolves 50")
    netlogo.command("set grass-regrowth-time 30")
    netlogo.command("set sheep-gain-from-food 4")
    netlogo.command("set wolf-gain-from-food 20")
    netlogo.command("set sheep-reproduce 4")
    netlogo.command("set wolf-reproduce 5")
    netlogo.command('setup')
    measures = ['ticks','count sheep']
    results = netlogo.repeat_report(measures, ticks_needed)
    return results   

if __name__ == '__main__':
    model_path = os.path.abspath(model_path)
    names = list(range(runs_needed))
    with multiprocessing.Pool(multiprocessing.cpu_count(), initializer=initializer, initargs=(model_path,)) as pool:
        results = []
        simulate_function = run_simulation_fire if ("Fire" in model_path) else (
                                run_simulation_ethnocentrism if ("Ethnocentrism" in model_path)
                                    else run_simulation_wsp
                                )
        for result in pool.map(simulate_function, names):
            results.append(result)