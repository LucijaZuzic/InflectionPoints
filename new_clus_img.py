import os
import pandas as pd
import matplotlib.pyplot as plt

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

plt.figure()
color_list = []
ix = 0
for num in range(16, 256, 2):
    print("#" +str(hex(num)).replace("0x", "") * 3)
    color_list.append("#" +str(hex(num)).replace("0x", "") * 3)
    plt.scatter(ix, ix, color = "#" + str(hex(num)).replace("0x", "") * 3)
    ix += 1
plt.show()
plt.close()

color_used = [color_list[0]]
while len(color_used) != len(color_list):
    color_curr = color_used[-1]
    color_diff = 0
    color_add = color_curr
    for color_other in color_list:
        if abs(int(color_curr.replace("#", "0x")[:4], 16) - int(color_other.replace("#", "0x")[:4], 16)) > color_diff and color_other not in color_used:
            color_add = color_other
            color_diff = abs(int(color_curr.replace("#", "0x")[:4], 16) - int(color_add.replace("#", "0x")[:4], 16))
    color_used.append(color_add)

plt.figure()
ix = 0
for num in range(len(color_used)):
    print(color_used[num], int(color_used[num].replace("#", "0x")[:4], 16))
    plt.scatter(ix, ix, color = color_used[num])
    ix += 1
plt.show()
plt.close()

for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        if "_all_percent_1_20" not in csv_file and "_all_percent_1_10" not in csv_file:
            
            continue

        print(csv_file) 

        for algo in ["DBSCAN", "KMeans"]:

            image_names = []

            for num_clus in list_clus:

                if not os.path.isdir("clustered/" + algo + "/" + str(num_clus) + "/" + subdir_name):
                    
                    os.makedirs("clustered/" + algo + "/" + str(num_clus) + "/" + subdir_name)  
                
                new_name_csv = "clustered/" + algo + "/" + str(num_clus) + "/" + subdir_name + "/clustered_" + algo + "_" + str(num_clus) + "_" + csv_file

                csv_df = pd.read_csv(new_name_csv)

                comp1 = csv_df["TSNE_f1"]
                comp2 = csv_df["TSNE_f2"]
                cluster = csv_df["cluster"]

                print(new_name_csv, algo, num_clus, len(set(csv_df["cluster"])), -1 in set(cluster))

                point_dict = dict()
                
                for ix_point in range(len(comp1)):
                    if cluster[ix_point] not in point_dict:
                        point_dict[cluster[ix_point]] = {"x": [], "y": []}
                    point_dict[cluster[ix_point]]["x"].append(comp1[ix_point])
                    point_dict[cluster[ix_point]]["y"].append(comp2[ix_point])
                    
                plt.figure()
                plt.title(algo + " " + str(num_clus))
                plt.xlabel("TSNE f1")
                plt.ylabel("TSNE f2")
                plt.fill_between([min(comp1), max(comp1)], min(comp2), max(comp2), color = "blue")
                for cluster_num in cluster:
                    plt.scatter(point_dict[cluster_num]["x"], point_dict[cluster_num]["y"], color = color_used[cluster_num + 1 * (-1 in set(cluster))])
                plt.show()
                plt.close()