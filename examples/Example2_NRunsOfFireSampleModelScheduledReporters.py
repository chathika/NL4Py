########Demonstration of NL4Py#################
#This example takes two commandline arguments n and model
#n : number of concurrent model runs required.
#model: path to model file
#example usage: python NRunsOfAModel.py 100 netlogo_home
###############################################

if __name__=='__main__':
	print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 
import sys
import multiprocessing

if __name__=='__main__':
	print("\n1) Starting the NetLogoControllerServer with: nl4py.initialize()\n")

nl4py.initialize(sys.argv[2])



print('\n2) Starting the model runs... ')

try:
	n = int(sys.argv[1])
except:
	print("ERROR: Please provide the number of concurrent model runs required as a commandline argument.")

model = "./Fire.nlogo"

if __name__=='__main__':
	print(f'\n2.1 defining init function for {multiprocessing.cpu_count()} sized process pool')
	print('\n2.2) Each process has it\'s own NetLogo HeadlessWorkspaces using create_headless_workspace')
	print(f'\n2.3) Opening copies of the model at {model} on the NetLogo HeadlessWorkspaces with: workspace.open_model("model")')
	print('\n2.4) Define init function with parameters set randomly using set_params_random()  ')
def init(model_path):   
	global workspace
	workspace = nl4py.create_headless_workspace()
	workspace.open_model(model_path)

if __name__=='__main__':
	print('\n2.4) Define simulation function to setup and run simulations on each workspace ')
def run_simulation_fire(runId):
	global workspace
	# Same netlogo commands as used for the NL4Py evaluation
	workspace.command("random-seed " + str(runId))
	workspace.set_params_random()
	workspace.command('setup')
	measures = ['ticks','burned-trees']
	results = workspace.schedule_reporters(measures, stopAtTick=20)
	return results   

if __name__=='__main__':
	names = list(range(n))
	results = []
	print(f'\n2.5) Running {n} simulations on {multiprocessing.cpu_count()} process')
	with multiprocessing.Pool(processes = multiprocessing.cpu_count(), initializer=init, 
		initargs=(model,)) as pool:
		results = []
		for result in pool.map(run_simulation_fire, names):
			results.append(result)
	print(f'There are {len(results)} runs of results:')
	print(results)
	print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')