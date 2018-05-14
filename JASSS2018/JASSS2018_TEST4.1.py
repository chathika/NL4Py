import time
startTime = int(round(time.time() * 1000))
import nl4py
nl4py.startServer()
workspaces = []
modelRuns = 200
for i in range(0,modelRuns):
	n = nl4py.newNetLogoHeadlessWorkspace()
	n.openModel("./Wolf Sheep Predation.nlogo")
        n.command("set initial-number-sheep random-float 250")
        n.command("set initial-number-wolves random-float 250")
        n.command("set grass-regrowth-time random-float 100")
        n.command("set sheep-gain-from-food random-float 50")
        n.command("set wolf-gain-from-food random 100")
        n.command("set sheep-reproduce random-float 20")
        n.command("set wolf-reproduce random-float 20")
        n.command("set show-energy? false")
	n.command('set model-version "sheep-wolves-grass"')
        n.command("setup")
        n.command("repeat 100 [go]")
	workspaces.append(n)
while len(workspaces) > 0:
	for workspace in workspaces:
		#Check if workspaces are stopped
		ticks = int(float(workspace.report("ticks")))
		stop1 = str(workspace.report("not any? turtles")).lower()  
		stop2 = str(workspace.report("not any? wolves and count sheep > max-sheep")).lower()  
		if ticks == 100 or stop1 == "true" or stop2 == "true":
			r1 = workspace.report('count sheep')
                        r2 = workspace.report('count wolves')
                        print(str(modelRuns - len(workspaces))+" "+str(r1)+" "+str(r2)+str(ticks))
			workspaces.remove(workspace)
stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
with open("Times_Comparison_Reporters.csv", "a+") as myfile:
        myfile.write('Wolf Sheep Predation,' + str(modelRuns) + ',NL4Py,' + str(totalTime) + '\n')
print(totalTime)
nl4py.stopServer()
