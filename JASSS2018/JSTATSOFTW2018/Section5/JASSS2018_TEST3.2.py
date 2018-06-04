import time
startTime = int(round(time.time() * 1000))
import pyNetLogo
workspaces = []
modelRuns = 200
for i in range(0,modelRuns):
	n = pyNetLogo.NetLogoLink(gui=False, netlogo_home = "C:\Program Files\NetLogo 6.0.3", netlogo_version = '6')
	n.load_model("./Ethnocentrism.nlogo")
        n.command("set mutation-rate random-float 1")
        n.command("set initial-PTR random-float 1")
        n.command("set death-rate random-float 1")
        n.command("set cost-of-giving random-float 1")
        n.command("set immigrants-per-day random 100")
        n.command("set gain-of-receiving random-float 1")
        n.command("set immigrant-chance-cooperate-with-same random-float 1")
        n.command("set immigrant-chance-cooperate-with-different random-float 1")
        n.command("setup-full")
        n.command("repeat 1000 [go]")
	workspaces.append(n)
while len(workspaces) > 0:
	for workspace in workspaces:
		#Check if workspaces are stopped
		ticks = int(float(workspace.report("ticks")))
		if ticks == 1000:
			r1 = workspace.report('count turtles with [shape = "circle"]')
                        r2 = workspace.report('count turtles with [shape = "circle 2"]')
                        r3 = workspace.report('count turtles with [shape = "square"]')
                        r4 = workspace.report('count turtles with [shape = "square 2"]')
                        print(str(modelRuns - len(workspaces))+" "+str(r1)+" "+str(r2)+" "+str(r3)+" "+str(r4)+" "+str(ticks))
			workspaces.remove(workspace)
stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
with open("Times_Comparison_Ethnocentrism.csv", "a+") as myfile:
        myfile.write('Ethnocentrism,' + str(modelRuns) + ',PyNetLogo,' + str(totalTime) + '\n')
print(totalTime)
