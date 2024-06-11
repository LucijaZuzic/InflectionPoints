import numpy as np
import pandas as pd

list_clus_short = list(range(2, 21))

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

did_choose_set_dict = dict()
euclid_yes_no_dict = dict()
dict_how_many_classes = dict()
for algo in ["KMeans", "DBSCAN"]:
    did_choose_set_dict[algo] = dict()
    euclid_yes_no_dict[algo] = dict()
    dict_how_many_classes[algo] = dict()
    for num_clus in list_clus:
        did_choose_set_dict[algo][num_clus] = dict()
        euclid_yes_no_dict[algo][num_clus] = dict()
        dict_how_many_classes[algo][num_clus] = dict()
        dict_how_many_classes[algo][num_clus][10] = dict()
        dict_how_many_classes[algo][num_clus][20] = dict()

df_use_choose = pd.read_csv("df_use_choose.csv")
df_use_euclid = pd.read_csv("df_use_euclid.csv")
dict_how_many_classes_merged = pd.read_csv("dict_how_many_classes_merged.csv")

for ix in range(len(df_use_choose["ws"])):
    algo, num_clus, ws = df_use_choose["algo"][ix], df_use_choose["num_clus"][ix], df_use_choose["ws"][ix]
    did_choose_set_dict[algo][num_clus][ws] = df_use_choose["user_avg"][ix]

for ix in range(len(df_use_euclid["ws"])):
    algo, num_clus, ws = df_use_euclid["algo"][ix], df_use_euclid["num_clus"][ix], df_use_euclid["ws"][ix]
    both_euclid, both_ord = df_use_euclid["both_euclid"][ix], df_use_euclid["both_ord"][ix]
    none_euclid, none_ord = df_use_euclid["none_euclid"][ix], df_use_euclid["none_ord"][ix]
    one_one_euclid, one_one_ord = df_use_euclid["one_one_euclid"][ix], df_use_euclid["one_one_ord"][ix]
    euclid_yes_no_dict[algo][num_clus][ws] = (both_euclid, both_ord, none_euclid, none_ord, one_one_euclid, one_one_ord)

for ix in range(len(dict_how_many_classes_merged["ws"])):
    algo, num_clus, ws = dict_how_many_classes_merged["algo"][ix], dict_how_many_classes_merged["num_clus"][ix], dict_how_many_classes_merged["ws"][ix]
    class_marker, size = dict_how_many_classes_merged["class"][ix], dict_how_many_classes_merged["size"][ix]
    dict_how_many_classes[algo][num_clus][ws][class_marker] = size

print("Parameter & KMeans 10 & KMeans 20 & DBSCAN 10 size & DBSCAN 10 & DBSCAN 20 size & DBSCAN 20 \\\\ \\hline")
for num_clus in list_clus_short:
    printer = ""
    for algo in ["KMeans", "DBSCAN"]:
        v3 = np.round(did_choose_set_dict[algo][num_clus][10], 2)
        v6 = np.round(did_choose_set_dict[algo][num_clus][20], 2)
        if "DBSCAN" == algo:
            printer += " & " + str(len(dict_how_many_classes[algo][num_clus][10])) + " & " + str(v3) + " & " + str(len(dict_how_many_classes[algo][num_clus][20])) + " & " + str(v6)
        else:                
            printer += str(num_clus) + " & " + str(v3) + " & " + str(v6)
    print(printer, "\\\\ \\hline")
    
for algo in ["KMeans", "DBSCAN"]:
    for ws in [10, 20]:
        print(algo + "_" + str(ws)) 
        print("Parameter & both_euclid & both_ord & none_euclid & none_ord & one_one_euclid & one_one_ord \\\\ \\hline")
        printer = ""
        for num_clus in list_clus_short:
            both_euclid, both_ord, none_euclid, none_ord, one_one_euclid, one_one_ord = euclid_yes_no_dict[algo][num_clus][ws]
            printer += str(num_clus) + " & " + str(np.round(np.average(both_euclid), 4)) + " & " + str(np.round(np.average(both_ord), 2)) + " & " + str(np.round(np.average(none_euclid), 4)) + " & " + str(np.round(np.average(none_ord), 2)) + " & " + str(np.round(np.average(one_one_euclid), 4)) + " & " + str(np.round(np.average(one_one_ord), 2)) + " \\\\ \\hline\n"
        print(printer)