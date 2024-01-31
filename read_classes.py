from utilities import * 

def save_distances(all_dict, markers_d, begin_name):
 
    list_keys = sorted([str(m) for m in list(all_dict[ws].keys())])

    print(len(list_keys))
  
    strpr = "vehicle;ride;ws"

    for mrk in list_keys:

        strpr += ";" + mrk 

    strpr += "\n"

    for subdir_name in markers_d[ws]:

        for short_name in markers_d[ws][subdir_name]:

            strpr += subdir_name + ";" + short_name + ";" + str(ws)

            for mrk in list_keys:

                cnt = 0

                if mrk in markers_d[ws][subdir_name][short_name]:

                    cnt = markers_d[ws][subdir_name][short_name][mrk]
 
                strpr += ";" + str(cnt)
  
            strpr += "\n"

    dirname = "marker_count/" + begin_name

    if not os.path.isdir(dirname):

        os.makedirs(dirname)

    file_distances = open(dirname + "/marker_" + begin_name + "_" + str(ws) + ".csv", "w")
    
    file_distances.write(strpr)

    file_distances.close()

all_subdirs = os.listdir() 
   
all_markers_dict = dict()

all_markers_converted_dict = dict()

all_markers_anom_dict = dict() 

markers_dict = dict() 

markers_percent_dict = dict()

markers_converted_dict = dict() 

markers_converted_percent_dict = dict()

markers_anom_dict = dict() 

markers_anom_percent_dict = dict()

for ws in range(5, 25, 5):

    all_markers_dict[ws] = dict()

    all_markers_converted_dict[ws] = dict()

    all_markers_anom_dict[ws] = dict()

    markers_dict[ws] = dict()

    markers_percent_dict[ws] = dict() 

    markers_converted_dict[ws] = dict() 

    markers_converted_percent_dict[ws] = dict()
    
    markers_anom_dict[ws] = dict() 

    markers_anom_percent_dict[ws] = dict() 

    for subdir_name in all_subdirs:
  
        markers_dict[ws][subdir_name] = dict()

        markers_percent_dict[ws][subdir_name] = dict()

        markers_converted_dict[ws][subdir_name] = dict()

        markers_converted_percent_dict[ws][subdir_name] = dict()

        markers_anom_dict[ws][subdir_name] = dict()

        markers_anom_percent_dict[ws][subdir_name] = dict()
            
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:

            continue 

        print(subdir_name)

        all_files = os.listdir(subdir_name + "/cleaned_csv/") 

        for some_file in all_files:   

            file_with_ride = pd.read_csv("markers/" + subdir_name + "/" + str(ws) + "/" + some_file, sep = ";", index_col = False)
    
            short_name = some_file.replace(".csv", "".replace("events_", ""))

            markers_list = list(file_with_ride["marker"])

            markers_set = set(file_with_ride["marker"])

            markers_converted_list = []

            markers_anom_list = []

            for mrk in markers_list:

                mrk_set = sorted(list(set(str(mrk))))

                mrk_str = ""

                for m in mrk_set:

                    mrk_str += m

                if str(mrk) == "nan":

                    mrk_str = "nan"

                is_anom = "non_anom"

                for l in mrk_str:

                    if l != "e" and l != "d":

                        is_anom = "anom"

                if str(mrk) == "nan":

                    is_anom = "non_anom"

                markers_converted_list.append(mrk_str)

                markers_anom_list.append(is_anom)

            markers_converted_set = set(markers_converted_list)

            markers_anom_set = set(markers_anom_list)
 
            markers_dict[ws][subdir_name][short_name] = {mrk: markers_list.count(mrk) for mrk in markers_set}
    
            markers_percent_dict[ws][subdir_name][short_name] = {mrk: markers_list.count(mrk) / len(markers_list) for mrk in markers_set}

            markers_converted_dict[ws][subdir_name][short_name] = {mrk: markers_converted_list.count(mrk) for mrk in markers_converted_set}
    
            markers_converted_percent_dict[ws][subdir_name][short_name] = {mrk: markers_converted_list.count(mrk) / len(markers_converted_list) for mrk in markers_converted_set}

            markers_anom_dict[ws][subdir_name][short_name] = {mrk: markers_anom_list.count(mrk) for mrk in markers_anom_set}
    
            markers_anom_percent_dict[ws][subdir_name][short_name] = {mrk: markers_anom_list.count(mrk) / len(markers_anom_list) for mrk in markers_anom_set}

            for mrk in markers_dict[ws][subdir_name][short_name]:

                if mrk not in all_markers_dict[ws]:

                    all_markers_dict[ws][mrk] = 0

                all_markers_dict[ws][mrk] += markers_dict[ws][subdir_name][short_name][mrk] 

            for mrk in markers_converted_dict[ws][subdir_name][short_name]:

                if mrk not in all_markers_converted_dict[ws]:

                    all_markers_converted_dict[ws][mrk] = 0

                all_markers_converted_dict[ws][mrk] += markers_converted_dict[ws][subdir_name][short_name][mrk] 
  
            for mrk in markers_anom_dict[ws][subdir_name][short_name]:

                if mrk not in all_markers_anom_dict[ws]:

                    all_markers_anom_dict[ws][mrk] = 0

                all_markers_anom_dict[ws][mrk] += markers_anom_dict[ws][subdir_name][short_name][mrk] 

    save_distances(all_markers_dict, markers_percent_dict, "all")

    save_distances(all_markers_converted_dict, markers_converted_percent_dict, "converted")

    save_distances(all_markers_anom_dict, markers_anom_percent_dict, "anom")