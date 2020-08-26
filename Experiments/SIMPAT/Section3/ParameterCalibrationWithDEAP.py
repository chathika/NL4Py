'''
NetLogo calibration with NL4Py and DEAP
In this example we use the DEAP library in combination with NL4Py to calibrate the Wolf Sheep Predation model 
using a simple evolutionary algorithm provided by DEAP. Additionally, both DEAP and NL4Py are parallelized, 
with DEAP EA individuals executing on a thread pool using multiprocessing library and NL4Py NetLogo 
headlessWorkspaces running on Java threads on the NetLogoControllerServer.

In this experiment, we calibrate the model to find the best parameter configuration able to produce a 
near-equilibrium state over the first 1000 simulation ticks of the Wolf Sheep Predation model. 
In other words, the parameters that cause the populations of both wolves and sheep to vary as little as 
possible over the simulation run.
'''

import random
import sys
import time
import os
import pandas as pd
import numpy as np
import multiprocessing

from deap import base, creator, tools, algorithms

import nl4py

netlogo_path = sys.argv[1]
nl4py.initialize(netlogo_path)
model_path = "Models/Wolf Sheep Predation.nlogo"

# In this experiment we intend to maximize fitness. Fitness is the measure of population stability, 
# an indicator of equilibrium in the Wolf Sheep Predation model.
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# An EA Individual is essentially a list of paramter values for our calibration purposes. Through 
# calibration, we intend to find the Individual that produces the highest fitness, or the most
# stable population dynamics.
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
# Use nl4py to find the parameter names and ranges
# Create a HeadlessWorkspace to read in the parameter names and ranges.
n = nl4py.create_headless_workspace()
# Open the model
model_path = "Models/Wolf Sheep Predation.nlogo"
n.open_model(model_path)
# Get the parameter names and ranges.
parameter_names = n.get_param_names()
parameterRanges = n.get_param_ranges()
parameterInitializers = []
# Iterate over the names and ranges and create DEAP initializers for all the parameters of the model
for parameterName, parameterRange in zip(parameter_names, parameterRanges):
    parameterName = ''.join(filter(str.isalnum, str(parameterName)))
    if len(parameterRange) == 3:
        if __name__=="__main__":
            print("Search Space: ")
            print(f'{parameterName} \t\t\t\t min: {str(parameterRange[0])} max: {str(parameterRange[2])} step: {str(parameterRange[1])}')
        toolbox.register(parameterName, random.randrange, parameterRange[0], parameterRange[2], 
            parameterRange[1])
        parameterInitializers.append(eval("toolbox."+str(parameterName)))


# Define the EA "individual" function in the DEAP toolbox which creates an Individual with a list of 
# parameters within the range specified by the NetLogo model interface.
toolbox.register("individual", tools.initCycle, creator.Individual, tuple(parameterInitializers))
# Define the "population" function in the DEAP toolbox
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# Define hyperparameters of the evolutionary algorithm
toolbox.register("mate", tools.cxTwoPoint)
lowerBounds = [row[1] for row in parameterRanges[:-2]]
upperBounds = [row[2] for row in parameterRanges[:-2]]
toolbox.register("mutate", tools.mutUniformInt, low = lowerBounds, up = upperBounds, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
POP = 2

'''
Next, we define a simulation run. This involves:

1. Starting a NetLogoHeadlessWorkspace through NL4Py,
2. Opening the Wolf Sheep Predation model,
3. Setting the parameters to the values of the EA individual,
4. Running the simulation
5. Calculating the metric

We define the metric as the stability of the population counts of the two species, without either going 
into extinction. for this we use first order derivatives per simulation time step and a heavy side 
function to score extinction as 0. High scores indicate more stable populations (closer to complete 
equilibrium). Please see the Sensitivity analysis Jupyter notebook for a mode detailed description 
of this calculation.
'''
def init(model_path):
    global workspace
    workspace = nl4py.create_headless_workspace()
    workspace.open_model(model_path)    

def calculate_population_stability(simulation_results):
    df = pd.DataFrame(simulation_results)
    sheep_pop = pd.to_numeric(df.iloc[:,1])
    wolves_pop = pd.to_numeric(df.iloc[:,2])
    #since time is in simulation ticks, this is the absolute rate of change of sheep population.
    dsheep_dt = sheep_pop.diff().abs()
    #since time is in simulation ticks, this is the absolute rate of change of wolf population.
    dwolves_dt = wolves_pop.diff().abs()   
    #Find population stabilities over time for species as reciprocal of derivatives multiplied by
    # a heavyside function ensuring extinction is scored at 0.
    epsilon = 0.000001
    population_stability_sheep = np.divide(1,(dsheep_dt + epsilon)).mul(np.where(sheep_pop==0,0,1))
    population_stability_wolves = np.divide(1,(dwolves_dt + epsilon)).mul(np.where(wolves_pop==0,0,1))
    #Find total population stability over time as the mean of population stabilities for both species.
    population_stability_total = (population_stability_sheep + population_stability_wolves) / 2
    #the aggregate metric is the mean, total population stability over time
    aggregate_metric = population_stability_total.sum()/len(population_stability_total)
    return aggregate_metric

def evaluate_wolf_sheep_predation(individual):
    '''
    The EA individual evaluation is defined as a simulation run of the model for the parameter values 
    specified and reports the total stability metric of the population.
    
    '''
    global workspace
    for name, value in zip(parameter_names, individual):
        cmd = 'set {0} {1}'.format(name, value)
        workspace.command(cmd)
    workspace.command('set model-version "sheep-wolves-grass"')
    workspace.command('setup')
    simulation_results = workspace.schedule_reporters(["ticks",'count sheep','count wolves'], 0,1,500,"go") 
    aggregate_metric = calculate_population_stability(simulation_results)
    return aggregate_metric,

toolbox.register("evaluate", evaluate_wolf_sheep_predation)
stats = tools.Statistics(key = lambda ind: ind.fitness.values)
stats.register("max",np.max)
stats.register("mean",np.mean)
hof = tools.HallOfFame(1) 

'''
We now define the statistics we are interested in tracking and run the EA with custom hyperparameters.
'''

if __name__=="__main__":
    with multiprocessing.Pool(initializer=init, initargs=(model_path,)) as pool:
        toolbox.register("map", pool.map)
        final_pop, log= algorithms.eaSimple(toolbox.population(n=POP), toolbox, cxpb=0.8, mutpb=0.2, 
                    ngen=2,stats = stats,halloffame = hof)

    print("The best individual over the complete calibration:")
    print(parameter_names)
    print(hof)

    '''
    We can now run and visualize the results...
    '''
    app = nl4py.netlogo_app()
    app.openModel(model_path)
    for name, value in zip(parameter_names, hof[0]):
        app.command('set {0} {1}'.format(name, value))
    app.command("setup")
    app.command("repeat 1000 [ if (count turtles < 10000) [go] ]")
    '''And plot the convergence progress by the EA
    '''
    app.closeModel()
    convergence_progress = pd.DataFrame(log)[['max','mean']]
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib.pyplot import plot
    plot = convergence_progress.plot(legend=True)
    plt.xlabel("Generation", size = 14)
    plt.ylabel("Fitness", size = 14)
    fig = plot.get_figure()
    fig.set_size_inches(9,6)
    fig.savefig("output/CalibrationConvergenceProgress.eps")
    os.system('output\\\\CalibrationConvergenceProgress.eps')
