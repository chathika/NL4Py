## NL4Py

A Python controller interface to NetLogo. NL4Py uses a Remote Procedure Call architecture, allowing Python client code to control NetLogo workspaces on a NetLogoWorkspaceController server. NL4Py supports controlling multiple workspaces through a single Python client. 

NetLogo with GUI is now supported with NL4Py v0.3.0!

**New: Changes to the NL4Py API have been made with v0.7.0 to make things more PEP-like. The new function signatures are described below, but I've allowed for backward compatibility and the older API calls should still work but throw deprecated warnings. **
**New: With 0.7.0 you can now let NL4Py take care of parallelization and execute batches of simulation runs with `run_experiment` (see below for details). **

NL4Py has been tested on both Python 3.6.2 and 2.7.13

### Requirements
* NL4Py works with NetLogo 6.0 and 6.1
* NL4Py requires JDK 1.8 or higher
* NL4Py requires [py4j](https://www.py4j.org/) to be installed with your Python distrubtion
	You can install py4j with: 
```
pip install py4j
``` 

### Installation
Please set the environment variable on your system NETLOGO_APP to point to the 'app' directory in your NetLogo installation folder.

For example, on Windows, this is typically at: 'C:\Program Files\NetLogo 6.0.2\app'

You can install NL4Py using pip-tools: 
```
pip install nl4py
```

### Usage
To use nl4py in your python code use: 

```python
import nl4py 
```
Then initialize with:
```python
nl4py.initialize(path_to_netlogo)
```

#### Examples

[Example1](https://github.com/chathika/NL4Py/blob/master/examples/Example1_NRunsOfFireSampleModel.py) : An example of how to run concurrent NetLogo models. To run this example enter the number of desired concurrent runs as a command line argument:

```
python Example1_NRunsOfFireSampleModel.py 200
```

[Example2](https://github.com/chathika/NL4Py/blob/master/examples/Example2_ScheduledReporters.py) : An example of how to schedule reporters to return simulation state over a range of ticks at a custom tick interval. To run:

```
python Example2_ScheduledReporters.py
```

Also, see this [demo jupyter notebook](https://github.com/chathika/NL4Py/blob/master/examples/Demo%20NL4Py.ipynb)

#### Functions

You can create multiple NetLogo HeadlessWorkspaces from Python using the netLogoWorkspaceFactory: 

```python
nl4py.create_headless_workspace()
```

The following HeadlessWorkspace functions are available:

```python
nl4py.NetLogoHeadlessWorkspace.open_model(self, path : str)
nl4py.NetLogoHeadlessWorkspace.close_model(self)
nl4py.NetLogoHeadlessWorkspace.command(self, command : str)
nl4py.NetLogoHeadlessWorkspace.report(self, reporter : str) -> str
nl4py.NetLogoHeadlessWorkspace.schedule_reporters(self, reporters : list, startAtTick : int = 0, intervalTicks : int = 1, 
                                        stopAtTick : int = -1, goCommand : str = 'go') -> list
nl4py.NetLogoHeadlessWorkspace.set_params_random(self)
nl4py.NetLogoHeadlessWorkspace.get_param_ranges(self) -> list
nl4py.NetLogoHeadlessWorkspace.get_param_names(self) -> list
```

Alternatively, you can execute an entire batch of NetLogo runs and let NL4Py take care of parallelization with:

```python
nl4py.run_experiment(model_name, setup_callback, setup_data=None, reporters=[], start_at_tick=0,interval=1,stop_at_tick=10000000,go_command="go",num_procs=-1)
```

Additionally, the nl4py provides the following functions:

```python
nl4py.get_all_headless_workspaces()
nl4py.delete_headless_workspace(headlessWorkspace)
```

To open the NetLogo application in GUI mode use:

```python
nl4py.netlogo_app()
```

### Referencing:

Please cite as: Gunaratne, C. (2018). NL4Py. https://github.com/chathika/NL4Py. Complex Adaptive Systems Lab, University of Central Florida, Orlando, FL.

NL4Py is based off of David Masad's [Py2NetLogo](https://github.com/dmasad/Py2NetLogo), available at: https://github.com/dmasad/Py2NetLogo

### Copyright

Copyright (C) 2018 Chathika Gunaratne, Complex Adaptive Systems Lab, University of Central Florida.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.





