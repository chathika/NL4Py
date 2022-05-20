
![Build wheel and Run Unittests](https://github.com/chathika/NL4Py/workflows/Build%20wheel%20and%20Run%20Unittests/badge.svg) ![Run Unittests](https://github.com/chathika/NL4Py/workflows/Run%20Unittests/badge.svg)
## NL4Py

A Python controller interface to NetLogo. NL4Py uses a Remote Procedure Call architecture, allowing Python client code to control NetLogo workspaces on a NetLogoWorkspaceController server. NL4Py supports controlling multiple workspaces through a single Python client. 

Read the NL4Py article is on arXiv: [https://arxiv.org/pdf/1808.03292.pdf](https://www.sciencedirect.com/science/article/pii/S2352711021001035)

[NetLogo with GUI control demo](https://www.youtube.com/watch?v=TXLqbYNYyVg)

NL4Py has been tested Python 3.6.2


### Requirements
* NL4Py works with NetLogo 6.0, 6.1, and 6.2
* NL4Py requires JDK 1.8 
* NL4Py requires [py4j](https://www.py4j.org/) to be installed with your Python distrubtion

### Installation
You can install NL4Py using pip-tools: 
```
pip install nl4py
```

### Usage
To use nl4py in your python code use: 

```python
import nl4py 
```

And start the NetLogoControllerServer with:

```python
nl4py.initialize(netlogo_home : str)
```

Where netlogo_home refers to the top level directory of your NetLogo installation.

#### Examples
1. [Example1](https://github.com/chathika/NL4Py/blob/master/examples/Example1_NRunsOfFireSampleModel.py) : An example of how to run concurrent NetLogo models. To run this example enter the number of desired concurrent runs and the path to your netlogo installation as command line arguments:

```
python Example1_NRunsOfFireSampleModel.py 200 "C:\Program Files\NetLogo 6.0.4"
```

2. [Example2](https://github.com/chathika/NL4Py/blob/master/examples/Example2_NRunsOfFireSampleModelScheduledReporters.py) : An example of how to schedule reporters to return simulation state over a range of ticks at a custom tick interval. To run pass in the path to your netlogo installation as a command line argument:

```
python Example2_ScheduledReporters.py 200 "C:\Program Files\NetLogo 6.0.4"
```

3. [Example3](https://github.com/chathika/NL4Py/blob/master/examples/Example3_NRunsOfFireRunExperiment.py
) : An example of how to run_experiment can be used to easily execute an experiment with parameter variation and return results of multiple reporters. To run pass in the path to your netlogo installation as a command line argument:

```
python Example3_NRunsOfFireRunExperiment.py 20 "C:\Program Files\NetLogo 6.0.4"
```

4. [Example4](https://github.com/chathika/NL4Py/blob/master/examples/Example4_NetLogoGUIAppControl.py
) : An example of how to control the NetLogoGUI. To run pass in the path to your netlogo installation as a command line argument:

```
python Example4_NetLogoGUIAppControl.py "C:\Program Files\NetLogo 6.0.4"
```

Also, see these demo jupyter notebooks:

1. [Parameter Calibration](https://github.com/chathika/NL4Py/blob/master/examples/ParameterCalibrationWithDEAP.ipynb)
2. [Sensitivity Analysis](https://github.com/chathika/NL4Py/blob/master/examples/SensitivityAnalysis.ipynb)

#### Functions
You can create multiple NetLogo HeadlessWorkspaces from Python using the netLogoWorkspaceFactory: 

```python
nl4py.create_headless_workspace() -> nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace
```

The following HeadlessWorkspace functions are available:

```python
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.open_model(self, path : str)
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.close_model(self)
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.command(self, command : str)
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.report(self, reporter : str) -> str
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.schedule_reporters(self, reporters : list, startAtTick : int = 0, 
                                                                      intervalTicks : int = 1, stopAtTick : int = -1, goCommand : str = 'go') -> list
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.set_params_random()
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.get_param_names()
nl4py.NetLogoHeadlessWorkspace.NetLogoHeadlessWorkspace.get_param_ranges()
```

To open the NetLogo application in GUI mode use:

```python
nl4py.netlogo_app() -> nl4py.NetLogoGUI.NetLogoGUI
```

### Referencing:

Please cite as: 
Gunaratne, C., & Garibay, I. (2021). NL4Py: Agent-based modeling in Python with parallelizable NetLogo workspaces. SoftwareX, 16, 100801.

NL4Py is based off of David Masad's [Py2NetLogo](https://github.com/dmasad/Py2NetLogo), available at: https://github.com/dmasad/Py2NetLogo

### Copyright

Copyright (C) 2018 Chathika Gunaratne, Complex Adaptive Systems Lab, University of Central Florida.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.





