import os
import queue
from tqdm import tqdm
import threading
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="A script to run multiple ns3 simulations, extract data, and show graph")
parser.add_argument("--process-only", action="store_true", help="pass this flag if you only wish to process the data")
args = parser.parse_args()

SIM_TIME = 10
MIN_CARS = 50
MAX_CARS = 200
STEP = 25
cars = list(range(MIN_CARS, MAX_CARS + 1, STEP))

def run_sim(num_cars, queue):
    os.system(f"./ns3 run 'vanet-routing-compare --totaltime={SIM_TIME} --nodes={num_cars} --CSVfileName=pdrVScars/{num_cars}cars.csv' > /dev/null 2>&1")
    queue.put(num_cars)

if args.process_only == False:

    input = input("This action will remove previous data, do you want to proceed (y/n)? ")
    if input.lower() != "y":
        print("Exiting...")
        exit()
        

    # clean up old csv's
    print("Cleaning old csv's...")
    dir_path = "./pdrVScars"
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    print("============================================================================")
    print(f"Running a total of {len(cars)} simulations w/ a simulation time of {SIM_TIME}")
    print(f"Starting car number is {MIN_CARS}")
    print(f"Ending car number is {MAX_CARS}")
    print(f"Stepping by {STEP} cars")
    print("============================================================================")

    queue = queue.Queue()
    threads = []
    for num_cars in cars:
        thread = threading.Thread(target=run_sim, args=(num_cars, queue))
        threads.append(thread)
        thread.start()

    # Update progress bar
    for i in tqdm(range(len(cars)), ascii=True):
        thread_num = queue.get()
        tqdm.write(f"Thread w/ {thread_num} cars just finished...")

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    print("\nAll threads finished...")

# process data
loc_list = ["SimulationSecond"]
bsm_list = [f"BSM_PDR{x}" for x in range(1,11)]
loc_list.extend(bsm_list)
dir_path = "./pdrVScars"
for file_name in os.listdir(dir_path):
    file_path = os.path.join(dir_path, file_name)
    if os.path.isfile(file_path):
        print(f"\nReading file: {file_path}")
        df = pd.read_csv(file_path)
        selected_columns = df.loc[:, loc_list]
        print(selected_columns)

# graph data 

