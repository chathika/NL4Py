## NL4Py

A Python controller interface to NetLogo. NL4Py uses a client-server architecture, allowing Python client code to control NetLogo workspaces on a controller server. NL4Py supports controlling multiple workspaces through a single Python client. 

At the moment, only HeadlessWorkspaces are supported.

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
	```
	import nl4py 
	```
#### Functions

You can now create NetLogo HeadlessWorkspaces from Python: 
	```
	n = nl4py.NetLogo_HeadlessWorkspace()
	```

The following core controller functions are available:

	1. nl4py.NetLogo_HeadlessWorkspace.openModel(path_to_model)
	2. nl4py.NetLogo_HeadlessWorkspace.closeModel()
	3. nl4py.NetLogo_HeadlessWorkspace.command(netlogo_command_string)
	4. nl4py.NetLogo_HeadlessWorkspace.report(netlogo_command_string)
	5. nl4py.NetLogo_HeadlessWorkspace.setParamsRandom()
	6. nl4py.NetLogo_HeadlessWorkspace.getParamNames()
	7. nl4py.NetLogo_HeadlessWorkspace.getParamRanges()
	
You can create multiple workspaces as required

#### Example

For an example please see this [demo jupyter notebook](https://github.com/chathika/NL4Py/blob/master/examples/Demo%20NL4Py.ipynb)
	
### Additional:

NL4Py is based off of David Masad's [Py2NetLogo](https://github.com/dmasad/Py2NetLogo).

#### Py2NetLogo

A hacked-together interface for controlling [NetLogo](https://ccl.northwestern.edu/netlogo/) from Python, using [Py4J](py4j.sourceforge.net/). Inspired by [RNetLogo](http://cran.r-project.org/web/packages/RNetLogo/index.html). 

The project (such as it is) is described in [this blog post](http://davidmasad.com/blog/netlogo-from-python). You can also view the [test IPython Notebook](http://nbviewer.ipython.org/github/dmasad/Py2NetLogo/blob/master/NetLogo%20Connection.ipynb).

### Requirements
* Python
* Java
* Py4J
* NetLogo 5.x


