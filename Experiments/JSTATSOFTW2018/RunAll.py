import sys
import re
import subprocess
#If user provides NetLogo path as argument, override the config file
if len(sys.argv) > 1:
    netlogo_path = sys.argv[1]
    with open("config.txt","a+") as configFile:
        configFile.write("\r\nnetlogo_path_user=\"" + str(netlogo_path).replace("\\", "/").strip('\"').strip("\'") + "\"")
else:
    #Otherwise use the path in the config file
    pass
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
import os
os.system('python -W ignore ParameterCalibrationWithDEAP.py')
os.system('python -W ignore SensitivityAnalysis.py')

