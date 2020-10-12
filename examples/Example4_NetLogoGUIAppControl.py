########Demonstration of NL4Py#################
#This example demonstrates NetLogo Application Control with GUI through NL4Py
#example usage: python Example3_NetLogoGUIAppControl.py netlogo_home
###############################################

print("\n\n------------ This is a Demonstration of NL4PY --------------------\n")
import time
import sys

import nl4py 

print("\n1) Starting the NetLogoControllerServer with: nl4py.startServer()\n")

nl4py.initialize(sys.argv[1])

print('\n2) Starting the model runs... ')

model = "./Fire.nlogo"

print('\n2.1) Starting the NetLogo Application with: n = nl4py.NetLogoApp()')
n = nl4py.netlogo_app()
print(f'\n2.2) Opening the model at {model} on the NetLogo application with: n.openModel("model")')
n.open_model(model)
	
print("\n2.3) Setting the parameters for the model to random values with: n.setParamsRandom()")
n.set_params_random()

print('\n2.4) Send setup and go commands to the model: n.command("setup") and: n.command("repeat 100 [go]") ')
n.command("setup")
n.command("repeat 100 [go]")

time.sleep(5)

print('\n2.5) Get back current state using a NetLogo reporter: n.report("burned-trees")')
print(n.report("burned-trees"))

print('\n3.1) Shutdown the NetLogo application using: nl4py.closeModel()')
n.close_model()

print('\n\n------------------------ Thanks for trying NL4PY -------------------------\n')