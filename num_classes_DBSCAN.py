from utilities import * 
import os
from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.manifold import TSNE

def random_colors(num_colors):
    colors_set = []
    for x in range(num_colors):
        string_color = "#"
        while string_color == "#" or string_color in colors_set:
            string_color = "#"
            set_letters = "0123456789ABCDEF"
            for y in range(6):
                string_color += set_letters[np.random.randint(0, 16)]
        colors_set.append(string_color)
    return colors_set

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        if "_all_percent_1_20" not in csv_file and "_all_percent_1_10" not in csv_file:
            
            continue

        file_csv = pd.read_csv("marker_count/" + subdir_name + "/" + csv_file, sep = ";", index_col = False)

        colname_sum = dict()

        sumsums = 0

        for colname in file_csv.columns[3:]:

            colname_sum[colname] = sum(file_csv[colname])

            sumsums += colname_sum[colname]

        set_used = set()

        suma = 0

        for val in dict(sorted(colname_sum.items(), key = lambda item: item[1], reverse = True)):

            if len(set_used) == 200:

                break

            else:

                set_used.add(val)  

                suma += colname_sum[val]

        print(csv_file, len(file_csv.columns[3:]), suma, sumsums, suma / sumsums) 

        X = [] 
        for ix in range(len(file_csv["vehicle"])):
            Xrow = []
            for val in sorted(list(set_used)):
                Xrow.append(file_csv[val][ix])
            X.append(Xrow)
        X = np.array(X)

        for num_clus in list_clus:

            if not os.path.isdir("clustered/DBSCAN/" + str(num_clus) + "/" + subdir_name):
                
                os.makedirs("clustered/DBSCAN/" + str(num_clus) + "/" + subdir_name)  
            
            new_name = "clustered/DBSCAN/" + str(num_clus) + "/" + subdir_name + "/clustered_DBSCAN_" + str(num_clus) + "_" + csv_file
            new_name_png = new_name.replace("csv", "png")
                    
            dbscan = DBSCAN(min_samples=num_clus, eps = 0.05).fit(X)
            X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)
            list_labels = list(dbscan.labels_)
            set_labels = sorted(list(set(list_labels)))
            count_clus = {lab: list_labels.count(lab) for lab in set_labels}
            print(count_clus)
            clusters_x = {lab: [] for lab in set_labels}
            clusters_y = {lab: [] for lab in set_labels}
            random_colors_set = random_colors(len(set_labels))
            for lab in set_labels:
                for ix in range(len(list_labels)):
                    if list_labels[ix] == lab:
                        clusters_x[lab].append(X_embedded[ix][0])
                        clusters_y[lab].append(X_embedded[ix][1])
            
            for ix_lab in range(len(set_labels)):
                lab = set_labels[ix_lab]
                color_use = random_colors_set[ix_lab]
                plt.scatter(clusters_x[lab], clusters_y[lab], c = color_use, label = str(lab))
            plt.axis("off")
            plt.savefig(new_name_png.replace(".png", "_no_legend.png"), bbox_inches = "tight")
            plt.close()

            for ix_lab in range(len(set_labels)):
                lab = set_labels[ix_lab]
                color_use = random_colors_set[ix_lab]
                plt.scatter(clusters_x[lab], clusters_y[lab], c = color_use, label = str(lab))
            plt.legend(ncol = int(np.sqrt(len(set_labels))), loc = "lower left", bbox_to_anchor = (0, - np.sqrt(0.12 * (len(set_labels) / int(np.sqrt(len(set_labels))))) / 1.25))
            plt.xlabel("TSNE Feature 1")
            plt.ylabel("TSNE Feature 2")
            ws = 10
            if "20" in csv_file:
                ws = 20
            plt.title("DBSCAN\nWindow size " + str(ws) + "\nMinimum " + str(num_clus) + " samples")
            plt.savefig(new_name_png, bbox_inches = "tight")
            plt.close()

            new_data_csv = {"vehicle": list(file_csv["vehicle"]), "ride": list(file_csv["ride"]), "cluster": list_labels, 
                            "TSNE_f1": [X_embedded[ix][0] for ix in range(len(list_labels))], 
                            "TSNE_f2": [X_embedded[ix][1] for ix in range(len(list_labels))]}
            df_new_data_csv = pd.DataFrame(new_data_csv)
            df_new_data_csv.to_csv(new_name, index = False)