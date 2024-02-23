from utilities import *

import json
 
for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        file_csv = pd.read_csv("marker_count/" + subdir_name + "/" + csv_file, sep = ";", index_col = False)
 
        colname_sum = dict()

        for colname in file_csv.columns[3:]:

            colname_sum[colname] = sum(file_csv[colname])

        set_used = set()

        for val in dict(sorted(colname_sum.items(), key = lambda item: item[1], reverse = True)):

            if len(set_used) == 200:

                break

            else:

                set_used.add(val) 

        rows_for_dist = []

        names_for_dist = []

        for i in range(len(file_csv["vehicle"])):

            names_for_dist.append(file_csv["vehicle"][i] + "/" + file_csv["ride"][i])

            rows_for_dist.append([])

            for val in sorted(list(set_used)):

                rows_for_dist[-1].append(file_csv[val][i])
            
            rows_for_dist[-1] = np.array(rows_for_dist[-1])
  
        rows_for_dist = np.array(rows_for_dist)

        distances_np = np.linalg.norm(rows_for_dist[:, None] - rows_for_dist, axis = 2)
    
        usable_indexes_all = {"compare_to": []}

        for ix in range(len(distances_np)):
 
            sort_distances = sorted([(distances_np[ix, colnum], names_for_dist[colnum]) for colnum in range(len(distances_np))]) 

            vehicle_name_started = names_for_dist[ix].split("/")
            
            vehicle_started = int(vehicle_name_started[0].split("_")[1])

            ride_started = int(vehicle_name_started[1].split("_")[1])

            usable_indexes_all["compare_to"].append({"index": ix, "vehicle": vehicle_started, "ride": ride_started, "similar": []})

            for ix_use in range(1, len(sort_distances), int(np.floor(len(sort_distances) // 19))):

                vehicle_name = sort_distances[ix_use][1].split("/")

                vehicle_use = int(vehicle_name[0].split("_")[1])

                ride_use = int(vehicle_name[1].split("_")[1])
 
                usable_indexes_all["compare_to"][-1]["similar"].append({"order": ix_use, "compare_vehicle": vehicle_use, "compare_ride": ride_use})
                
        print(usable_indexes_all)  

        if not os.path.isdir("most_similar/" + subdir_name):
            os.makedirs("most_similar/" + subdir_name)

        with open("most_similar/" + subdir_name + "/" + csv_file.replace("csv", "json"), "w") as outfile: 
            json.dump(usable_indexes_all, outfile)