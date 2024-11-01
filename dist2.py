from utilities import *
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
import kneed

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
        print(np.shape(X))
        
        X_components = PCA(n_components = 2, random_state = 42, svd_solver = "full").fit_transform(X)
        
        X_embedded = TSNE(n_components = 2, perplexity = 30, random_state = 42, init = "pca").fit_transform(X)
        
        for min_nbs in [346]:

            if os.path.isfile("clustered_new/kneed/" + str(min_nbs) + "/" + subdir_name + "/elbow_" + str(min_nbs) + "_" + csv_file):
                continue

            if not os.path.isdir("clustered_new/kneed/" + str(min_nbs) + "/" + subdir_name):
                os.makedirs("clustered_new/kneed/" + str(min_nbs) + "/" + subdir_name)

            print(min_nbs)

            neighbors = NearestNeighbors(n_neighbors = min_nbs)
            neighbors_fit = neighbors.fit(X)
            distances, indices = neighbors_fit.kneighbors(X)

            distances_sorted = np.sort(distances, axis=0)
            distances_subset = distances_sorted[:,1]
            #plt.plot([ix for ix in range(len(distances_subset))], distances_subset)
            #plt.show()
            #plt.close()

            kneedle = kneed.KneeLocator([ix for ix in range(len(distances_subset))], distances_subset, curve = "concave", direction = "increasing")
            knee_point = kneedle.knee
            knee_point_dist = distances_subset[knee_point]
            print("Knee: ", knee_point, knee_point_dist)
            #kneedle.plot_knee()
            #plt.show()
            #plt.close()
            
            kneedle = kneed.KneeLocator([ix for ix in range(len(distances_subset))], distances_subset, curve = "convex", direction = "increasing")
            elbow_point = kneedle.elbow
            elbow_point_dist = distances_subset[elbow_point]
            print("Elbow: ", elbow_point, elbow_point_dist)
            #kneedle.plot_knee()
            #plt.show()
            #plt.close()

            new_name_elbow = "clustered_new/kneed/" + str(min_nbs) + "/" + subdir_name + "/elbow_" + str(min_nbs) + "_" + csv_file

            new_data_csv_elbow = {"knee_point": [knee_point for ix in range(len(distances[0]))], 
                            "knee_point_dist": [knee_point_dist for ix in range(len(distances[0]))], 
                            "elbow_point": [elbow_point for ix in range(len(distances[0]))], 
                            "elbow_point_dist": [elbow_point_dist for ix in range(len(distances[0]))]}
            print(len(distances), len(indices), len(distances[0]), len(indices[0]), np.shape(distances), np.shape(indices[0]))
            for ix in range(len(distances)):
                new_data_csv_elbow["distances " + str(ix)] = distances[ix]
                new_data_csv_elbow["indices " + str(ix)] = indices[ix]
                            
            df_new_data_csv_elbow = pd.DataFrame(new_data_csv_elbow)
            df_new_data_csv_elbow.to_csv(new_name_elbow, index = False)

            if not os.path.isdir("clustered_new/DBSCAN/elbow/" + str(min_nbs) + "/" + subdir_name):
                os.makedirs("clustered_new/DBSCAN/elbow/" + str(min_nbs) + "/" + subdir_name)

            new_name_dbscan_elbow  = "clustered_new/DBSCAN/elbow/" + str(min_nbs) + "/" + subdir_name + "/clustered_DBSCAN_" + str(min_nbs) + "_" + csv_file

            dbscan_elbow = DBSCAN(min_samples = min_nbs, eps = elbow_point_dist).fit(X)
            list_labels_dbscan_elbow = list(dbscan_elbow.labels_)
            
            new_data_csv_dbscan_elbow = {"vehicle": list(file_csv["vehicle"]), "ride": list(file_csv["ride"]), "cluster": list_labels_dbscan_elbow, 
                            "PCA_f1": [X_components[ix][0] for ix in range(len(list_labels_dbscan_elbow))], 
                            "PCA_f2": [X_components[ix][1] for ix in range(len(list_labels_dbscan_elbow))],
                            "TSNE_f1": [X_embedded[ix][0] for ix in range(len(list_labels_dbscan_elbow))], 
                            "TSNE_f2": [X_embedded[ix][1] for ix in range(len(list_labels_dbscan_elbow))]}
            df_new_data_csv_dbscan_elbow = pd.DataFrame(new_data_csv_dbscan_elbow)
            df_new_data_csv_dbscan_elbow.to_csv(new_name_dbscan_elbow, index = False)

            num_clusters_elbow = len(set(list_labels_dbscan_elbow))
            print(num_clusters_elbow)

            if not os.path.isdir("clustered_new/DBSCAN/knee/" + str(min_nbs) + "/" + subdir_name):
                os.makedirs("clustered_new/DBSCAN/knee/" + str(min_nbs) + "/" + subdir_name)

            new_name_dbscan_knee  = "clustered_new/DBSCAN/knee/" + str(min_nbs) + "/" + subdir_name + "/clustered_DBSCAN_" + str(min_nbs) + "_" + csv_file

            dbscan_knee = DBSCAN(min_samples = min_nbs, eps = knee_point_dist).fit(X)
            list_labels_dbscan_knee = list(dbscan_knee.labels_)
            
            new_data_csv_dbscan_knee = {"vehicle": list(file_csv["vehicle"]), "ride": list(file_csv["ride"]), "cluster": list_labels_dbscan_knee, 
                            "PCA_f1": [X_components[ix][0] for ix in range(len(list_labels_dbscan_knee))], 
                            "PCA_f2": [X_components[ix][1] for ix in range(len(list_labels_dbscan_knee))],
                            "TSNE_f1": [X_embedded[ix][0] for ix in range(len(list_labels_dbscan_knee))], 
                            "TSNE_f2": [X_embedded[ix][1] for ix in range(len(list_labels_dbscan_knee))]}
            df_new_data_csv_dbscan_knee = pd.DataFrame(new_data_csv_dbscan_knee)
            df_new_data_csv_dbscan_knee.to_csv(new_name_dbscan_knee, index = False)

            num_clusters_knee = len(set(list_labels_dbscan_knee))
            print(num_clusters_knee)
            
            for num_clusters in [num_clusters_elbow, num_clusters_knee]:

                if num_clusters < 2:
                    continue

                if not os.path.isdir("clustered_new/KMeans/" + str(num_clusters) + "/" + subdir_name):
                    os.makedirs("clustered_new/KMeans/" + str(num_clusters) + "/" + subdir_name)

                new_name_kmeans  = "clustered_new/KMeans/" + str(num_clusters) + "/" + subdir_name + "/clustered_KMeans_" + str(num_clusters) + "_" + csv_file

                kmeans = KMeans(n_clusters = num_clusters, random_state = 42, init = "k-means++", n_init = "auto").fit(X)
                list_labels_kmeans = list(kmeans.labels_)
                
                new_data_csv_kmeans = {"vehicle": list(file_csv["vehicle"]), "ride": list(file_csv["ride"]), "cluster": list_labels_kmeans, 
                                "PCA_f1": [X_components[ix][0] for ix in range(len(list_labels_kmeans))], 
                                "PCA_f2": [X_components[ix][1] for ix in range(len(list_labels_kmeans))],
                                "TSNE_f1": [X_embedded[ix][0] for ix in range(len(list_labels_kmeans))], 
                                "TSNE_f2": [X_embedded[ix][1] for ix in range(len(list_labels_kmeans))]}
                df_new_data_csv_kmeans = pd.DataFrame(new_data_csv_kmeans)
                df_new_data_csv_kmeans.to_csv(new_name_kmeans, index = False)