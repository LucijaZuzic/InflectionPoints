import os
import pandas as pd
import matplotlib.pyplot as plt

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

plt.figure()
ix = 0
red_list = []
green_list = []
blue_list = []
cyan_list = []
magenta_list = []
yellow_list = []
for num in range(19, -1, -1):
    component = str(hex(135 + num * 6)).replace("0x", "")
    while len(component) < 2:
        component = "0" + component
    red_list.append("#" + component + "00" * 2)
    plt.scatter(ix, ix, color = "#" + component + "00" * 2)
    green_list.append("#00" + component + "00")
    plt.scatter(20 + ix, 20 + ix, color = "#00" + component + "00")
    blue_list.append("#0000" + component)
    plt.scatter(40 + ix, 40 +  ix, color = "#0000" + component)
    cyan_list.append("#00" + component * 2)
    plt.scatter(60 + ix, 60 + ix, color = "#00" + component * 2)
    magenta_list.append("#" + component + "00" + component)
    plt.scatter(80 + ix, 80 + ix, color = "#" + component + "00" + component)
    yellow_list.append("#" + component * 2 + "00")
    plt.scatter(100 + ix, 100 + ix, color = "#" + component * 2 + "00")
    ix += 1
#plt.show()
plt.close()

color_used = []
step = len(blue_list)
while len(color_used) < 6 * len(blue_list) and step >= 1:
    for sp in range(0, len(blue_list), step):
        if blue_list[sp] not in color_used:
            color_used.append(blue_list[sp])
        if yellow_list[sp] not in color_used:
            color_used.append(yellow_list[sp])
        if cyan_list[sp] not in color_used:
            color_used.append(cyan_list[sp])
        if magenta_list[sp] not in color_used:
            color_used.append(magenta_list[sp])
        if red_list[sp] not in color_used:
            color_used.append(red_list[sp])
        if green_list[sp] not in color_used:
            color_used.append(green_list[sp])
    step = step // 2

plt.figure()
ix = 0
for num in range(len(color_used)):
    plt.scatter(ix, ix, color = color_used[num])
    ix += 1
#plt.show()
plt.close()

dict_for_plot = dict()
maxcoord_algo_ws_num_clus = dict()
maxcoord_algo_ws = dict()
maxcoord_algo = dict()
maxcoord = {"x": (1000000, -1000000), "y": (1000000, -1000000)}

for ws in [10, 20]:

    for algo in ["DBSCAN", "KMeans"]:

        image_names = []

        for num_clus in list_clus:

            if not os.path.isdir("clustered/" + algo + "/" + str(num_clus) + "/all_percent_1"):
                
                os.makedirs("clustered/" + algo + "/" + str(num_clus) + "/all_percent_1")  
            
            new_name_csv = "clustered/" + algo + "/" + str(num_clus) + "/all_percent_1/clustered_" + algo + "_" + str(num_clus) + "_marker_all_percent_1_" + str(ws) + ".csv"

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

            if algo not in maxcoord_algo_ws_num_clus:
                maxcoord_algo_ws_num_clus[algo] = dict()
            if ws not in maxcoord_algo_ws_num_clus[algo]:
                maxcoord_algo_ws_num_clus[algo][ws] = dict()
            if num_clus not in maxcoord_algo_ws_num_clus[algo][ws]:
                maxcoord_algo_ws_num_clus[algo][ws][num_clus] = {"x": (1000000, -1000000), "y": (1000000, -1000000)}
            maxcoord_algo_ws_num_clus[algo][ws][num_clus]["x"] = (min(maxcoord_algo_ws_num_clus[algo][ws][num_clus]["x"][0], min(comp1)), max(maxcoord_algo_ws_num_clus[algo][ws][num_clus]["x"][1], max(comp2)))
            maxcoord_algo_ws_num_clus[algo][ws][num_clus]["y"] = (min(maxcoord_algo_ws_num_clus[algo][ws][num_clus]["y"][0], min(comp2)), max(maxcoord_algo_ws_num_clus[algo][ws][num_clus]["y"][1], max(comp2)))

            if algo not in maxcoord_algo_ws:
                maxcoord_algo_ws[algo]= dict()
            if ws not in maxcoord_algo_ws[algo]:
                maxcoord_algo_ws[algo][ws] = {"x": (1000000, -1000000), "y": (1000000, -1000000)}
            maxcoord_algo_ws[algo][ws]["x"] = (min(maxcoord_algo_ws[algo][ws]["x"][0], min(comp1)), max(maxcoord_algo_ws[algo][ws]["x"][1], max(comp2)))
            maxcoord_algo_ws[algo][ws]["y"] = (min(maxcoord_algo_ws[algo][ws]["y"][0], min(comp2)), max(maxcoord_algo_ws[algo][ws]["y"][1], max(comp2)))
            
            if algo not in maxcoord_algo:
                maxcoord_algo[algo] = {"x": (1000000, -1000000), "y": (1000000, -1000000)}
            maxcoord_algo[algo]["x"] = (min(maxcoord_algo[algo]["x"][0], min(comp1)), max(maxcoord_algo[algo]["x"][1], max(comp2)))
            maxcoord_algo[algo]["y"] = (min(maxcoord_algo[algo]["y"][0], min(comp2)), max(maxcoord_algo[algo]["y"][1], max(comp2)))
            
            maxcoord["x"] = (min(maxcoord["x"][0], min(comp1)), max(maxcoord["x"][1], max(comp2)))
            maxcoord["y"] = (min(maxcoord["y"][0], min(comp2)), max(maxcoord["y"][1], max(comp2)))

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

            if ws not in dict_for_plot[algo]:
                dict_for_plot[algo][ws] = dict()

            dict_for_plot[algo][ws][num_clus] = {
                "point_dict": point_dict,
                "cluster_zorder": cluster_zorder
            }

