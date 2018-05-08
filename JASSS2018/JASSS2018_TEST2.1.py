import time
startTime = int(round(time.time() * 1000))
import nl4py
nl4py.startServer()
workspaces = []
for i in range(0,200):
	n = nl4py.newNetLogoHeadlessWorkspace()
	n.openModel("./Fire.nlogo")
	n.command("set density random 99")
	n.command("setup")
	n.command("repeat 100 [go]")
	workspaces.append(n)
while len(workspaces) > 0:
	#time.sleep(4)
	for workspace in workspaces:
		#Check if workspaces are stopped
		ticks = int(float(workspace.report("ticks")))
                stop = str(workspace.report("not any? turtles")).lower()
                if ticks == 100 or stop == "true":
			print(str(200 - len(workspaces)) + " " +  str(workspace.report("burned-trees")) + " " + str(ticks) + " " + stop)
			workspaces.remove(workspace)
stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
print(totalTime)
with open("Times_Comparison_Fire.csv", "a") as myfile:
	myfile.write('Fire,200,NL4Py,' + str(totalTime))
nl4py.stopServer()
