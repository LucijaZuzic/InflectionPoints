from utilities import *
import seaborn as sns

all_subdirs = os.listdir() 
   
all_markers_dict = dict()

markers_dict = dict()

for ws in range(5, 25, 5):

    all_markers_dict[ws] = dict()

    markers_dict[ws] = dict()

    for subdir_name in all_subdirs:
  
        markers_dict[ws][subdir_name] = dict()
            
        if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
            continue 
        print(subdir_name)

        all_files = os.listdir(subdir_name + "/cleaned_csv/") 

        for some_file in all_files:   

            file_with_ride = pd.read_csv("markers/" + subdir_name + "/" + str(ws) + "/" + some_file, sep = ";", index_col = False)
    
            short_name = some_file.replace(".csv", "".replace("events_", ""))

            markers_list = list(file_with_ride["marker"])

            markers_set = set(file_with_ride["marker"])

            markers_dict[ws][subdir_name][short_name] = {mrk: markers_list.count(mrk) / len(markers_list) for mrk in markers_set}
  
            for mrk in markers_dict[ws][subdir_name][short_name]:

                if mrk not in all_markers_dict[ws]:

                    all_markers_dict[ws][mrk] = 0

                all_markers_dict[ws][mrk] += markers_dict[ws][subdir_name][short_name][mrk]

            #chr_list = [hex(c)[-1] for c in range(16)]

            #chrs_of_len = ['']

            #len_reached = 0

            #for x in range(ws):

                #chrs_of_len = [c1 + c2 for c1 in chr_list for c2 in chrs_of_len]
            
            #print(len(chrs_of_len)) 
         
    for mrkr in all_markers_dict[ws]:

        if all_markers_dict[ws][mrkr] > 10:
 
            print(mrkr, all_markers_dict[ws][mrkr])

    print(len(all_markers_dict[ws]))

    list_keys = sorted([str(mrk) for mrk in list(all_markers_dict[ws].keys())])

    strpr = "vehicle;ride;ws"

    for mrk in list_keys:

        strpr += ";" + mrk 

    strpr += "\n"

    rows_for_dist = []

    names_for_dist = []

    for subdir_name in markers_dict[ws]:

        for short_name in markers_dict[ws][subdir_name]:

            strpr += subdir_name + ";" + short_name + ";" + str(ws)

            names_for_dist.append(subdir_name + "/" + str(ws) + "/" + short_name)

            rows_for_dist.append([])

            for mrk in list_keys:

                cnt = 0

                if mrk in markers_dict[ws][subdir_name][short_name]:

                    cnt = markers_dict[ws][subdir_name][short_name][mrk]

                strpr += ";" + str(cnt)

                rows_for_dist[-1].append(cnt)

            rows_for_dist[-1] = np.array(rows_for_dist[-1])

            strpr += "\n"

    #file_distances = open("marker_distances_" + str(ws) + ".csv", "w")
    
    #file_distances.write(strpr)

    #file_distances.close()

    rows_for_dist = np.array(rows_for_dist)

    distances_np = np.linalg.norm(rows_for_dist[:, None] - rows_for_dist, axis = 2)

    print(np.shape(distances_np))
    sns.heatmap(distances_np) 
    plt.show()

    for rownum in range(len(distances_np)):
        sort_distances = sorted([(distances_np[rownum, colnum], names_for_dist[colnum]) for colnum in range(len(distances_np))])
        print(sort_distances[1:11])

    break