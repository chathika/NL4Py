from os import environ
import os
import sys
import multiprocessing
import nl4py

netlogo_path = str(sys.argv[1])
model_path = str(sys.argv[2])
runs_needed = int(sys.argv[3])
ticks_needed = int(sys.argv[4])


import time
def ethnocentrism_setup_callback(data):
    # Same netlogo commands as used for the PyNetLogo evaluation
    setup_commands = []
    setup_commands.append("random-seed " + str(data))
    setup_commands.append("set mutation-rate 0.005")
    setup_commands.append("set death-rate 0.1")
    setup_commands.append("set immigrants-per-day 1")
    setup_commands.append("set immigrant-chance-cooperate-with-same 0.5")
    setup_commands.append("set immigrant-chance-cooperate-with-different 0.5")
    setup_commands.append("set initial-PTR 0.12")
    setup_commands.append("set cost-of-giving 0.01")
    setup_commands.append("set gain-of-receiving 0.03")
    setup_commands.append('setup-empty')
    return setup_commands

def run_simulation_fire(runId):
    # Same netlogo commands as used for the PyNetLogo evaluation
    setup_commands = []
    setup_commands.append("random-seed " + str(runId))
    setup_commands.append("set density 57")
    setup_commands.append('setup')
    measures = ['ticks','burned-trees']
    return setup_commands

def run_simulation_ethnocentrism(runId):
    # Same netlogo commands as used for the PyNetLogo evaluation
    setup_commands = []
    setup_commands.append("random-seed " + str(runId))
    setup_commands.append("set mutation-rate 0.005")
    setup_commands.append("set death-rate 0.1")
    setup_commands.append("set immigrants-per-day 1")
    setup_commands.append("set immigrant-chance-cooperate-with-same 0.5")
    setup_commands.append("set immigrant-chance-cooperate-with-different 0.5")
    setup_commands.append("set initial-PTR 0.12")
    setup_commands.append("set cost-of-giving 0.01")
    setup_commands.append("set gain-of-receiving 0.03")
    setup_commands.append('setup-full')
    measures = ['ticks','count turtles with [shape = "circle"]']
    return setup_commands  

def run_simulation_wsp(runId):
    # Same netlogo commands as used for the PyNetLogo evaluation
    setup_commands = []
    setup_commands.append("random-seed " + str(runId))
    setup_commands.append("set model-version \"sheep-wolves\"")
    setup_commands.append("set initial-number-sheep 100")
    setup_commands.append("set initial-number-wolves 50")
    setup_commands.append("set grass-regrowth-time 30")
    setup_commands.append("set sheep-gain-from-food 4")
    setup_commands.append("set wolf-gain-from-food 20")
    setup_commands.append("set sheep-reproduce 4")
    setup_commands.append("set wolf-reproduce 5")
    setup_commands.append('setup')
    measures = ['ticks','count sheep']
    return setup_commands 

def testRunExperiment(model_path,runs_needed,ticks_needed):
    model_path = os.path.join(model_path)
    simulate_function = run_simulation_fire if ("Fire" in model_path) else (
                                run_simulation_ethnocentrism if ("Ethnocentrism" in model_path)
                                    else run_simulation_wsp
                                )
    measures = ['ticks','(burned-trees / initial-trees) * 100'] if ("Fire" in model_path) else (
                                ['ticks','count turtles with [shape = "circle"]'] if ("Ethnocentrism" in model_path)
                                    else ['ticks','count sheep']
                                )
    data = list(range(runs_needed))
    results = nl4py.run_experiment(model_name = model_path, callback=simulate_function,data=data,reporters=measures, start_at_tick=0,interval=1,stop_at_tick=ticks_needed,go_command="go",num_procs=multiprocessing.cpu_count())    
    return results

nl4py.initialize(netlogo_path) 
results = testRunExperiment(model_path,runs_needed,ticks_needed)