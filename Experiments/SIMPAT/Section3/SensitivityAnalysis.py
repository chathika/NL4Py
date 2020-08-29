#Performing Sensitivity Analysis with NL4Py
'''
In this experiment, we perform sensitivity analysis using SALib on the Wolf Sheep Predation model via NL4Py. Two sensitivity analysis techniques are used, Sobol with Saltelli sampling and FAST as described in the article "NL4Py: Agent-Based Modeling in Python with Parallelizable NetLogo Workspaces" and results are compared. Additionally, SALib is run in parallel to improve performance and NetLogo HeadlessWorkspaces are run in parallel as well as Java threads on NL4Py's NetLogoControllerServer.

Start the NetLogoControllerServer
'''
import nl4py
import sys
import os
import multiprocessing

from matplotlib import pyplot
import pandas as pd
import numpy as np
from matplotlib.pyplot import draw
from SALib.sample import saltelli
from SALib.analyze import sobol


#Start the NetLogoControllerServer
netlogo_path = sys.argv[1]
nl4py.initialize(netlogo_path)
model_path = "Models/Wolf Sheep Predation.nlogo"

'''
Since the number of runs required would most likely far exceed the number of cores available, we define a function that makes sure we only run a number parallel NetLogoHeadlessWorkspaces equal to the number of cores on the machine for optimal performance.

We then iterate through the entire set of parameter configurations sampled from the product space and execute simulate(...) accordingly. The simulation output is obtained and aggregated into a final metric.

In this experiment, we target population equilibrium (May, 1974). To quantify equilibrium we find the population_stability as the reciprocal of the derivatives of both populations over simulation time. The resulting population_stabilities are passed through a heavyside function to give a score of zero if populations that are equal to 0, (equilibria can exist both at extinction in addition to populations > 0). The population_stability_total is found as the mean population_stability over time between both species. Finally, the aggregate_metric scoring the simulation run is calculated as the mean population_stability_total over time.
'''
def init(model_path):
    global workspace
    workspace = nl4py.create_headless_workspace()
    workspace.open_model(model_path)    

def calculate_population_stability(simulation_results):
    ###Process simulation results###
    df = pd.DataFrame(simulation_results)
    sheep_pop = pd.to_numeric(df.iloc[:,1])
    wolves_pop = pd.to_numeric(df.iloc[:,2])
    #since time is in simulation ticks, this is the absolute rate of change of sheep population.
    dsheep_dt = sheep_pop.diff().abs()
    #since time is in simulation ticks, this is the absolute rate of change of wolf population.
    dwolves_dt = wolves_pop.diff().abs()   
    #Find population stabilities over time for species as reciprocal of derivatives multiplied by
    # a heavyside function ensuring extinction is scored at 0.
    population_stability_sheep = np.divide(1,(dsheep_dt + 0.000001)).mul(np.where(sheep_pop==0,0,1))
    population_stability_wolves = np.divide(1,(dwolves_dt + 0.000001)).mul(np.where(wolves_pop==0,0,1))
    #Find total population stability over time as the mean of population stabilities for both species.
    population_stability_total = (population_stability_sheep + population_stability_wolves) / 2
    #the aggregate metric is the mean, total population stability over time
    aggregate_metric = population_stability_total.sum()/len(population_stability_total)
    return aggregate_metric

def runForParameters(simulation_parameters):
    '''
    Define what a simulation is. In this experiment, a simulation run is initialized with a parameter configuration, resets the model and runs it for 100 ticks. We perform the sensitivity analysis on the sheep, wolves, and grass version of the Wolf Sheep Predation model. We track the sheep and wolf populations over time as model output.
    '''
    global workspace

    workspace.command("stop")
    for i, name in enumerate(problem['names']):
        if name == 'random-seed':
            workspace.command('random-seed {}'.format(simulation_parameters[i]))
        else:
            workspace.command('set {0} {1}'.format(name, simulation_parameters[i]))
    workspace.command('set model-version "sheep-wolves-grass"')
    workspace.command('set initial-number-sheep 100')
    workspace.command('set initial-number-wolves 100')
    workspace.command('setup')
    newResults = workspace.schedule_reporters(["ticks",'count sheep','count wolves'], 0,1,500,"go") 
    aggregate_metric = calculate_population_stability(newResults)
    return aggregate_metric


