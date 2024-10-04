import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

color_used = ["#0000ff", "#ffff00"]

dict_for_plot = dict()
maxcoord_algo_ws_num_clus = dict()
maxcoord_algo_ws = dict()
maxcoord_algo = dict()
maxcoord = {"x": (1000000, -1000000), "y": (1000000, -1000000)}

for ws in [10, 20]:

    for algo in ["DBSCAN", "KMeans"]:

        for num_clus in list_clus:

            if not os.path.isdir("clustered/" + algo + "/" + str(num_clus) + "/all_percent_1"):
                
                os.makedirs("clustered/" + algo + "/" + str(num_clus) + "/all_percent_1")  
            
            new_name_csv = "clustered/" + algo + "/" + str(num_clus) + "/all_percent_1/clustered_" + algo + "_" + str(num_clus) + "_marker_all_percent_1_" + str(ws) + ".csv"

            csv_df = pd.read_csv(new_name_csv)

            comp1 = csv_df["TSNE_f1"]
            comp2 = csv_df["TSNE_f2"]
            cluster = csv_df["cluster"]
            
            cluster_size = {c: list(cluster).count(c) for c in list(cluster)}

            cluster_size_keys = list(cluster_size.keys())
            cluster_size_values= list(cluster_size.values())
            max_key_ix = np.argmax(cluster_size_values)
            max_key = cluster_size_keys[max_key_ix]

            point_dict = dict()

            for ix_point in range(len(comp1)):
                marker = 0
                if cluster[ix_point] != max_key:
                    marker = 1
                if marker not in point_dict:
                    point_dict[marker] = {"x": [], "y": []}
                point_dict[marker]["x"].append(comp1[ix_point])
                point_dict[marker]["y"].append(comp2[ix_point])

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

            if algo not in dict_for_plot:
                dict_for_plot[algo] = dict()

            if ws not in dict_for_plot[algo]:
                dict_for_plot[algo][ws] = dict()

            dict_for_plot[algo][ws][num_clus] = {
                "point_dict": point_dict
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
            for cluster_num in range(len(color_used)):
                label_cluster_num = "Normal"
                if cluster_num == 1:
                    label_cluster_num = "Anomaly"
                if cluster_num in point_dict:
                    plt.scatter(point_dict[cluster_num]["x"],
                                point_dict[cluster_num]["y"],
                                s = 1,
                                zorder = 4 - cluster_num,
                                c = color_used[cluster_num],
                                label = label_cluster_num)
                else:
                    plt.scatter(0,
                                0,
                                s = 1,
                                zorder = 2,
                                c = color_used[cluster_num],
                                label = label_cluster_num)
            if row == 4 and col == 0:
                plt.legend(ncol = 2, loc = "lower left", bbox_to_anchor = (-0.5, -0.75))
            ix_ord += 1
        #plt.show()
        plt.savefig(algo + "_" + str(ws) + "_all_2.png", bbox_inches = "tight")
        plt.close()