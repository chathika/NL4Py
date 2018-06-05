This supplement contains the code used to generate results for "NL4Py: Agent-Based Modeling in Python with Parallelizable NetLogo Workspaces"

## Requirements

The general requirements to run NL4Py are:
* System must have JDK install and path to java bin included in environment variables. JDK 1.8 is recommended.
* System must have Python 2.7 or higher or Python 3.6 higher installed. Please make sure pip tools is installed with Python.
* System must have NetLogo 6.0.2 or higher installed.

NL4Py may work with previous versions of NetLogo but has not been officially tested with versions prior to 6.0.2.

Additionally, some of the experiments in the article require:
* Anaconda (tested with version 1.6) and Jupyter notebook ( tested with version 5.0.0). Jupyter notebook is opened through the Anaconda navigator and can be used with either version of Python as described above.

## Instructions

Section 3 and Section 5 contain results from the code samples included here.

### Section 3

In Section 3 we describe two applications of NL4Py important for statistical analysis of agent-based model output, sensitivity analysis and parameter calibration. We perform these methods on the Wolf Sheep Predation model, from the sample models collection in the NetLogo examples library. 

#### Sensitivity analysis

This code is completely availabe in a Jupyter notebook under the path Section3\SensitivityAnalysis.ipynb

#### Paramter calibration

This code is completely availabe in a Jupyter notebook under the path Section3\ParameterCalibration.ipynb

### Section 5

In Section 5 of the article we present results for execution time comparisons of NL4Py under different thread configurations and results for execution time comparisons between NL4Py, PyNetLogo, and PyNetLogo in combination with IPyParallel (as demonstrated by []).

#### Thread count comparison

In order to run the thread count comparisons

#### NL4Py vs PyNetLogo execution time comparison

#### NL4Py vs PyNetLogo on IPyParallel cluster execution time comparison

Here we compare the execution time of NL4Py's scheduled reporters against the PyNetLogo equivalent, repeat_reporter. This code is split across two Jupyter Notebooks. 
In order to run the NL4Py execution time measurement experiments open and run the following Jupyter notebook through Anaconda:
(nl4py_gunaratne2018_5.3.nl4py_scheduledreporters.ipynb)[./section5/nl4py_gunaratne2018_5.3.nl4py_scheduledreporters.ipynb]
In order to run the PyNetLogo on IPyParallel cluster execution time measurement experiments open and run the following Jupyter notebook through Anaconda:
(nl4py_gunaratne2018_5.3.pynetlogo_repeatreporter.ipynb)[./section5/nl4py_gunaratne2018_5.3.pynetlogo_repeatreporter.ipynb]
