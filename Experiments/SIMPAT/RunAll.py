import sys
import signal
import re
import subprocess
import os
import plot 
from matplotlib.pyplot import show
import time
import pandas as pd
#If user provides NetLogo path as argument, override the config file
if len(sys.argv) > 1:
    netlogo_path = sys.argv[1]
else: 
    print("Please provide the path to your NetLogo installation as a command line argument and try again.")
    exit(1)
os.environ["netlogo_path"] = netlogo_path
python_command = os.path.basename(sys.executable)

print("Please enter experiment number you want to run: ")
print("0 Run all experiments (Full Replication)")
print("1 Parameter Calibration with NL4Py and DEAP")
print("2 Sensitvity Analysis with NL4Py and SALib")
print("3 Thread execution time comparisons using NL4Py")
print("4 Execution time comparisons between NL4Py and PyNetLogo on three different models")
print("5 Execution time comparison between NL4Py and PyNetLogo with IPCluster")
experiment = int(input("Run experiment: "))

print("All experiment outputs will be generated in the output folder.")
outDir = "output"
if not os.path.exists("output"):
    os.mkdir(outDir)

# Section3
if (experiment == 0):
    print("\n\nBeginning Section 3 Experiments...\n")

if (experiment == 0 or experiment == 1):    
    print("\n5.1 Running Parameter Calibration on the Wolf Sheep Predation NetLogo model with DEAP...\n")
    os.system('{0} -W ignore Section3/ParameterCalibrationWithDEAP.py "{1}"'.format(python_command,netlogo_path) )

if (experiment == 0 or experiment == 2):
    print("\n\n------------------------------------------------------------------------------------\n")
    print("\n5.2 Running Sensitivity Analysis on the Wolf Sheep Predation NetLogo model with SALib...\n")
    os.system('{0} -W ignore Section3/SensitivityAnalysis.py "{1}"'.format(python_command,netlogo_path) )


# Section5
if (experiment == 0):
    print("Beginning Section 5 Experiments...")
if (experiment == 0 or experiment == 3):
    print("\n\n5.1 Starting execution time evaluation for NL4Py under different thread counts...\n")
    print("Please wait. This may take a while to complete...")
    os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.1.threadcountcomparison.py "{1}"'.format(python_command,netlogo_path) )
    plot.plot5_1()

if (experiment == 0 or experiment == 4):
    print("\n\n5.2 Starting execution time comparisons between NL4Py and PyNetLogo...\n")
    outputFile = "output/5.2_output.csv"
    if os.path.exists(outputFile):
        os.remove(outputFile)
    with open(outputFile, "w+") as out:
        out.write('model,runs,connector,time.ms\n')

    print("Performing 10 repetitions of 200 model runs of the Fire NetLogo model with NL4Py")
    totalRepeats = 10
    currentRepeat = 1
    for i in range(0,totalRepeats):
        print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
        os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.2.fire.nl4py.py "{1}"'.format(python_command,netlogo_path) )
        currentRepeat = currentRepeat + 1
    print("Performing 10 repetitions of 200 model runs of the Fire NetLogo model with PyNetLogo")
    currentRepeat = 1
    for i in range(0,totalRepeats):
        print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
        os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.2.fire.pynetlogo.py "{1}"'.format(python_command,netlogo_path) )
        currentRepeat = currentRepeat + 1
    print("Performing 10 repetitions of 200 model runs of the Ethnocentrism NetLogo model with NL4Py")
    currentRepeat = 1
    for i in range(0,totalRepeats):
        print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
        os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.2.ethnocentrism.nl4py.py "{1}"'.format(python_command,netlogo_path) )
        currentRepeat = currentRepeat + 1
    print("Performing 10 repetitions of 200 model runs of the Ethnocentrism NetLogo model with PyNetLogo")
    currentRepeat = 1
    for i in range(0,totalRepeats):
        print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
        os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.2.ethnocentrism.pynetlogo.py "{1}"'.format(python_command,netlogo_path) )
        currentRepeat = currentRepeat + 1
    print("Performing 10 repetitions of 200 model runs of the Wolf Sheep Predation NetLogo model with NL4Py")
    currentRepeat = 1
    for i in range(0,totalRepeats):
        print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
        os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.2.wolfsheeppredation.nl4py.py "{1}"'.format(python_command,netlogo_path) )
        currentRepeat = currentRepeat + 1
    print("Performing 10 repetitions of 200 model runs of the Wolf Sheep Predation NetLogo model with PyNetLogo")
    currentRepeat = 1
    for i in range(0,totalRepeats):
        print("Performing {0} out of {1}".format(currentRepeat, totalRepeats))
        os.system('{0} -W ignore Section5/nl4py_gunaratne2018_5.2.wolfsheeppredation.pynetlogo.py "{1}"'.format(python_command,netlogo_path) )
        currentRepeat = currentRepeat + 1
    plot.plot5_2()

