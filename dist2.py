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
            
            distances = np.sort(distances, axis=0)
            distances = distances[:,1]
            plt.plot(distances)