mintotal = min(maxcoord["x"][0], maxcoord["y"][0])
maxtotal = max(maxcoord["x"][1], maxcoord["y"][1])

for ws in [10, 20]:
    for algo in dict_for_plot:
        plt.figure(figsize = (8, 5), dpi = 600)
        plt.rcParams.update({"font.size": 5})
        ix_ord = 1
        for num_clus in dict_for_plot[algo][ws]:
            point_dict = dict_for_plot[algo][ws][num_clus]["point_dict"]
            cluster_zorder = dict_for_plot[algo][ws][num_clus]["cluster_zorder"]
            plt.subplot(5, 8, ix_ord)
            row = (ix_ord - 1) // 8
            col = (ix_ord - 1) % 8
            fig = plt.gcf()
            ax = fig.gca()
            ax.axes.set_aspect('equal')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            if ix_ord % 8 != 1:
                ax.spines['left'].set_visible(False)
                plt.yticks([])
            else:
                if row == 2:
                    plt.ylabel("TSNE 2")
            if row != 4:
                ax.spines['bottom'].set_visible(False)
                plt.xticks([])
            else:
                if col == 3:
                    plt.xlabel("TSNE 1")
            plt.xlim(mintotal, maxtotal)
            plt.ylim(mintotal, maxtotal)
            if row == 0 and col == 3:
                plt.title(algo.replace("KMeans", "K-means") + " Window size " + str(ws))
            if algo == "DBSCAN":    
                plt.text(mintotal, maxtotal, str(num_clus) + " points")
            else:
                plt.text(mintotal, maxtotal, str(num_clus) + " clusters")
            num_added = set()
            for color_num in range(len(color_used)):
                cluster_num = color_num - 1 * (-1 in point_dict)
                if cluster_num in point_dict:
                    plt.scatter(point_dict[cluster_num]["x"],
                                point_dict[cluster_num]["y"],
                                s = 1,
                                zorder = cluster_zorder[cluster_num],
                                c = color_used[color_num],
                                label = str(color_num + 1))
                else:
                    plt.scatter(0,
                                0,
                                s = 1,
                                zorder = 2,
                                c = color_used[color_num],
                                label = str(color_num + 1))
            if row == 4 and col == 0:
                plt.legend(ncol = 15, loc = "lower left", bbox_to_anchor = (-0.5, -2))
            ix_ord += 1
        #plt.show()
        plt.savefig(algo + "_" + str(ws) + "_all.png", bbox_inches = "tight")
        plt.close()