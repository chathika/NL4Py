import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pylab import plot, draw, savefig, xlim, figure, ylim, legend, boxplot, setp, axes
import os
import seaborn as sns

plt.rcParams.update({'font.size': 20})
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
    times['time.s'] = times['time.ms'] / 1000
    times.loc[:,"connector"] = times.connector.apply(lambda x: "NL4Py" if x == "nl4py" else "pyNetLogo")
    print(times)
    return times
############### 5.1 ################
def plot5_1_1():
    times = pd.read_csv("output/5.1_output.csv")
    times["time.s"] = times["time.ms"] / 1000
    g = sns.catplot(x = "connector", y="time.s", hue = "connector", col = "model", sharey=False, data = times, kind="box")
    g.set_titles("{col_name}").set(ylabel="Time in Seconds", xlabel = "Runs")
    savefig('output/5_1_1.eps')
    os.system(os.path.join("output"."5_1_1.eps"))

def plot5_1_2():
    memory = pd.read_csv("output/5.1_output.csv")
    memory["max.memory.used.GiB"] = memory["max.memory.used.b"] / (1024**3)
    g = sns.catplot(x = "connector", y="max.memory.used.GiB", hue = "connector", col = "model", sharey=False, data = memory, kind="box")
    g.set_titles("{col_name}").set(ylabel="Max Memory Used in GiB", xlabel = "Runs")
    savefig('output/5_1_2.eps')
    os.system(os.path.join("output"."5_1_2.eps"))
############### 5.2 ################
def plot5_2_1():
    times = pd.read_csv("output/5.2_output.csv")
    times["time.s"] = times["time.ms"] / 1000
    times["connector_function"] = times.apply(lambda x: "{} {}".format(x.connector, x.function),axis=1)
    g = sns.FacetGrid(data=times,col="model", hue="connector_function", sharey=False,legend_out=False)
    g = g.map(sns.lineplot,"runs", "time.s",err_style="bars",ci="sd")
    g.set_titles("{col_name}").set(ylabel="Time in Seconds", xlabel = "Runs")#.add_legend(title="Function",loc="lower center")    
    g.fig.legend(labels = times.connector_function.unique(), ncol = 3, title="Function",loc="lower center")
    savefig('output/5_2_1.eps')
    os.system(os.path.join("output"."5_2_1.eps"))

def plot5_2_2():
    memory = pd.read_csv("output/5.2_output.csv")
    memory["max.memory.used.GiB"] = memory["max.memory.used.b"] / (1024**3)
    memory["connector_function"] = memory.apply(lambda x: "{} {}".format(x.connector, x.function),axis=1)
    g = sns.FacetGrid(data=memory,col="model", hue="connector_function", sharey=False)
    g = g.map(sns.lineplot,"runs", "max.memory.used.GiB",err_style="bars",ci="sd")
    g.set_titles("{col_name}").set(ylabel="Max Memory Used in GiB", xlabel = "Runs")#.add_legend(title="Function",loc="lower center")
    g.fig.legend(labels = memory.connector_function.unique(), ncol = 3, title="Function",loc="lower center")
    savefig('output/5_2_2.eps')
    os.system(os.path.join("output"."5_2_2.eps"))