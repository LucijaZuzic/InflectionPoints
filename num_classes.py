from utilities import *
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        if "_all_percent_1_5" not in csv_file:
            
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
        kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)
        X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)
        list_labels = list(kmeans.labels_)
        count_clus = {lab: list_labels.count(lab) for lab in set(list_labels)} 
        clusters_x = {lab: [] for lab in set(list_labels)}
        clusters_y = {lab: [] for lab in set(list_labels)}
        for lab in clusters_x:
            for ix in range(len(list_labels)):
                if list_labels[ix] == lab:
                    clusters_x[lab].append(X_embedded[ix][0])
                    clusters_y[lab].append(X_embedded[ix][1])
        plt.scatter(clusters_x[0], clusters_y[0], c = "r")
        plt.scatter(clusters_x[1], clusters_y[1], c = "g")
        plt.show()
        plt.close()
