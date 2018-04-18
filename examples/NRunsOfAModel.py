########Demonstration of NL4Py#################
#This example takes two commandline arguments n and model
#n : number of concurrent model runs required.
#model: path to model file
#example usage: python NRunsOfAModel.py 100 "/path/to/model.nlogo"
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")

import nl4py 

print("\n1) Starting the NetLogoControllerServer with: nl4py.startServer()\n")

nl4py.startServer()

import sys

print('\n2) Starting the model runs... ')

n = sys.argv[1]
model = sys.argv[2]

print('\n2.1) Creating ' + n + ' NetLogo HeadlessWorkspaces with: nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()')
print('\n2.2) Opening ' + model + ' copies of the model at ' + str(n) + ' on the NetLogo HeadlessWorkspaces with: nl4py.NetLogoHeadlessWorkspace.openModel("model")')
for i in range(0,int(n)):
	n = nl4py.netlogoWorkspaceFactory.newNetLogoHeadlessWorkspace()
	n.openModel(model)
	
print("\n2.3) Setting the parameters for all " + str(n) + " models to random values with nl4py.NetLogoHeadlessWorkspace.setParamsRandom()")
for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
	workspace.setParamsRandom()

print('\n2.4) Send setup and go commands to each model using: nl4py.NetLogo_HeadlessWorkspace.command("setup") and nl4py.NetLogoHeadlessWorkspace.command("go") ')
for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
	workspace.command("setup")
	workspace.command("go")

print('\n2.5) Get back current state from all executing models using a NetLogo reporter: nl4py.NetLogo_HeadlessWorkspace.report("burned-trees")')
for workspace in nl4py.netlogoWorkspaceFactory.getAllExistingWorkspaces():
	print(workspace.report("burned-trees"))

print('\n3) Shutdown the server to release compute resources using: nl4py.stopServer()')
nl4py.stopServer()
print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')