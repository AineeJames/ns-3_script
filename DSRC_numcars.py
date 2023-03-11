import os
import queue
from tqdm import tqdm
import multiprocessing
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="A script to run multiple ns3 simulations, extract data, and show graph")
parser.add_argument("--process-only", action="store_true", help="pass this flag if you only wish to process the data")
args = parser.parse_args()

def run_sim(num_cars, queue, SIM_TIME):
    os.system(f"../ns3 run 'vanet-routing-compare --totaltime={SIM_TIME} --nodes={num_cars} --CSVfileName=ns-3_script/pdrVScars/{num_cars}cars.csv --CSVfileName=ns-3_script/pdrVScars/{num_cars}cars_summary.csv' > /dev/null 2>&1")
    queue.put(num_cars)

if __name__ == "__main__":
    if not os.path.exists("pdrVScars"):
        print("Creating pdrVScars directory...")
        os.mkdir("pdrVScars")

    if args.process_only == False:

        print("What settings do you wish to use?")
        print("Please enter settings with the folowing format: sim_time min_cars max_cars step")
        settings_input = input("Settings: ")
        settings = settings_input.split(' ')
        if len(settings) != 4:
            print("Not enough arguments provided, exiting...")
            exit()
        SIM_TIME = int(settings[0])
        MIN_CARS = int(settings[1])
        MAX_CARS = int(settings[2])
        STEP = int(settings[3])
        cars = list(range(MIN_CARS, MAX_CARS + 1, STEP))

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

        queue = multiprocessing.Queue()
        processes = []
        for num_cars in cars:
            process = multiprocessing.Process(target=run_sim, args=(num_cars, queue, SIM_TIME))
            process.start()
            processes.append(process)

        # Update progress bar
        for i in tqdm(range(len(cars)), ascii=False):
            process_num = queue.get()
            tqdm.write(f"Thread w/ {process_num} cars just finished...")

        # Wait for all processs to finish
        for process in processes:
            process.join()
        print("\nAll processs finished...")

    # process and graph data
    sns.set_style("whitegrid")
    plt.figure(figsize=(10,6))
    loc_list = ["SimulationSecond", "BSM_PDR4"]
    dir_path = "./pdrVScars"

    dir_path = "./pdrVScars"
    file_paths = []
    for file_name in os.listdir(dir_path):
        file_paths.append(os.path.join(dir_path, file_name))
    sorted_file_paths = sorted(file_paths, key=lambda x: int(x.split('/')[-1].split('cars')[0]))

    for file_path in sorted_file_paths:
        if os.path.isfile(file_path):
            print(f"\nReading file: {file_path}")
            df = pd.read_csv(file_path)
            selected_columns = df.loc[:, loc_list]
            print(selected_columns)
            label = file_path.split('/')[2].split('c')[0]
            sns.lineplot(data=selected_columns.iloc[:, 1], label=f'{label} Cars')

    plt.title('BSM PDR for 10 Simulations')
    plt.xlabel('Simulation Time')
    plt.ylabel('Packet Delivery Ratio')
    plt.show()


