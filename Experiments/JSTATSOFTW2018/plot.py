import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pylab import plot, draw, savefig, xlim, figure, ylim, legend, boxplot, setp, axes
import os

# function for setting the colors of the box plots pairs
# takes boxplot and color string and hatch pattern
def setBoxColors(bp, color, hatch):
    setp(bp['boxes'], color=color)
    setp(bp['caps'], color='black')
    setp(bp['whiskers'], color=color)
    setp(bp['fliers'], color=color)
    setp(bp['medians'], color='black')
    setp(bp['boxes'],edgecolor='black', linewidth = 1, hatch = hatch)

def readData(filename):
    times = pd.read_csv(filename)
    print(times)
    times['time.ms'] = times['time.ms'] / 1000
    return times
############### 5.1 ################
def plot5_1():
    times = readData("output/5.1_output.csv")
    runs = pd.unique(times['runs'])
    times_1thread = []
    times_4thread = []
    times_8thread = []
    times_16thread = []
    print(runs.sort())
    for r in runs: 
        times_1thread.append(times[(times['threads'] == 1) & (times['runs'] ==r)]['time.ms'].values)
        times_4thread.append(times[(times['threads'] == 4) & (times['runs'] ==r)]['time.ms'].values)
        times_8thread.append(times[(times['threads'] == 8) & (times['runs'] ==r)]['time.ms'].values)
        times_16thread.append(times[(times['threads'] == 16) & (times['runs'] ==r)]['time.ms'].values)
    fig = figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twiny()    
    fig.subplots_adjust(bottom=0.2)
    bp1thread = boxplot(times_1thread, positions = [1,7,13], widths = 0.6, patch_artist=True)#
    setBoxColors(bp1thread, "red", None)
    bp4threads = boxplot(times_4thread, positions = [2,8,14],  widths = 0.6, patch_artist=True)
    setBoxColors(bp4threads, "green", None)
    bp8threads = boxplot(times_8thread, positions = [3,9,15], widths = 0.6, patch_artist=True)
    setBoxColors(bp8threads, "lightblue", None)
    bp16threads = boxplot(times_16thread, positions = [4,10,16], widths = 0.6, patch_artist=True)
    setBoxColors(bp16threads, "purple", None)
    xlim(0,17)
    circ1 = mpatches.Patch( facecolor="red",hatch=None,label='1 thread')
    circ4= mpatches.Patch( facecolor="green",hatch=None,label='4 threads')
    circ8 = mpatches.Patch( facecolor="lightblue",hatch=None,label='8 threads')
    circ16= mpatches.Patch( facecolor="purple",hatch=None,label='16 threads')
    legend(handles = [circ1,circ4,circ8,circ16])
    ax.set_xticks(range(0,18))
    
    ax.set_xticklabels(["","1","4","8","16","","","1","4","8","16","","","1","4","8","16"], size = 9)
    
    new_tick_locations = np.array([2.5, 8.5, 14.5])
    ax2.xaxis.set_ticks_position("bottom")
    ax2.xaxis.set_label_position("bottom")
    ax2.spines["bottom"].set_position(("axes", -0.1))
    ax2.set_frame_on(True)
    ax2.patch.set_visible(False)
    #for sp in ax2.spines.itervalues():
        #sp.set_visible(False)
    ax2.spines["bottom"].set_visible(True)
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(runs)
    fig.text(1,max(times_1thread[0]),"1 thread", ha='center',size = 14, rotation='vertical')
    plt.xlabel("Model Runs")
    plt.ylabel("Execution Time in Seconds")
    fig.text(0.1, 0.157,"Threads", ha='center',size = 10)
    savefig('output/5.1.png')
    os.system("output\\\\5.1.png")
############### 5.2 ################
def plot5_2():
    times = readData("output/5.2_output.csv")
    models = pd.unique(times['connector'])
    models.sort()
    times_fire = []
    times_ethonocentrism = []
    times_wolfsheeppredation = []
    for model in models:
        times_fire.append(times[(times['model'] == "Fire") & (times['connector'] == model)]['time.ms'].values)
        times_ethonocentrism.append(times[(times['model'] == "Ethnocentrism") & (times['connector'] == model)]['time.ms'].values)
        times_wolfsheeppredation.append(times[(times['model'] == "Wolf Sheep Predation") & (times['connector'] == model)]['time.ms'].values)
    fig,axs = plt.subplots(1, 3)
    bpFire = axs[0].boxplot(times_fire, positions = [1,3], widths = 0.6, patch_artist=True)
    setBoxColors(bpFire, "red", None)
    axs[0].set_xticklabels(models)
    axs[0].set_title("Fire")
    bpEthocentrism = axs[1].boxplot(times_ethonocentrism, positions = [1,3],  widths = 0.6, patch_artist=True)
    setBoxColors(bpEthocentrism, "green", None)
    axs[1].set_xticklabels(models)
    axs[1].set_title("Ethnocentrism")
    bpWolfSheepPredation = axs[2].boxplot(times_wolfsheeppredation, positions = [1,3], widths = 0.6, patch_artist=True)
    setBoxColors(bpWolfSheepPredation, "lightblue", None)
    axs[2].set_xticklabels(models)
    axs[2].set_title("Wolf Sheep Predation")
    fig.text(0.5, 0.02,"Connector", ha='center',size = 14)
    fig.text(0.02, 0.5,"Execution Time in Seconds", va='center', rotation='vertical',size = 14)
    fig.set_size_inches(10, 6)
    savefig('output/5.2.png')
    os.system("output\\\\5.2.png")
############### 5.3 ################
def plot5_3():
    times = readData("output/5.3_output.csv")
    runs = pd.unique(times['runs'])
    B = []
    A = []
    for r in runs: 
        A.append(times[(times['connector'] == "pyNetLogo") & (times['runs'] ==r)]['time.ms'].values)
        B.append(times[(times['connector'] == "nl4py") & (times['runs'] ==r)]['time.ms'].values)        
    fig = figure()
    ax = axes()

    bpA = boxplot(A, positions = [1,5,9], widths = 0.6, patch_artist=True)
    setBoxColors(bpA, "lightblue", '\\\\\\\\')
    bpB = boxplot(B,positions = [2,6,10],  widths = 0.6, patch_artist=True)
    setBoxColors(bpB, "red",'////')

    xlim(0,11)
    ax.set_xticklabels(pd.unique(times['runs']))

    hB, = plot([1,1],'b-')
    hR, = plot([1,1],'r-')
    circA = mpatches.Patch( facecolor="lightblue",hatch='\\\\\\\\',label='PyNetLogo on IPCluster')
    circB= mpatches.Patch( facecolor="red",hatch='////',label='NL4Py')

    legend(handles = [circA,circB])
    hB.set_visible(False)
    hR.set_visible(False)
    plt.xlabel("Model Runs")
    plt.ylabel("Execution Time in Seconds")
    savefig('output/5.3.png')
    os.system("output\\\\5.3.png")