'''
Next, we use NL4Py to read in the parameters from the NetLogo model's interface and populate the problem space, required by SALib for sensitivity analysis, with both the names and ranges, automatically.
'''
ws = nl4py.create_headless_workspace()
ws.open_model(model_path)
#Read in the parameter info with NL4Py functions and generate a SALib problem
problem = { 
  'num_vars': 6,
  'names': ['random-seed'],
  'bounds': [[1, 100000]] 
}
problem['names'].extend(ws.get_param_names()[:-2])
problem['bounds'].extend( [item[0::2] for item in ws.get_param_ranges()[:-2]])
#Remove the initial conditions from the problem space. These are set to fixed values in the simulate function
del problem['bounds'][problem['names'].index("initial-number-wolves")]
problem['names'].remove("initial-number-wolves")
del problem['bounds'][problem['names'].index("initial-number-sheep")]
problem['names'].remove("initial-number-sheep")
print("Problem parameter space: ")
print(problem)

'''
The simulation experiment is now defined. We can now run sensitivity analysis using techniques of our choice. We choose to use SALib.

First, we perform Sobol's sensitivity analysis using Saltelli's sampling sequence technique. (Sobol 2001),(Saltelli 2002),(Saltelli et al. 2010)
'''

print("\nPerforming Sobol sensitivity analysis with Saltelli sampling... \n")
if __name__ == '__main__':
    firstOrderSobol = np.array([])
    totalSobol = np.array([])
    sampleSizes = range(500, 1501, 500 )
    for sampleSize in sampleSizes:
        param_values_sobol = saltelli.sample(problem, sampleSize)
        with multiprocessing.Pool(initializer=init, initargs=(model_path,)) as pool:
            Y = np.array(pool.map(runForParameters, param_values_sobol))
        print(Y)
        print("\n")
        Si_Sobol = sobol.analyze(problem, Y, print_to_console=True)#, parallel=True, n_processors=multiprocessing.cpu_count())
        #Get the absolute values of the first order sobol sensitivity indices
        sobol_s1_abs = np.abs(Si_Sobol["S1"])
        #The residual of the first order sensitivity indicies represents the sensitivity caused by 
        # higher order interactions of the parameters
        S1_and_interactions_sobol = np.append(sobol_s1_abs,(1 - sobol_s1_abs.sum()))                                                
        firstOrderSobol = np.append(firstOrderSobol, S1_and_interactions_sobol)
        totalSobol = np.append(totalSobol, np.array(Si_Sobol["ST"]))

    '''
    Plot the first order Sobol sensitivity indices
    '''
    labels = np.append(problem['names'],'Interactions')
    fig = pyplot.figure(figsize=[8, 6])
    ax = fig.add_subplot(111)
    yS1 = firstOrderSobol.reshape(int(firstOrderSobol.shape[0]/len(sampleSizes)),len(sampleSizes), order='F')
    ax.stackplot(sampleSizes, yS1, labels = labels)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),  ncol=3, fancybox=True, shadow=True, fontsize = 11)
    pyplot.xticks(fontsize=18)
    pyplot.xlabel("Number of Samples", fontsize = 18)
    pyplot.yticks(fontsize=18)
    pyplot.ylabel("S1", fontsize = 18)
    pyplot.xticks(sampleSizes)
    draw()
    fig.savefig('output/SobolWSPS1.eps')
    os.system('output\\\\SobolWSPS1.eps')

    '''
    Plot the Sobol Total sensitivities to higher order interactions of parameters
    '''
    yST = totalSobol.reshape(int(totalSobol.shape[0]/len(sampleSizes)),len(sampleSizes), order='F')
    for col in range(0,yST.shape[1]):
        yST[:,col] = yST[:,col]/yST[:,col].sum()

    fig = pyplot.figure(figsize=[8, 6])
    ax = fig.add_subplot(111)
    ax.stackplot(sampleSizes, yST, labels = labels)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),  ncol=3, fancybox=True, shadow=True, fontsize = 11)
    pyplot.xticks(fontsize=18)
    pyplot.xlabel("Number of Samples", fontsize = 18)
    pyplot.yticks(fontsize=18)
    pyplot.ylabel("Relative ST", fontsize = 18)
    pyplot.xticks(sampleSizes)
    draw()
    fig.savefig('output/SobolWSPST.eps')
    os.system('output\\\\SobolWSPST.eps')


    '''
    Next, run the Fourier Amplitude Sensitivity Test (FAST) sampling and sensitivity analysis technique (Cukier et al., 1973), (Saltelli et al., 1999).
    ''''''
    print("\nPerforming Fourier Amplitude Sensitivity Test..\n")
    from SALib.analyze import fast
    from SALib.sample import fast_sampler

    firstOrderFast = np.array([])
    totalFast = np.array([])

    for sampleSize in sampleSizes:
        nl4py.deleteAllHeadlessWorkspaces()
        param_values_fast = fast_sampler.sample(problem, sampleSize)
        Y_FAST = np.array(runForParameters(param_values_fast))  
        print("\n")
        Si_FAST = fast.analyze(problem, Y_FAST, print_to_console=True)
        S1_and_interactions_fast = np.append(np.array(Si_FAST["S1"]),(1 - np.array(Si_FAST["S1"]).sum()))
        firstOrderFast = np.append(firstOrderFast, S1_and_interactions_fast)
        totalFast = np.append(totalFast, np.array(Si_FAST["ST"]))

    ''''''
    Plot the first order FAST sensitivity indices
    ''''''
    labels = np.append(problem['names'],'Interactions')
    fig = pyplot.figure(figsize=[8, 6])
    ax = fig.add_subplot(111)
    yFS1 = firstOrderFast.reshape(int(firstOrderFast.shape[0]/len(sampleSizes)),len(sampleSizes), order='F')
    ax.stackplot(sampleSizes, yFS1, labels = labels)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),  ncol=3, fancybox=True, shadow=True, fontsize = 11)
    pyplot.xticks(fontsize=18)
    pyplot.xlabel("Number of Samples", fontsize = 18)
    pyplot.yticks(fontsize=18)
    pyplot.ylabel("S1", fontsize = 18)
    pyplot.xticks(sampleSizes)
    draw()
    fig.savefig('output/FASTWSPS1.eps')
    os.system('output\\\\FASTWSPS1.eps')

    ''''''
    Plot the FAST Total sensitivities to higher order interactions of parameters
    ''''''
    yFST = totalFast.reshape(int(totalFast.shape[0]/len(sampleSizes)),len(sampleSizes), order='F')
    for col in range(0,yFST.shape[1]):
        yFST[:,col] = yFST[:,col]/yFST[:,col].sum()

    fig = pyplot.figure(figsize=[8, 6])
    ax = fig.add_subplot(111)
    ax.stackplot(sampleSizes, yFST, labels = labels)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),  ncol=3, fancybox=True, shadow=True, fontsize = 11)
    pyplot.xticks(fontsize=18)
    pyplot.xlabel("Number of Samples", fontsize = 18)
    pyplot.yticks(fontsize=18)
    pyplot.ylabel("Relative ST", fontsize = 18)
    pyplot.xticks(sampleSizes)
    draw()
    fig.savefig('output/FASTWSPST.eps')
    os.system('output\\\\FASTWSPST.eps')
    '''