import sys
import re
import subprocess
import papermill as pm
import os
import plot 
from matplotlib.pyplot import show
#If user provides NetLogo path as argument, override the config file
if len(sys.argv) > 1:
    netlogo_path = sys.argv[1]
else: 
    print("Please provide the path to your NetLogo installation as a command line argument and try again.")
    exit(1)
os.environ["netlogo_path"] = netlogo_path

print("All experiment outputs will be generated in the output folder.")
outDir = "output"
if not os.path.exists("output"):
    os.mkdir(outDir)

# Section3
print("\n\nBeginning Section 3 Experiments...\n")
print("\n5.1 Running Parameter Calibration on the Wolf Sheep Predation NetLogo model with DEAP...\n")
os.system('python -W ignore Section3/ParameterCalibrationWithDEAP.py "{0}"'.format(netlogo_path) )


print("\n\n------------------------------------------------------------------------------------\n")
print("\n5.2 Running Sensitivity Analysis on the Wolf Sheep Predation NetLogo model with SALib...\n")
os.system('python -W ignore Section3/SensitivityAnalysis.py "{0}"'.format(netlogo_path) )


# Section5

print("Beginning Section 5 Experiments...")
print("\n\n5.1 Starting execution time evaluation for NL4Py under different thread counts...\n")
print("Please wait. This may take a while to complete...")
os.system('python -W ignore Section5/nl4py_gunaratne2018_5.1.threadcountcomparison.py "{0}"'.format(netlogo_path) )
plot.plot5_1()

print("\n\n5.2 Starting execution time comparisons between NL4Py and PyNetLogo...\n")
outputFile = "output/5.2_output.csv"
if os.path.exists(outputFile):
    os.remove(outputFile)
with open(outputFile, "w+") as out:
    out.write('model,runs,connector,time.ms\n')

print("Performing 10 repetitions of 200 model runs of the Fire NetLogo model with NL4Py")
totalRepeats = 10
currentRepeat = 1
for i in range(0,currentRepeat):
    print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
    os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.fire.nl4py.py "{0}"'.format(netlogo_path) )
    currentRepeat = currentRepeat + 1
print("Performing 10 repetitions of 200 model runs of the Fire NetLogo model with PyNetLogo")
currentRepeat = 1
for i in range(0,currentRepeat):
    print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
    os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.fire.pynetlogo.py "{0}"'.format(netlogo_path) )
    currentRepeat = currentRepeat + 1
print("Performing 10 repetitions of 200 model runs of the Ethnocentrism NetLogo model with NL4Py")
currentRepeat = 1
for i in range(0,currentRepeat):
    print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
    os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.ethnocentrism.nl4py.py "{0}"'.format(netlogo_path) )
    currentRepeat = currentRepeat + 1
print("Performing 10 repetitions of 200 model runs of the Ethnocentrism NetLogo model with PyNetLogo")
currentRepeat = 1
for i in range(0,currentRepeat):
    print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
    os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.ethnocentrism.pynetlogo.py "{0}"'.format(netlogo_path) )
    currentRepeat = currentRepeat + 1
print("Performing 10 repetitions of 200 model runs of the Wolf Sheep Predation NetLogo model with NL4Py")
currentRepeat = 1
for i in range(0,currentRepeat):
    print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
    os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.wolfsheeppredation.nl4py.py "{0}"'.format(netlogo_path) )
    currentRepeat = currentRepeat + 1
print("Performing 10 repetitions of 200 model runs of the Wolf Sheep Predation NetLogo model with PyNetLogo")
currentRepeat = 1
for i in range(0,currentRepeat):
    print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
    os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.wolfsheeppredation.pynetlogo.py "{0}"'.format(netlogo_path) )
    currentRepeat = currentRepeat + 1

plot.plot5_2()
print("\n\n5.3 Starting execution time comparisons between NL4Py and PyNetLogo with IPCluster...\n")
outputFile = 'output/5.3_output.csv'
if(os.path.exists(outputFile)):
    os.remove(outputFile)
with open (outputFile, "w+") as out:
    out.write("connector,function,runs,time.ms\n")

print("Starting 10 repititions of 5000, 10000, and 15000 Wolf Sheep Predation model runs with NL4Py...")
print("Please wait. This may take a while...")
# 5.3 NL4Py
os.system("jupyter nbconvert --to html Section5/nl4py_gunaratne2018_5.3.nl4py_scheduledreporters.ipynb --ExecutePreprocessor.kernel_name=python  --ExecutePreprocessor.enabled=True --ExecutePreprocessor.timeout=-1")
# 5.3 pyNetLogo
print("Starting 10 repititions of 5000, 10000, and 15000 Wolf Sheep Predation model runs with PyNetLogo...")
print("Please wait. This may take a while...")
import subprocess
import ipyparallel as ipp
def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''

    # Poll process for new output until finished
    for line in iter(process.stdout.readline, ""):
        print(line,)
        output += str(line)
        if "successfully" in str(line):
            os.system("jupyter nbconvert --to html Section5/nl4py_gunaratne2018_5.3.pynetlogo_repeatreporter.ipynb  --ExecutePreprocessor.kernel_name=python --ExecutePreprocessor.enabled=True --ExecutePreprocessor.timeout=-1")
            print("done")
            return 
            #rc = ipp.Client()
            # shutdown everything, including the Hub
            #rc.shutdown(hub=True)


    process.wait()
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise Exception(command, exitCode, output)

execute(['ipcluster', 'start', '-n', '8'])
rc = ipp.Client()
# shutdown everything, including the Hub
rc.shutdown(hub=True)

plot.plot5_3()

print("All Experiments Done. Please press Ctrl + c to exit")

