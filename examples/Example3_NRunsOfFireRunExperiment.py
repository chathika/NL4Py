########Demonstration of NL4Py#################
#This example takes two commandline arguments n and model
#n : number of concurrent model runs required.
#model: path to model file
#example usage: python NRunsOfAModel.py 100 netlogo_home
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 
import sys
import multiprocessing

print("\n1) Starting the NetLogoControllerServer with: nl4py.initialize()\n")

nl4py.initialize(sys.argv[2])

print('\n2) Starting the model runs... ')

try:
	n = int(sys.argv[1])
except:
	print("ERROR: Please provide the number of concurrent model runs required as a commandline argument.")

model = "./Fire.nlogo"

print('\n2.1) Define simulation setup function')
def run_simulation_fire(runId):
	setup_commands = [f"random-seed {runId}","setup"]
	return setup_commands

reporters = ['ticks','burned-trees']

print(f'\n2.2 use run_experiment to run {n} simulations of Fire model and return results')
results = nl4py.run_experiment(model, run_simulation_fire, list(range(n)),reporters,stop_at_tick=10)
print(f'There are {len(results)} runs of results:')
print(results)
print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')