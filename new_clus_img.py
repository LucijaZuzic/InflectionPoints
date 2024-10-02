import os
import pandas as pd
import matplotlib.pyplot as plt

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

plt.figure()
ix = 0
blue_list = []
yellow_list = []
gray_list = []
for num in range(40):
    light_part = str(hex(248 - num * 6)).replace("0x", "")
    while len(light_part) < 2:
        light_part = "0" + light_part
    dark_part = str(hex(8 + num * 6)).replace("0x", "")
    while len(dark_part) < 2:
        dark_part = "0" + dark_part
    blue_list.append("#0000" + light_part)
    plt.scatter(ix, ix, color = "#0000" + light_part)
    yellow_list.append("#" + light_part * 2 + "00")
    plt.scatter(ix + 40, ix + 40, color = "#" + light_part * 2 + "00")
    gray_list.append("#" + dark_part * 3)
    plt.scatter(ix + 80, ix + 80, color = "#" + dark_part * 3)
    ix += 1
plt.show()
plt.close()

color_used = []
step = len(yellow_list)
while len(color_used) < 3 * len(yellow_list) and step >= 1:
    step = step // 2
    for sp in range(0, len(yellow_list), step):
        if blue_list[sp] not in color_used:
            color_used.append(blue_list[sp])
        if yellow_list[sp] not in color_used:
            color_used.append(yellow_list[sp])
        if gray_list[sp] not in color_used:
            color_used.append(gray_list[sp])

plt.figure()
ix = 0
for num in range(len(color_used)):
    plt.scatter(ix, ix, color = color_used[num])
    ix += 1
plt.show()
plt.close()

dict_for_plot = dict()

for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        if "_all_percent_1_20" not in csv_file and "_all_percent_1_10" not in csv_file:
            
            continue

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

                point_dict = dict()
                
                for ix_point in range(len(comp1)):
                    if cluster[ix_point] not in point_dict:
                        point_dict[cluster[ix_point]] = {"x": [], "y": []}
                    point_dict[cluster[ix_point]]["x"].append(comp1[ix_point])
                    point_dict[cluster[ix_point]]["y"].append(comp2[ix_point])

                cluster_size = {c: len(point_dict[c]["x"]) for c in point_dict}

                min_zorder = 3
                cluster_zorder = dict()
                for size in sorted(list(cluster_size.values()), reverse = True):
                    for cluster_name in cluster_size:
                        if cluster_size[cluster_name] == size and cluster_name not in cluster_zorder:
                            cluster_zorder[cluster_name] = min_zorder
                            min_zorder += 1

                if algo not in dict_for_plot:
                    dict_for_plot[algo] = dict()

                dict_for_plot[algo][num_clus] = {
                    "point_dict": point_dict,
                    "cluster_zorder": cluster_zorder
                }

for algo in dict_for_plot:
    plt.figure()
    ix_ord = 1
    for num_clus in dict_for_plot[algo]:
        point_dict = dict_for_plot[algo][num_clus]["point_dict"]
        cluster_zorder = dict_for_plot[algo][num_clus]["cluster_zorder"]
        plt.subplot(8, 5, ix_ord)
        plt.title(algo + " " + str(num_clus))
        plt.xlabel("TSNE 1")
        plt.ylabel("TSNE 2")
        num_added = set()
        for color_num in range(len(color_used)):
            cluster_num = color_num - 1 * (-1 in point_dict)
            if cluster_num in point_dict:
                plt.scatter(point_dict[cluster_num]["x"], point_dict[cluster_num]["y"], 
                            zorder = cluster_zorder[cluster_num], 
                            edgecolor = color_used[color_num], 
                            facecolor = color_used[color_num], 
                            label = str(color_num + 1))
            else:
                plt.scatter(0, 0, 
                            zorder = 2, 
                            edgecolor = color_used[color_num], 
                            facecolor = color_used[color_num],
                            label = str(color_num + 1))
        if ix_ord == 36:
            plt.legend(ncol = 10)
        ix_ord += 1
    plt.show()
    plt.close()