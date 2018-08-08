import sys
import re
import subprocess
import papermill as pm
import os
import plot 
#If user provides NetLogo path as argument, override the config file
if len(sys.argv) > 1:
    netlogo_path = sys.argv[1]
    with open("config.txt","a+") as configFile:
        configFile.write("\r\nnetlogo_path_user=\"" + str(netlogo_path).replace("\\", "/").strip('\"').strip("\'") + "\"")
else:
    #Otherwise use the path in the config file
    pass

os.environ["netlogo_path"] = netlogo_path
'''
with open("config.txt","r") as configFile:
    configFileContent = configFile.readlines()
for line in configFileContent:
    elements = line.split("=")
    print(elements)
    if str(elements[0]).lower().strip() == "netlogo_path":
        netlogo_path = elements[1]
print(netlogo_path)

'''
outDir = "output"
if not os.path.exists("output"):
    os.mkdir(outDir)
# Section3
#os.system('python -W ignore Section3/ParameterCalibrationWithDEAP.py')
#os.system('python -W ignore Section3/SensitivityAnalysis.py')
#pm.execute_notebook('Section3/ParameterCalibrationWithDEAP.ipynb','out_5.3.ipynb', parameters = dict(netlogo_path= netlogo_path))
#pm.execute_notebook('Section3/SensitivityAnalysis.ipynb','out_5.3.ipynb', parameters = dict(netlogo_path= netlogo_path))
# Section5
outputFile = "output/5.1_output.csv"
if os.path.exists(outputFile):
    os.remove(outputFile)
os.system('python -W ignore Section5/nl4py_gunaratne2018_5.1.threadcountcomparison.py "{0}"'.format(netlogo_path) )
plot.plot5_1()

outputFile = "output/5.2_output.csv"
if os.path.exists(outputFile):
    os.remove(outputFile)
with open(outputFile, "w+") as myfile:
    myfile.write('model,runs,connector,time.ms\n')
for i in range(0,4):
  os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.fire.nl4py.py "{0}"'.format(netlogo_path) )

for i in range(0,4):
  os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.fire.pynetlogo.py "{0}"'.format(netlogo_path) )

for i in range(0,4):
  os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.ethnocentrism.nl4py.py "{0}"'.format(netlogo_path) )

for i in range(0,4):
  os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.ethnocentrism.pynetlogo.py "{0}"'.format(netlogo_path) )

for i in range(0,4):
  os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.wolfsheeppredation.nl4py.py "{0}"'.format(netlogo_path) )

for i in range(0,4):
  os.system('python -W ignore Section5/nl4py_gunaratne2018_5.2.wolfsheeppredation.pynetlogo.py "{0}"'.format(netlogo_path) )
plot.plot5_2()
'''
# 5.3 NL4Py
os.system("jupyter nbconvert --to html Section5/nl4py_gunaratne2018_5.3.nl4py_scheduledreporters.ipynb --ExecutePreprocessor.kernel_name=python  --ExecutePreprocessor.enabled=True --ExecutePreprocessor.timeout=-1")
# 5.3 pyNetLogo
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
'''
