import numpy as np
import pandas as pd

list_clus_short = list(range(2, 21))

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

algo_list_short = ["DBSCAN"]
algo_list = ["KMeans", "DBSCAN"]
    
avg_yes_no_dict = dict()
dict_how_many_classes = dict()
for algo in algo_list:
    avg_yes_no_dict[algo] = dict()
    dict_how_many_classes[algo] = dict()
    for num_clus in list_clus:
        avg_yes_no_dict[algo][num_clus] = dict()
        dict_how_many_classes[algo][num_clus] = dict()
        for ws in [10, 20]:
            avg_yes_no_dict[algo][num_clus][ws] = dict()
            dict_how_many_classes[algo][num_clus][ws] = dict()
            begin_dir = "avg_yes_no/" + str(ws) + "/" + str(algo) + "/" + str(num_clus) + "/"
            dict_avg_yes_no_dict = pd.read_csv(begin_dir + "avg_yes_no_" + str(ws) + "_" + str(algo) + "_" + str(num_clus) + ".csv")
            for ix in range(len(dict_avg_yes_no_dict["seq"])):
                seq, yes, no, all = dict_avg_yes_no_dict["seq"][ix], dict_avg_yes_no_dict["yes"][ix], dict_avg_yes_no_dict["no"][ix], dict_avg_yes_no_dict["all"][ix]
                avg_yes_no_dict[algo][num_clus][ws][seq] = (yes, no, all)
            
dict_how_many_classes_merged = pd.read_csv("dict_how_many_classes_merged.csv")
for ix in range(len(dict_how_many_classes_merged["ws"])):
    algo, num_clus, ws = dict_how_many_classes_merged["algo"][ix], dict_how_many_classes_merged["num_clus"][ix], dict_how_many_classes_merged["ws"][ix]
    class_marker, size = dict_how_many_classes_merged["class"][ix], dict_how_many_classes_merged["size"][ix]
    dict_how_many_classes[algo][num_clus][ws][class_marker] = size

changed = dict()
changed[10] = set()
changed[20] = set()
for algo in algo_list:
    for ws in [10, 20]:
        for num_clus in list_clus_short:
            #print(algo, ws, num_clus)
            ix = 0
            for seq in avg_yes_no_dict[algo][num_clus][ws]:
                if avg_yes_no_dict[algo][num_clus][ws][seq][2] >= 0.1:
                    ix += 1
                    if abs(avg_yes_no_dict[algo][num_clus][ws][seq][0] - avg_yes_no_dict[algo][num_clus][ws][seq][1]) >= 0.1:
                        changed[ws].add(seq)
                        #print(algo, ws, num_clus, seq, np.round(avg_yes_no_dict[algo][num_clus][ws][seq][0] * 100, 2), np.round(avg_yes_no_dict[algo][num_clus][ws][seq][1] * 100, 2), avg_yes_no_dict[algo][num_clus][ws][seq][2] * 100, 2)

use_numclus = False
print(changed)
for ws in changed:
    for seq in changed[ws]:
        v3 = np.round(avg_yes_no_dict["KMeans"][2][ws][seq][2] * 100, 2)
        #print(ws, seq, v3)
        printer = "Parameter" 
        for algo in algo_list_short:
            if algo != "KMeans" and use_numclus:
                printer += " & Clusters"
            printer += " & " + algo + " yes & " + algo + " no"
        printer += " \\\\ \\hline\n"
        for num_clus in list_clus_short:
            printer += "$" + str(num_clus) + "$"
            for algo in algo_list_short:
                v1 = np.round(avg_yes_no_dict[algo][num_clus][ws][seq][0] * 100, 2)
                v2 = np.round(avg_yes_no_dict[algo][num_clus][ws][seq][1] * 100, 2)
                if algo != "KMeans" and use_numclus:
                    printer += " & $" + str(len(dict_how_many_classes[algo][num_clus][ws])) + "$"
                printer += " & $" + str(v1) + "\\%$ & $" + str(v2) + "\\%$"
            printer += " \\\\ \\hline\n"
        #print(printer)

for algo in algo_list_short:
    for seq in changed[10]:
        if seq in changed[20]:
            v3 = np.round(avg_yes_no_dict[algo][2][10][seq][2] * 100, 2)
            v6 = np.round(avg_yes_no_dict[algo][2][20][seq][2] * 100, 2)
            print(seq, v3, v6)
            printer = "Parameter"
            if algo != "KMeans" and use_numclus:
                printer += " & Clusters"
            printer += " & " + algo + " 10 yes & " + algo + " 10 no & " + algo + " 20 yes & " + algo + " 20 no \\\\ \\hline\n"
            for num_clus in list_clus_short:
                v1 = np.round(avg_yes_no_dict[algo][num_clus][10][seq][0] * 100, 2)
                v2 = np.round(avg_yes_no_dict[algo][num_clus][10][seq][1] * 100, 2)
                v4 = np.round(avg_yes_no_dict[algo][num_clus][20][seq][0] * 100, 2)
                v5 = np.round(avg_yes_no_dict[algo][num_clus][20][seq][1] * 100, 2)
                printer += "$" + str(num_clus) + "$"
                if algo != "KMeans" and use_numclus:
                    printer += " & $" + str(len(dict_how_many_classes[algo][num_clus][ws])) + "$"
                printer += " & $" + str(v1) + "\\%$ & $" + str(v2) + "\\%$ & $" + str(v4) + "\\%$ & $" + str(v5) + "\\%$ \\\\ \\hline\n"
            print(printer)