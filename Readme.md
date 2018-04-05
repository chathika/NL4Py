## NL4Py

A Python controller interface to NetLogo. NL4Py uses a client-server architecture, allowing Python client code to control NetLogo workspaces on a controller server. NL4Py supports controlling multiple workspaces through a single Python client. 

At the moment, only HeadlessWorkspaces are supported.

NL4Py is based off of David Masad's Py2NetLogo.

## Py2NetLogo

A hacked-together interface for controlling [NetLogo](https://ccl.northwestern.edu/netlogo/) from Python, using [Py4J](py4j.sourceforge.net/). Inspired by [RNetLogo](http://cran.r-project.org/web/packages/RNetLogo/index.html). 

The project (such as it is) is described in [this blog post](http://davidmasad.com/blog/netlogo-from-python). You can also view the [test IPython Notebook](http://nbviewer.ipython.org/github/dmasad/Py2NetLogo/blob/master/NetLogo%20Connection.ipynb).

### Requirements
* Python
* Java
* Py4J
* NetLogo 5.x


