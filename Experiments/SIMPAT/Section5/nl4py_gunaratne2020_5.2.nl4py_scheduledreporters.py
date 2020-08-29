import os
import sys
import multiprocessing
import nl4py

netlogo_path = str(sys.argv[1])
model_path = str(sys.argv[2])
runs_needed = int(sys.argv[3])
ticks_needed = int(sys.argv[4])
nl4py.initialize(netlogo_path)

def init(model_path):   
    global netlogo
    netlogo = nl4py.create_headless_workspace()
    netlogo.open_model(model_path)
    
def run_simulation_fire(runId):
    global netlogo
    # Same netlogo commands as used for the NL4Py evaluation
    netlogo.command("random-seed " + str(runId))
    netlogo.command("set dddddensity 57")
    netlogo.command('setup')
    measures = ['ticks','burned-trees']
    results = netlogo.schedule_reporters(measures, stopAtTick=ticks_needed)
    return results   

def run_simulation_ethnocentrism(runId):
    global netlogo
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
    measures = ['ticks',"count turtles with [shape = \"circle\"]"]
    results = netlogo.schedule_reporters(measures, stopAtTick=ticks_needed)
    return results   

def run_simulation_wsp(runId):
    global netlogo
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
    results = netlogo.schedule_reporters(measures, stopAtTick=ticks_needed)
    return results   

if __name__ == '__main__':     
    
    model_path = os.path.join(model_path)
    names = list(range(runs_needed))
    with multiprocessing.Pool(initializer=init, initargs=(model_path,)) as pool:
        results = []
        simulate_function = run_simulation_fire if ("Fire" in model_path) else (
                                run_simulation_ethnocentrism if ("Ethnocentrism" in model_path)
                                    else run_simulation_wsp
                                )
        for result in pool.map(simulate_function, names):
            results.append(result)
