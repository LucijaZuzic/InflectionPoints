from utilities import *

import json

all_subdirs = os.listdir()

file_all_short = open("all_data_short.json")

usable_ride = []
data_all_short = json.load(file_all_short)
for veh in data_all_short["vehicles"]:
    for ride in veh["rides"]:
        usable_ride.append(ride["ride"])
file_all_short.close()
 
for subdir_name in all_subdirs:
        
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue
    print(subdir_name)

    is_ok = False

    vehicle_no = int(subdir_name.split("_")[-1]) 

    all_files = os.listdir(subdir_name + "/cleaned_csv/") 

    bad_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")

    for some_file in all_files:    
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames and bad_rides_filenames[subdir_name + "/cleaned_csv/" + some_file] != -4:
            continue

        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)

        ride_no = int(some_file.replace(".csv", "").split("_")[-1])

        if ride_no not in usable_ride:
            continue

        longitudes = list(file_with_ride["fields_longitude"])  
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])

        is_ok = is_ok or len(longitudes) > 0
        
        new_dir = "cleaned_png_small/"

        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)

        new_file = new_dir + "/" + str(vehicle_no) + "_" + str(ride_no) + ".png" 

        xrange = max(longitudes) - min(longitudes)
        yrange = max(latitudes) - min(latitudes)

        cwidth = 20
        cheight = 20

        plt.figure(figsize = (cwidth, cheight), dpi = 80) 
        plt.axis('off') 
        plt.xlim(min(longitudes), min(longitudes) + max(xrange, yrange))
        plt.ylim(min(latitudes), min(latitudes) + max(xrange, yrange))
        plt.plot(longitudes, latitudes, c = "k", linewidth=10)
        plt.savefig(new_file, bbox_inches = "tight")
        plt.close() 