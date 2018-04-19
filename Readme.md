## NL4Py

A Python controller interface to NetLogo. NL4Py uses a client-server architecture, allowing Python client code to control NetLogo workspaces on a controller server. NL4Py supports controlling multiple workspaces through a single Python client. 

At the moment, only HeadlessWorkspaces are supported. NL4Py has been tested on both Python 3.6.2 and 2.7.13

### Requirements
* NL4Py works with NetLogo 6.0.2
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
#### Examples

For an example please see run this [Python file](https://github.com/chathika/NL4Py/blob/master/examples/Example1_NRunsOfFireSampleModel.py) with the number of desired concurrent runs as a command line argument:

```
python Example1_NRunsOfFireSampleModel.py 200
```

Also, see this [demo jupyter notebook](https://github.com/chathika/NL4Py/blob/master/examples/Demo%20NL4Py.ipynb)

#### Functions

You can create multiple NetLogo HeadlessWorkspaces from Python using the netLogoWorkspaceFactory: 

```python
nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
```

The following HeadlessWorkspace functions are available:

```python
nl4py.NetLogo_HeadlessWorkspace.openModel(path_to_model)
nl4py.NetLogo_HeadlessWorkspace.closeModel()
nl4py.NetLogo_HeadlessWorkspace.command(netlogo_command_string)
nl4py.NetLogo_HeadlessWorkspace.report(netlogo_command_string)
nl4py.NetLogo_HeadlessWorkspace.scheduleReportersAndRun(reporters_array, startAtTick=0, intervalTicks=1, stopAtTick=-1, goCommand="go")
nl4py.NetLogo_HeadlessWorkspace.getScheduledReporterResults()
nl4py.NetLogo_HeadlessWorkspace.setParamsRandom()
nl4py.NetLogo_HeadlessWorkspace.getParamNames()
nl4py.NetLogo_HeadlessWorkspace.getParamRanges()
```

Additionally, the netLogoWorkspaceFactory provides the following functions:

```python
nl4py.netlogoWorkspaceFactory.deleteAllExistingWorkspaces() 
nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces()
```
	
### Referencing:

Please cite as: Gunaratne, C. (2018). NL4Py. https://github.com/chathika/NL4Py. Complex Adaptive Systems Lab, University of Central Florida, Orlando, FL.

NL4Py is based off of David Masad's [Py2NetLogo](https://github.com/dmasad/Py2NetLogo), available at: https://github.com/dmasad/Py2NetLogo

### Copyright

Copyright (C) 2018 Chathika Gunaratne, Complex Adaptive Systems Lab, University of Central Florida.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.





