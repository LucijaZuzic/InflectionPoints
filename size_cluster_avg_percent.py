import os
import pandas as pd 
import numpy as np

list_clus = list(range(2, 21))
for r in list(range(100, 121)):
    list_clus.append(r)

def process_ws(ws):

    class_file = dict()
    for algo in ["DBSCAN", "KMeans"]:
        class_file[algo] = dict()   
        for num_clus in list_clus:
            class_file[algo][num_clus] = dict()
            new_name = "clustered/" + algo + "/" + str(num_clus) + "/all_percent_1/clustered_" + algo + "_" + str(num_clus) + "_marker_all_percent_1_" + str(ws) + ".csv"
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

def labels_to_use(name):
    
    for subdir_name in os.listdir("marker_count"):
        
        for csv_file in os.listdir("marker_count/" + subdir_name):

            if ".csv" not in csv_file:
                
                continue  

            if name not in csv_file:
                
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

            X = dict()
            for ix in range(len(file_csv["vehicle"])):
                ref = file_csv["vehicle"][ix].split("_")[-1] + "_" + file_csv["ride"][ix].split("_")[-1]
                X[ref] = dict()
                for val in sorted(list(set_used)):
                    X[ref][val] = file_csv[val][ix]
            return X
        
def avg_yes_no(set_ref, lab_set, ws, algo, num_clus):
    avg_dict_yes = dict()
    avg_dict_no = dict()
    avg_dict = dict()
    for ref in lab_set:
        for val in lab_set[ref]:
            avg_dict_yes[val] = []
            avg_dict_no[val] = []
            avg_dict[val] = []
    for ref in lab_set:
        if ref in set_ref:
            for val in lab_set[ref]:
                avg_dict[val].append(lab_set[ref][val])
                avg_dict_yes[val].append(lab_set[ref][val])
        else:
            for val in lab_set[ref]:
                avg_dict[val].append(lab_set[ref][val])
                avg_dict_no[val].append(lab_set[ref][val])
    df_new = {"seq": [], "yes": [], "no": [], "all": []}
    for val in avg_dict_yes:
        df_new["seq"].append(val)
        df_new["yes"].append(np.average(avg_dict_yes[val]))
        df_new["no"].append(np.average(avg_dict_no[val]))
        df_new["all"].append(np.average(avg_dict[val]))
        avg_dict_yes[val] = np.average(avg_dict_yes[val])
        avg_dict_no[val] = np.average(avg_dict_no[val])
        avg_dict[val] = np.average(avg_dict[val])
        #if avg_dict[val] >= 0.01:
            #print(val, np.round(avg_dict_yes[val] * 100, 2), np.round(avg_dict_no[val] * 100, 2), np.round(avg_dict[val] * 100, 2))
    #print(avg_dict_yes)
    #print(avg_dict_no)
    #print(avg_dict)

    begin_dir = "avg_yes_no/" + str(ws) + "/" + str(algo) + "/" + str(num_clus) + "/"

    if not os.path.isdir(begin_dir):
        os.makedirs(begin_dir)

    df_avg_yes_no_csv = pd.DataFrame(df_new)
    df_avg_yes_no_csv.to_csv(begin_dir + "avg_yes_no_" + str(ws) + "_" + str(algo) + "_" + str(num_clus) + ".csv")

    return (avg_dict_yes, avg_dict_no, avg_dict)

cluster_for_ref_10, minimaxdict10, dict_how_many_classes10 = process_ws(10)
cluster_for_ref_20, minimaxdict20, dict_how_many_classes20 = process_ws(20)

labels10 = labels_to_use("_all_percent_1_10")
labels20 = labels_to_use("_all_percent_1_20")

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

        avg_yes_no(dict_how_many_classes10[algo][num_clus][minclus10], labels10, 10, algo, num_clus) 
        avg_yes_no(dict_how_many_classes20[algo][num_clus][minclus20], labels20, 20, algo, num_clus) 