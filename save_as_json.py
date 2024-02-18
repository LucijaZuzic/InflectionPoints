from utilities import *

import json

all_subdirs = os.listdir()
 
dict_all_all_data = {"vehicles": []}

dict_all_all_no_data = {"vehicles": []}

for subdir_name in all_subdirs:
        
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    print(subdir_name)

    is_ok = False

    vehicle_no = int(subdir_name.split("_")[-1])

    dict_all_all_data["vehicles"].append({"vehicle": vehicle_no, "rides": []})

    dict_all_all_no_data["vehicles"].append({"vehicle": vehicle_no, "rides": []})

    dict_all_subdir_data = {"vehicles": [{"vehicle": vehicle_no, "rides": []}]}

    dict_all_subdir_no_data = {"vehicles": [{"vehicle": vehicle_no, "rides": []}]}
    
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 

    bad_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
 
    for some_file in all_files:    
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames and bad_rides_filenames[subdir_name + "/cleaned_csv/" + some_file] != -4:
            continue

        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)

        ride_no = int(some_file.replace(".csv", "").split("_")[-1])

        dict_all_all_data["vehicles"][-1]["rides"].append({"ride": ride_no, "data": []})

        dict_all_subdir_data["vehicles"][-1]["rides"].append({"ride": ride_no, "data": []})

        dict_all_data = {"vehicles": [{"vehicle": vehicle_no, "rides": [{"ride": ride_no, "data": []}]}]} 

        dict_all_all_no_data["vehicles"][-1]["rides"].append({"ride": ride_no})

        dict_all_subdir_no_data["vehicles"][-1]["rides"].append({"ride": ride_no})

        dict_all_no_data = {"vehicles": [{"vehicle": vehicle_no, "rides": [{"ride": ride_no}]}]} 

        longitudes = list(file_with_ride["fields_longitude"])  
        latitudes = list(file_with_ride["fields_latitude"]) 
        times = list(file_with_ride["time"])
 
        for ix in range(len(longitudes)): 

            dict_all_data["vehicles"][-1]["rides"][-1]["data"].append({"index": ix, "longitude": longitudes[ix], "latitude": latitudes[ix], "time": times[ix]})
            
            dict_all_subdir_data["vehicles"][-1]["rides"][-1]["data"].append({"index": ix, "longitude": longitudes[ix], "latitude": latitudes[ix], "time": times[ix]})

            dict_all_all_data["vehicles"][-1]["rides"][-1]["data"].append({"index": ix, "longitude": longitudes[ix], "latitude": latitudes[ix], "time": times[ix]})

            is_ok = True
        
        new_dir = "cleaned_json/" + str(vehicle_no) + "/" + str(ride_no)

        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)

        with open(new_dir + "/" + str(vehicle_no) + "_" + str(ride_no) + ".json", "w") as outfile: 
            json.dump(dict_all_data, outfile)

        new_dir_no_data = "cleaned_json_no_data/" + str(vehicle_no) + "/" + str(ride_no)

        if not os.path.isdir(new_dir_no_data):
            os.makedirs(new_dir_no_data)

        with open(new_dir_no_data + "/" + str(vehicle_no) + "_" + str(ride_no) + "_no_data.json", "w") as outfile: 
            json.dump(dict_all_no_data, outfile)

    if is_ok:
        with open("cleaned_json/" + str(vehicle_no) + "/all_data_" + str(vehicle_no) + ".json", "w") as outfile: 
            json.dump(dict_all_subdir_data, outfile)

        with open("cleaned_json_no_data/" + str(vehicle_no) + "/all_data_" + str(vehicle_no) + "_no_data.json", "w") as outfile: 
            json.dump(dict_all_subdir_no_data, outfile)

with open("all_data.json", "w") as outfile: 
    json.dump(dict_all_all_data, outfile)

with open("all_no_data.json", "w") as outfile: 
    json.dump(dict_all_all_no_data, outfile)