if (experiment == 0 or experiment == 5):
    plot.plot5_3_1()
    plot.plot5_3_2()
    def getMemoryUsedForConnector(connector,runsNeeded,ticksNeeded,rep):
        with open("output/memory/{0}_runs{1}_ticks{2}_rep{3}.txt".format(connector,str(runsNeeded),str(ticksNeeded),str(rep)),"r") as f:
            lines = f.readlines()
            column_names = re.sub("\s+",",",lines[0]).split(",")[:4]
            memory_data = []
            for line in lines[1:]:
                memory_entry = re.sub("\s+",",",line).split(",")[:-1]
                if "Total:" in memory_entry and not "free" in memory_entry:
                    memory_data.append(memory_entry)
        df = pd.DataFrame(memory_data, columns=column_names).iloc[:,1:].astype(int)
        df["connector"]=connector
        df["rep"]=rep
        df["runs"]=runsNeeded
        df["ticks"]=ticksNeeded
        return df

    """print("\n\n5.3 Starting execution time comparisons between NL4Py runExperiment and PyNetLogo with multiprocessing...\n")
    outputFile = 'output/5.3_output.csv'
    if(os.path.exists(outputFile)):
        os.remove(outputFile)
    with open (outputFile, "w+") as out:
        out.write("connector,function,runs,ticks,time.ms,max.memory.used.kb\n")
        out.flush()
        out.close()
    #ensure jupyter has the python kernel being used:
    ###os.system("{0} -m ipykernel install --name {0} --user".format(python_command))
    # 5.3 NL4Py
    print("Starting 10 repititions of 5000, 10000, and 15000 Ethnocentrism model runs for 2000, 4000, and 8000 ticks...")
    print("Please wait. This may take a while...")
    totalRepeats = 5
    runsNeededList = [500,1000,1500]
    ticksNeededList = [100]#,200,300]
    import os
    outputFile = 'output/5.3_output.csv' 
    all_memory_data_kilobytes = pd.DataFrame(columns=["connector","rep","runs","ticks","total","used","free"])
    with open (outputFile, "a+") as time_out:
            for rep in range(totalRepeats):
                for runsNeeded in runsNeededList:
                    for ticksNeeded in ticksNeededList:
                        #nl4py
                        mem_log_cmd = "while true; do free -tk >> output/memory/{0}_runs{1}_ticks{2}_rep{3}.txt; sleep 1;done".format("nl4py",str(runsNeeded),str(ticksNeeded),str(rep))
                        mem_log_proc = subprocess.Popen(mem_log_cmd, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
                        startTime = int(round(time.time() * 1000))
                        os.system("{0} Section5/nl4py_gunaratne2019_5.3.nl4py_runexperiment.py {1} {2} {3}".format(python_command,netlogo_path,runsNeeded,ticksNeeded))
                        stopTime = int(round(time.time() * 1000))
                        os.killpg(os.getpgid(mem_log_proc.pid), signal.SIGTERM)
                        executionTime = stopTime - startTime
                        df = getMemoryUsedForConnector("nl4py",runsNeeded,ticksNeeded,rep)
                        all_memory_data_kilobytes=all_memory_data_kilobytes.append(df,sort=False)
                        time_out.write("nl4py,runExperiment," + str(runsNeeded) + "," + str(ticksNeeded) + "," + str(executionTime) + "," + str(df.used.max()) + "\n")
                        time_out.flush()
                        print("nl4py,runExperiment," + str(runsNeeded) + "," + str(ticksNeeded) + "," + str(executionTime) + "," + str(df.used.max()))                        
                        #pynetlogo
                        mem_log_cmd = "while true; do free -tk >> output/memory/{0}_runs{1}_ticks{2}_rep{3}.txt; sleep 1;done".format("pynetlogo",str(runsNeeded),str(ticksNeeded),str(rep))
                        mem_log_proc = subprocess.Popen(mem_log_cmd, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
                        startTime = int(round(time.time() * 1000))
                        os.system("{0} Section5/nl4py_gunaratne2018_5.3.pynetlogo_repeatreporter.py {1} {2} {3}".format(python_command,netlogo_path,runsNeeded,ticksNeeded))
                        stopTime = int(round(time.time() * 1000))
                        os.killpg(os.getpgid(mem_log_proc.pid), signal.SIGTERM)
                        executionTime = stopTime - startTime
                        df = getMemoryUsedForConnector("pynetlogo",runsNeeded,ticksNeeded,rep)                            
                        all_memory_data_kilobytes=all_memory_data_kilobytes.append(df,sort=False)
                        time_out.write("pynetlogo,repeat_report," + str(runsNeeded) + "," + str(ticksNeeded) + "," + str(executionTime) + "," + str(df.used.max()) + "\n")
                        time_out.flush()
                        print("pynetlogo,repeat_report," + str(runsNeeded) + "," + str(ticksNeeded) + "," + str(executionTime) + "," + str(df.used.max()))
    print(all_memory_data_kilobytes)
    
    plot.plot5_3_1()
    plot.plot5_3_2()
    os.system('output\\\\5.3.png')""" 
    """if (experiment == 0 or experiment == 6):
        # 5.3 pyNetLogo
        print("Starting 10 repititions of 5000, 10000, and 15000 Ethnocentrism model runs for 2000, 4000, and 8000 ticks with pyNetLogo...")
        import subprocess
        import ipyparallel as ipp
        def execute(command):
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = ''
            # Poll process for new output until finished
            for line in iter(process.stdout.readline, ""):
                output += str(line)
                if len(line) > 0:
                    print(line)
                if "successfully" in str(line):
                    for i in range(0,totalRepeats):                
                        os.system("jupyter nbconvert --to html Section5/nl4py_gunaratne2018_5.3.pynetlogo_repeatreporter.ipynb  --execute  --ExecutePreprocessor.kernel_name={0}  --ExecutePreprocessor.timeout=-1".format(python_command))
                    print("done")
                    return 
            process.wait()
            exitCode = process.returncode
            if (exitCode == 0):
                return output
            else:
                raise Exception(command, exitCode, output)
        print("Trying to shut down any active ipclusters. Ignore errors if shutdown unable due to absence of active clusters.")
        os.system("ipcluster stop")
        execute('ipcluster start -n ' + str(multiprocessing.cpu_count()))"""
        #
        
print("All Experiments Done.")
