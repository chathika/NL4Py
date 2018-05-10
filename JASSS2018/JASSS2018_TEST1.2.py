import nl4py
nl4py.startServer()

import time
startTime = int(round(time.time() * 1000))
nl4py.deleteAllHeadlessWorkspaces() 

runsDone = 0
runsStarted = 0
runsNeeded = 1000
allResults = []
def schedule(workspace_):
    workspace_.command("stop")
    '''for i, name in enumerate(problem['names']):
        if name == 'random-seed':
            #The NetLogo random seed requires a different syntax
            workspace_.command('random-seed {}'.format(param_values[runsStarted][i]))
        else:
            #Otherwise, assume the input parameters are global variables
            workspace_.command('set {0} {1}'.format(name, param_values[runsStarted][i]))'''
    workspace_.setParamsRandom()
    workspace_.command('setup')
    workspace_.scheduleReportersAndRun(["ticks",'count sheep','count wolves'], 0,1,100,"go")    

for i in range(0,1):
    workspace = nl4py.newNetLogoHeadlessWorkspace()
    workspace.openModel('Wolf Sheep Predation.nlogo')
    schedule(workspace)
    runsStarted = runsStarted + 1
while (runsDone < runsNeeded):
    for workspace in nl4py.getAllHeadlessWorkspaces(): 
        wsr = workspace.getScheduledReporterResults()
        print(wsr)
        if wsr != []:
            allResults.extend(wsr)
            runsDone = runsDone + 1
            print(runsDone)
            if runsStarted < runsNeeded:
                    schedule(workspace)
                    runsStarted = runsStarted + 1
stopTime = int(round(time.time() * 1000))
print(stopTime - startTime)