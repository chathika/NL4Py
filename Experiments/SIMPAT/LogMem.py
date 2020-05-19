import psutil
import os
import time
import csv

def log_mem(connector,runsNeeded,ticksNeeded,rep):
    mem_output_file = os.path.join("output","memory","{0}_runs{1}_ticks{2}_rep{3}.csv".format(connector,str(runsNeeded),str(ticksNeeded),str(rep)))
    os.makedirs(os.path.dirname(mem_output_file), exist_ok=True)
    mem_stats = dict(psutil.virtual_memory()._asdict())
    with open (mem_output_file, "w+") as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerow(mem_stats.keys())
        while True:
            mem_stats = dict(psutil.virtual_memory()._asdict())
            writer.writerow(mem_stats.values())
            time.sleep(1)
            out.flush()
