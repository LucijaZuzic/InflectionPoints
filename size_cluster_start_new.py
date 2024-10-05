import os
import pandas as pd 
import numpy as np

list_clus = [2]

def process_ws(ws, dict_how_many_classes_merged):

    class_file = dict()
    for algo in ["DBSCAN", "KMeans"]:
        class_file[algo] = dict()   
        add = ""
        if algo == "DBSCAN":
            add = "elbow/" 
        for nc in os.listdir("clustered_new/" + algo + "/" + add):
            if nc != "346" and algo == "DBSCAN":
                continue
            if nc != "2" and algo == "KMeans":
                continue
            num_clus = 2
            class_file[algo][num_clus] = dict()
            new_name = "clustered_new/" + algo + "/" + add + str(nc) + "/all_percent_1/clustered_" + algo + "_" + str(nc) + "_marker_all_percent_1_" + str(ws) + ".csv"
            file_new_name = pd.read_csv(new_name, index_col = False)
            for ix in range(len(file_new_name["vehicle"])):
                nn = file_new_name["vehicle"][ix].split("_")[1] + "_" +  str(file_new_name["ride"][ix]).split("_")[1]
                class_file[algo][num_clus][nn] = file_new_name["cluster"][ix]
  
    file_distance_json = open("count_me/all_percent_1/marker_all_percent_1_" + str(ws) + ".json", "r")

    distance_json = eval(file_distance_json.readlines()[0])

    dict_actual = dict()

    cluster_for_ref = dict()
    dict_how_many_classes = dict()
    for algo in ["DBSCAN", "KMeans"]:
        cluster_for_ref[algo] = dict()
        dict_how_many_classes[algo] = dict()
        for num_clus in list_clus:
            cluster_for_ref[algo][num_clus] = dict()
            dict_how_many_classes[algo][num_clus] = dict()

    for ix in range(len(distance_json["compare_to"])):
        merge_reference = str(distance_json["compare_to"][ix]["vehicle"]) + "_" + str(distance_json["compare_to"][ix]["ride"])
        dict_actual[merge_reference] = dict() 
        for other_ix in range(len(distance_json["compare_to"][ix]["similar"])):
            other_reference = str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_vehicle"]) + "_" + str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_ride"])
            dist_ref = distance_json["compare_to"][ix]["similar"][other_ix]["distance"]
            ord_ref = distance_json["compare_to"][ix]["similar"][other_ix]["order"]
            dict_actual[merge_reference][other_reference] = (ord_ref, dist_ref)
            for algo in ["DBSCAN", "KMeans"]:
                for num_clus in list_clus:
                    cls_me = class_file[algo][num_clus][merge_reference]
                    cls_other = class_file[algo][num_clus][other_reference]
                    if cls_me not in dict_how_many_classes[algo][num_clus]:
                        dict_how_many_classes[algo][num_clus][cls_me] = set()
                    dict_how_many_classes[algo][num_clus][cls_me].add(merge_reference)
                    if cls_other not in dict_how_many_classes[algo][num_clus]:
                        dict_how_many_classes[algo][num_clus][cls_other] = set()
                    dict_how_many_classes[algo][num_clus][cls_other].add(other_reference)
                    cluster_for_ref[algo][num_clus][merge_reference] = cls_me
                    cluster_for_ref[algo][num_clus][other_reference] = cls_other

    minimaxdict = dict()
    for algo in dict_how_many_classes: 
        minimaxdict[algo] = dict()
        for num_clus in dict_how_many_classes[algo]: 
            #print(algo, num_clus)
            maxsize = 0
            maxclus = ""
            minsize = 100000
            minclus = ""
            nd = dict()
            for cls_other in sorted(list(dict_how_many_classes[algo][num_clus].keys())):
                nd[cls_other] = len(dict_how_many_classes[algo][num_clus][cls_other])
                dict_how_many_classes_merged["ws"].append(ws)
                dict_how_many_classes_merged["algo"].append(algo)
                dict_how_many_classes_merged["num_clus"].append(num_clus)
                dict_how_many_classes_merged["class"].append(cls_other)
                dict_how_many_classes_merged["size"].append(nd[cls_other])
                if nd[cls_other] > maxsize:
                    maxsize = nd[cls_other]
                    maxclus = cls_other
                if nd[cls_other] < minsize:
                    minsize = nd[cls_other]
                    minclus = cls_other
            #print(maxsize, maxclus, minsize, minclus)
            #print(nd)
            minimaxdict[algo][num_clus] = (maxsize, maxclus, minsize, minclus)
    return cluster_for_ref, minimaxdict, dict_how_many_classes

