from utilities import *
import seaborn as sns
  
for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue

        if "_percent_1_5" not in csv_file:
            
            continue 

        file_csv = pd.read_csv("marker_count/" + subdir_name + "/" + csv_file, sep = ";", index_col = False)
 
        colname_sum = dict()

        for colname in file_csv.columns[4:]:

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

        save_object("marker_count/" + subdir_name + "/" + csv_file.replace(".csv", ".npy"), distances_np)
  
        #sns.heatmap(distances_np) 

        #plt.show()

        name_find = "Vehicle_10/events_8377353"

        ix = names_for_dist.index(name_find)
    
        sort_distances = sorted([(distances_np[ix, colnum], names_for_dist[colnum]) for colnum in range(len(distances_np))])

        print(sort_distances[1:11])
        print(sort_distances[1], sort_distances[-1])

        #for rownum in range(len(distances_np)):

            #sort_distances = sorted([(distances_np[rownum, colnum], names_for_dist[colnum]) for colnum in range(len(distances_np))])