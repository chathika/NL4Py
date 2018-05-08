import time
startTime = int(round(time.time() * 1000))
import pyNetLogo
workspaces = []
for i in range(0,200):
	n = pyNetLogo.NetLogoLink(gui=False, netlogo_home = "/home/ubuntu/netlogo", netlogo_version = '6')
	n.load_model(r"./Fire.nlogo")
	n.command("set density random 99")
	n.command("setup")
	n.command("repeat 100 [go]")
	workspaces.append(n)
while len(workspaces) > 0:
	for workspace in workspaces:
		#Check if workspaces are stopped
		ticks = int(float(workspace.report("ticks")))
		stop = str(workspace.report("not any? turtles")).lower()
		if ticks == 100 or stop == "true":
			print(str(200 - len(workspaces)) + " " +  str(workspace.report("burned-trees")) + " " + str(ticks) + " " + stop)
			workspaces.remove(workspace)
stopTime = int(round(time.time() * 1000))
totalTime = stopTime - startTime
with open("Times_Comparison_Fire.csv", "a+") as myfile:
        myfile.write('Fire,200,PyNetLogo,' + str(totalTime))
print(totalTime)