dict_how_many_classes_merged = {"ws": [], "algo": [], "num_clus": [], "class": [], "size": []}
cluster_for_ref_10, minimaxdict10, dict_how_many_classes10 = process_ws(10, dict_how_many_classes_merged)
cluster_for_ref_20, minimaxdict20, dict_how_many_classes20 = process_ws(20, dict_how_many_classes_merged)
dict_how_many_classes_merged_csv = pd.DataFrame(dict_how_many_classes_merged)
dict_how_many_classes_merged_csv.to_csv("new_dict_how_many_classes_merged.csv")

df_use_euclid = dict()
df_use_choose = dict()
did_choose_set_dict = dict()
euclid_yes_no_dict = dict()

for algo in cluster_for_ref_10:
    did_choose_set_dict[algo] = dict()
    euclid_yes_no_dict[algo] = dict()
    for num_clus in cluster_for_ref_10[algo]:
        did_choose_set_dict[algo][num_clus] = dict()
        euclid_yes_no_dict[algo][num_clus] = dict()
        equal_num = 0
        not_equal_num = 0
        in_both_smallest = set()
        in_one_smallest = set()
        not_in_both_largest = set()
        not_in_one_largest = set()
        not_in_largest10 = set()
        not_in_largest20 = set()
        maxsize10, maxclus10, minsize10, minclus10 = minimaxdict10[algo][num_clus]
        maxsize20, maxclus20, minsize20, minclus20 = minimaxdict20[algo][num_clus]
        for ref in cluster_for_ref_10[algo][num_clus]:
            if cluster_for_ref_10[algo][num_clus][ref] == cluster_for_ref_20[algo][num_clus][ref]:
                equal_num += 1
            else:
                not_equal_num += 1
            if cluster_for_ref_10[algo][num_clus][ref] == minclus10 and cluster_for_ref_20[algo][num_clus][ref] == minclus20:
                in_both_smallest.add(ref)
            if cluster_for_ref_10[algo][num_clus][ref] == minclus10 or cluster_for_ref_20[algo][num_clus][ref] == minclus20:
                in_one_smallest.add(ref)
            if not cluster_for_ref_10[algo][num_clus][ref] == maxclus10 and not cluster_for_ref_20[algo][num_clus][ref] == maxclus20:
                not_in_both_largest.add(ref)
            if not cluster_for_ref_10[algo][num_clus][ref] == maxclus10:
                not_in_largest10.add(ref)
            if not cluster_for_ref_20[algo][num_clus][ref] == maxclus20:
                not_in_largest20.add(ref)
        sets_ref = [in_both_smallest, in_one_smallest, dict_how_many_classes10[algo][num_clus][minclus10], dict_how_many_classes20[algo][num_clus][minclus20], not_in_both_largest, not_in_one_largest, not_in_largest10, not_in_largest20]
        
        print(algo, num_clus, np.round(equal_num / (equal_num + not_equal_num) * 100, 2), np.round(len(in_both_smallest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(len(in_one_smallest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(minsize10 / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(minsize20 / len(cluster_for_ref_20[algo][num_clus]) * 100, 2))
        print(algo, num_clus, np.round(equal_num / (equal_num + not_equal_num) * 100, 2), np.round(len(not_in_both_largest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(len(not_in_one_largest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(100 - maxsize10 / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(100 - maxsize20 / len(cluster_for_ref_20[algo][num_clus]) * 100, 2))