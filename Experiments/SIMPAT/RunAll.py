import sys
import signal
import re
import subprocess
from multiprocessing import Process
import os
import plot 
from matplotlib.pyplot import show
import time
import pandas as pd
import psutil
import csv
import LogMem
if __name__=="__main__":
    #If user provides NetLogo path as argument, override the config file
    if len(sys.argv) > 1:
        netlogo_path = os.path.join(sys.argv[1])
    else: 
        print("Please provide the path to your NetLogo installation as a command line argument and try again.")
        exit(1)
    os.environ["netlogo_path"] = os.path.join(netlogo_path)
    python_command = "python"#os.path.basename(sys.executable)

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


        def getMemoryUsedForConnector(connector,model,runsNeeded,ticksNeeded,rep):
            mem_output_file = os.path.join("output","memory","{0}_model{1}_runs{2}_ticks{3}_rep{4}.csv".format(connector,str(model),str(runsNeeded),str(ticksNeeded),str(rep)))
            df = pd.read_csv(mem_output_file)
            df["connector"]=connector
            df["model"]=model
            df["rep"]=rep
            df["runs"]=runsNeeded
            df["ticks"]=ticksNeeded
            return df

        print("\n\n5.3 Starting execution time comparisons between NL4Py runExperiment and PyNetLogo with multiprocessing...\n")
        outputFile = os.path.join('output','5.3_output.csv')
        with open (outputFile, "w") as out:
            out.write("connector,function,runs,ticks,time.ms,max.memory.used.b\n")
            out.flush()
            out.close()
        # 5.3 NL4Py
        print("Starting 10 repititions of 5000, 10000, and 15000 Ethnocentrism model runs for 2000, 4000, and 8000 ticks...")
        print("Please wait. This may take a while...")
        totalRepeats = 10
        runsNeededList = list(range(200,1200,200))
        models = ["Fire.nlogo","Ethnocentrism.nlogo","Wolf Sheep Predation.nlogo"]
        ticks = [100,1000,100]
        all_memory_data_bytes = pd.DataFrame(columns=["connector","model","rep","runs","ticks","total","used","free"])    
        with open (outputFile, "a+") as time_out:
                for rep in range(totalRepeats):
                    for runs_needed in runsNeededList:
                        for idx in range(len(models)):
                            model_path = os.path.join("Models",models[idx])
                            ticks_needed = ticks[idx]
                            #nl4py
                            mem_proc = Process(target=LogMem.log_mem, args = ("nl4py",models[idx],runs_needed,ticks_needed,rep,))
                            mem_proc.start()
                            experiment_path = os.path.join("Section5","nl4py_gunaratne2019_5.3.nl4py_scheduledreporters.py")
                            startTime = int(round(time.time() * 1000))
                            os.system("{0} \"{1}\" \"{2}\" \"{3}\" {4} {5}".format("python",experiment_path,netlogo_path,model_path,runs_needed,ticks_needed))
                            stopTime = int(round(time.time() * 1000))
                            mem_proc.terminate()
                            mem_proc.join()
                            executionTime = stopTime - startTime
                            df = getMemoryUsedForConnector("nl4py",models[idx],runs_needed,ticks_needed,rep)
                            all_memory_data_bytes=all_memory_data_bytes.append(df,sort=False)
                            time_out.write("nl4py,scheduledreporters," + str(models[idx]) + "," + str(runs_needed) + "," + str(ticks_needed) + "," + str(executionTime) + "," + str(df.used.max()-df.used.min()) + "\n")
                            time_out.flush()
                            print("nl4py,scheduledreporters," + str(models[idx]) + "," + str(runs_needed) + "," + str(ticks_needed) + "," + str(executionTime) + "," + str(df.used.max()-df.used.min()))                        
                            #nl4py
                            mem_proc = Process(target=LogMem.log_mem, args = ("nl4py",models[idx],runs_needed,ticks_needed,rep,))
                            mem_proc.start()
                            experiment_path = os.path.join("Section5","nl4py_gunaratne2019_5.3.nl4py_runexperiment.py")
                            startTime = int(round(time.time() * 1000))
                            os.system("{0} \"{1}\" \"{2}\" \"{3}\" {4} {5}".format("python",experiment_path,netlogo_path,model_path,runs_needed,ticks_needed))
                            stopTime = int(round(time.time() * 1000))
                            mem_proc.terminate()
                            mem_proc.join()
                            executionTime = stopTime - startTime
                            df = getMemoryUsedForConnector("nl4py",models[idx],runs_needed,ticks_needed,rep)
                            all_memory_data_bytes=all_memory_data_bytes.append(df,sort=False)
                            time_out.write("nl4py,runexperiment," + str(models[idx]) + ","  + str(runs_needed) + "," + str(ticks_needed) + "," + str(executionTime) + "," + str(df.used.max()-df.used.min()) + "\n")
                            time_out.flush()
                            print("nl4py,runexperiment," + str(models[idx]) + ","  + str(runs_needed) + "," + str(ticks_needed) + "," + str(executionTime) + "," + str(df.used.max()-df.used.min()))                        
                            #pynetlogo
                            mem_proc = Process(target=LogMem.log_mem, args = ("pynetlogo",models[idx],runs_needed,ticks_needed,rep,))
                            mem_proc.start()   
                            experiment_path = os.path.join("Section5","nl4py_gunaratne2018_5.3.pynetlogo_repeatreporter.py")
                            startTime = int(round(time.time() * 1000))
                            os.system("{0} \"{1}\" \"{2}\" \"{3}\" {4} {5}".format("python",experiment_path,netlogo_path,model_path,runs_needed,ticks_needed))
                            stopTime = int(round(time.time() * 1000))
                            mem_proc.terminate()
                            mem_proc.join()
                            executionTime = stopTime - startTime
                            df = getMemoryUsedForConnector("pynetlogo",models[idx],runs_needed,ticks_needed,rep)
                            all_memory_data_bytes=all_memory_data_bytes.append(df,sort=False)
                            time_out.write("pynetlogo,repeatreporter," + str(models[idx]) + "," + str(runs_needed) + "," + str(ticks_needed) + "," + str(executionTime) + "," + str(df.used.max()-df.used.min()) + "\n")
                            time_out.flush()
                            print("pynetlogo,repeatreporter," + str(models[idx]) + "," + str(runs_needed) + "," + str(ticks_needed) + "," + str(executionTime) + "," + str(df.used.max()-df.used.min()))  
        print(all_memory_data_bytes)
        
        plot.plot5_3_1()
        plot.plot5_3_2()
        show()
            
    print("All Experiments Done.")
