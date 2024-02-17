from utilities import *

all_subdirs = os.listdir()
ws = 5
 
classes = {"I": 0, "D": 0, "NF": 0, "NM": 0}
num_infls_long = dict()
num_infls_lat = dict()
num_infls_all = dict()
num_infls_mrkr = dict()

anomaly_classes = set()
non_anomaly_classes = set()
 
for subdir_name in all_subdirs:
        
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    print(subdir_name)
    
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 

    bad_rides_filenames = dict()
    if os.path.isfile(subdir_name + "/bad_rides_filenames"):
        bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")
 
    for some_file in all_files:    
        if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames and bad_rides_filenames[subdir_name + "/cleaned_csv/" + some_file] != -4:
            continue

        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)

        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"])  
        times = list(file_with_ride["time"])
        times_processed = [process_time(time_new) for time_new in times]  
 
        order_of_mrkrs = dict()

        for x in range(0, len(longitudes) - ws + 1):
            long = longitudes[x:x + ws]
            lat = latitudes[x:x + ws] 
            tms = times_processed[x:x + ws] 
            tms_delays = [tms[time_index + 1] - tms[time_index] for time_index in range(len(tms) - 1)] 
 
            long_diff = [long[i] - long[0] for i in range(len(long))]
            lat_diff = [lat[i] - lat[0] for i in range(len(long))] 
            points = set([(long[i], lat[i]) for i in range(len(long))])
              
            angle_all = []
            radius_all = []
            for i in range(1, len(long_diff)):
                radius_all.append(np.sqrt(lat_diff[i] ** 2 + long_diff[i] ** 2)) 
                angle_all.append(np.arctan2(lat_diff[i], long_diff[i])) 

            long_new = [radius_all[i] * np.cos(angle_all[i] - angle_all[-1]) for i in range(len(radius_all))]
            lat_new = [radius_all[i] * np.sin(angle_all[i] - angle_all[-1]) for i in range(len(radius_all))] 
            
            long_new.insert(0, 0)
            lat_new.insert(0, 0)

            long_new, lat_new = preprocess_long_lat(long_new, lat_new)
 
            long_sgn = [long_new[i + 1] > long_new[i] for i in range(len(long_new) - 1)]
            lat_sgn = [lat_new[i + 1] > lat_new[i] for i in range(len(lat_new) - 1)]

            long_change_sgn = [long_sgn[i + 1] != long_sgn[i] for i in range(len(long_sgn) - 1)]
            lat_change_sgn = [lat_sgn[i + 1] != lat_sgn[i] for i in range(len(lat_sgn) - 1)]

            infls_long = []
            infls_lat = []
            infls_long_lat = []
            mrkr = ""
            for i in range(len(long_change_sgn)):
                if long_change_sgn[i] or lat_change_sgn[i] :
                    infls_long_lat.append(i + 1)
                    comp_str_long = str(int(long_sgn[i])) + str(int(long_sgn[i + 1]))
                    comp_str_lat= str(int(lat_sgn[i])) + str(int(lat_sgn[i + 1]))
                    int_comp = int(comp_str_long + comp_str_lat, base = 2)
                    mrkr += str(hex(int_comp))[2:]
                if long_change_sgn[i]:
                    infls_long.append(i + 1)
                if lat_change_sgn[i]:
                    infls_lat.append(i + 1) 

            order_of_mrkrs[x] = (mrkr, max(tms_delays))

            if len(mrkr) > 0:

                is_anom = mrkr[0] != "e"

                if not is_anom:
                    for ch in mrkr:
                        if ch != "d" and ch != "e":
                            is_anom = True
                            break
            
            else:

                is_anom = False

            if is_anom:
                anomaly_classes.add(mrkr)
            else:
                non_anomaly_classes.add(mrkr)
 
        if not os.path.isdir("markers/" + subdir_name + "/" + str(ws)):
            os.makedirs("markers/" + subdir_name + "/" + str(ws))
            
        strpr = "vehicle;ride;pos;ws;marker;time_delay\n" 
        for x in order_of_mrkrs:
            strpr += subdir_name + ";" + some_file.replace(".csv", "").replace("events_", "") + ";" + str(x) + ";" + str(ws) + ";" + order_of_mrkrs[x][0] + ";" + str(order_of_mrkrs[x][1]) + "\n"
        
        file_marker = open("markers/" + subdir_name + "/" + str(ws) + "/" + some_file, "w")
        file_marker.write(strpr)
        file_marker.close()