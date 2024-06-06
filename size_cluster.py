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
        
def avg_yes_no(set_ref, lab_set):
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
    for val in avg_dict_yes:
        avg_dict_yes[val] = np.average(avg_dict_yes[val])
        avg_dict_no[val] = np.average(avg_dict_no[val])
        avg_dict[val] = np.average(avg_dict[val])
        if avg_dict_no[val] >= 0.01 or avg_dict_yes[val] >= 0.01 or avg_dict[val] >= 0.01:
            print(val, np.round(avg_dict_yes[val] * 100, 2), np.round(avg_dict_no[val] * 100, 2), np.round(avg_dict[val] * 100, 2))
    #print(avg_dict_yes)
    #print(avg_dict_no)
    #print(avg_dict)

def euclid_yes_no(set_ref, ws):

    file_distance_json = open("count_me/all_percent_1/marker_all_percent_1_" + str(ws) + ".json", "r")

    distance_json = eval(file_distance_json.readlines()[0])

    dict_actual = dict()

    for ix in range(len(distance_json["compare_to"])):
        merge_reference = str(distance_json["compare_to"][ix]["vehicle"]) + "_" + str(distance_json["compare_to"][ix]["ride"])
        dict_actual[merge_reference] = dict() 
        for other_ix in range(len(distance_json["compare_to"][ix]["similar"])):
            other_reference = str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_vehicle"]) + "_" + str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_ride"])
            dist_ref = distance_json["compare_to"][ix]["similar"][other_ix]["distance"]
            ord_ref = distance_json["compare_to"][ix]["similar"][other_ix]["order"]
            dict_actual[merge_reference][other_reference] = (ord_ref, dist_ref)

    both_euclid = []
    both_ord = []
    one_not_euclid = []
    one_not_ord = []
    one_euclid = []
    one_ord = []
    first_euclid = []
    first_ord = []
    second_euclid = []
    second_ord = []
    first_not_euclid = []
    first_not_ord = []
    second_not_euclid = []
    second_not_ord = []
    none_euclid = []
    none_ord = []
    yes_no_euclid = []
    yes_no_ord = []
    no_yes_euclid = []
    no_yes_ord = []
    one_one_euclid = []
    one_one_ord = []
    for r1 in dict_actual:
        for r2 in dict_actual[r1]:
            ord, euclid = dict_actual[r1][r2]
            if r1 in set_ref and r2 in set_ref:
                both_euclid.append(euclid)
                both_ord.append(ord)
            if r1 not in set_ref or r2 not in set_ref:
                one_not_euclid.append(euclid)
                one_not_ord.append(ord)
            if r1 in set_ref or r2 in set_ref:
                one_euclid.append(euclid)
                one_ord.append(ord)
            if r1 in set_ref:
                first_euclid.append(euclid)
                first_ord.append(ord)
            if r2 in set_ref:
                second_euclid.append(euclid)
                second_ord.append(ord)
            if r1 not in set_ref:
                first_not_euclid.append(euclid)
                first_not_ord.append(ord)
            if r2 not in set_ref:
                second_not_euclid.append(euclid)
                second_not_ord.append(ord)
            if r1 not in set_ref and r2 not in set_ref:
                none_euclid.append(euclid)
                none_ord.append(ord)
            if r1 in set_ref and r2 not in set_ref:
                yes_no_euclid.append(euclid)
                yes_no_ord.append(ord)
            if r1 not in set_ref and r2 in set_ref:
                no_yes_euclid.append(euclid)
                no_yes_ord.append(ord)
            if (r1 not in set_ref and r2 in set_ref) or (r2 not in set_ref and r1 in set_ref):
                one_one_euclid.append(euclid)
                one_one_ord.append(ord)
    #print(np.average(one_euclid), np.average(one_ord))
    #print(np.average(one_not_euclid), np.average(one_not_ord))
    #print(np.average(first_euclid), np.average(first_ord))
    #print(np.average(second_euclid), np.average(second_ord))
    #print(np.average(first_not_euclid), np.average(first_not_ord))
    #print(np.average(second_not_euclid), np.average(second_not_ord))
    #print(np.average(yes_no_euclid), np.average(yes_no_ord))
    #print(np.average(no_yes_euclid), np.average(no_yes_ord))
    print(np.average(both_euclid), np.average(both_ord))
    print(np.average(none_euclid), np.average(none_ord))
    print(np.average(one_one_euclid), np.average(one_one_ord))

def did_choose_set(set_ref, ws): 

    file_distance_json = open("count_me/all_percent_1/marker_all_percent_1_" + str(ws) + ".json", "r")

    distance_json = eval(file_distance_json.readlines()[0])

    dict_actual = dict()
    dict_actual_20 = dict()
    dict_actual_5 = dict()

    class_of_ref = dict()
    for ix in range(len(distance_json["compare_to"])):
        merge_reference = str(distance_json["compare_to"][ix]["vehicle"]) + "_" + str(distance_json["compare_to"][ix]["ride"])
        dict_actual[merge_reference] = dict() 
        dict_actual_20[merge_reference] = 0
        dict_actual_5[merge_reference] = 0
        cls_me = merge_reference in set_ref
        class_of_ref[merge_reference] = cls_me
        for other_ix in range(len(distance_json["compare_to"][ix]["similar"])):
            other_reference = str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_vehicle"]) + "_" + str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_ride"])
            dist_ref = distance_json["compare_to"][ix]["similar"][other_ix]["distance"]
            ord_ref = distance_json["compare_to"][ix]["similar"][other_ix]["order"]
            dict_actual[merge_reference][other_reference] = (ord_ref, dist_ref)
            cls_other = other_reference in set_ref
            class_of_ref[other_reference] = cls_other
            if class_of_ref[merge_reference] == class_of_ref[other_reference]:
                dict_actual_20[merge_reference] += 1
                if ord_ref < 5 * 114 + 1:
                    dict_actual_5[merge_reference] += 1

    usable_ref = set()
    banned = ["oldsz6oBFprLHMCOZ8RrY5qC4NqyWN2", "uYtOqsFbKhhEjc3zFe1AlHDaGEz2", "wzn4aVKA1Ja8D7ifTq1NzOCaWex1", "9Y00mt5TXdb2jZnDHANZQJjFzK43"] 
    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        if user_id in banned: 
            continue 
        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])):
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            usable_ref.add(merge_reference)
        break

    dict_user = dict()
    dict_user_clus = dict()

    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        if user_id in banned: 
            continue  
        dict_user[user_id] = dict()
        dict_user_clus[user_id] = dict()
        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])): 
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            dict_user[user_id][merge_reference] = file_user_id["chosen"][ix].split(":")
            dict_user[user_id][merge_reference] = [oi.split("_")[0] + "_" + oi.split("_")[1] for oi in dict_user[user_id][merge_reference]]
            dict_user_clus[user_id][merge_reference] = 0
            for other_reference in dict_user[user_id][merge_reference]:
                if class_of_ref[merge_reference] == class_of_ref[other_reference]:
                    dict_user_clus[user_id][merge_reference] += 1
 
    for user_id in dict_user:
        main_number = []
        number_20 = []
        number_5 = []
        number_20_average = []
        number_5_average = []
        for merge_reference in dict_user[user_id]:
            main_number.append(class_of_ref[merge_reference])
            number_20_split = []
            number_5_split = []
            for other_reference in dict_actual[merge_reference]:
                ord_ref, dist_ref = dict_actual[merge_reference][other_reference]
                number_20.append(class_of_ref[other_reference])
                number_20_split.append(class_of_ref[other_reference])
                if ord_ref < 5 * 114 + 1:
                    number_5.append(class_of_ref[other_reference])
                    number_5_split.append(class_of_ref[other_reference])
            number_20_average.append(np.sum(number_20_split) / len(number_20_split))
            number_5_average.append(np.sum(number_5_split) / len(number_5_split))
        print(np.sum(main_number) / len(main_number), np.sum(main_number), len(main_number))
        print(np.sum(number_20) / len(number_20), np.sum(number_20), len(number_20))
        print(np.sum(number_5) / len(number_5), np.sum(number_5), len(number_5))
        print(np.average(number_20_average), np.average(number_5_average))
        break

    for cls in [True, False]:
        avg_user = dict()
        avg_avg_user = dict()
        avg_w_user = dict()
        avg_avg_w_user = dict()
        avg_w = dict()
        avg_avg_w = dict()
        lenw = dict()
        lenm = dict()
        for user_id in dict_user_clus:
            avg_user[user_id] = []
            avg_w_user[user_id] = []
            avg_w[user_id] = []
            lenw[user_id] = dict()
            lenm[user_id] = dict()
            for ref in dict_user_clus[user_id]:
                if class_of_ref[ref] != cls:
                    continue
                if min(dict_actual_20[ref], 5) != 0:
                    avg_user[user_id].append(dict_user_clus[user_id][ref] / min(dict_actual_20[ref], 5))
                    avg_w_user[user_id].append(dict_user_clus[user_id][ref] / 5)
                avg_w[user_id].append(dict_user_clus[user_id][ref] / 5)
                if dict_actual_20[ref] not in lenw[user_id]:
                    lenw[user_id][dict_actual_20[ref]] = 0
                lenw[user_id][dict_actual_20[ref]] += 1
                if min(dict_actual_20[ref], 5) not in lenm[user_id]:
                    lenm[user_id][min(dict_actual_20[ref], 5)] = 0
                lenm[user_id][min(dict_actual_20[ref], 5)] += 1
            if len(avg_w[user_id]) < 1:
                continue
            avg_avg_user[user_id] = np.average(avg_user[user_id])
            avg_avg_w_user[user_id] = np.average(avg_w_user[user_id])
            avg_avg_w[user_id] = np.average(avg_w[user_id])
        if len(avg_avg_w) < 1:
            continue
        print(np.round(np.average(list(avg_avg_user.values())) * 100, 2))
        print(np.round(np.average(list(avg_avg_w_user.values())) * 100, 2))
        print(np.round(np.average(list(avg_avg_w.values())) * 100, 2))
        for user_id in dict_user_clus:
            print(lenw[user_id])
            print(lenm[user_id])
            break

    avg_user = dict()
    avg_avg_user = dict()
    avg_w_user = dict()
    avg_avg_w_user = dict()
    avg_w = dict()
    avg_avg_w = dict()
    lenw = dict()
    lenm = dict()
    for user_id in dict_user_clus:
        avg_user[user_id] = []
        avg_w_user[user_id] = []
        avg_w[user_id] = []
        lenw[user_id] = dict()
        lenm[user_id] = dict()
        for ref in dict_user_clus[user_id]:
            if min(dict_actual_20[ref], 5) != 0:
                avg_user[user_id].append(dict_user_clus[user_id][ref] / min(dict_actual_20[ref], 5))
                avg_w_user[user_id].append(dict_user_clus[user_id][ref] / 5)
            avg_w[user_id].append(dict_user_clus[user_id][ref] / 5)
            if dict_actual_20[ref] not in lenw[user_id]:
                lenw[user_id][dict_actual_20[ref]] = 0
            lenw[user_id][dict_actual_20[ref]] += 1
            if min(dict_actual_20[ref], 5) not in lenm[user_id]:
                lenm[user_id][min(dict_actual_20[ref], 5)] = 0
            lenm[user_id][min(dict_actual_20[ref], 5)] += 1
        avg_avg_user[user_id] = np.average(avg_user[user_id])
        avg_avg_w_user[user_id] = np.average(avg_w_user[user_id])
        avg_avg_w[user_id] = np.average(avg_w[user_id])
    print(np.round(np.average(list(avg_avg_user.values())) * 100, 2))
    print(np.round(np.average(list(avg_avg_w_user.values())) * 100, 2))
    print(np.round(np.average(list(avg_avg_w.values())) * 100, 2))
    for user_id in dict_user_clus:
        print(lenw[user_id])
        print(lenm[user_id])
        break

    avg_user = []
    avg_w_user = []
    avg_w = []
    lenw = dict()
    lenm = dict()
    for ref in dict_user_clus[list(dict_user_clus.keys())[0]]:
        if min(dict_actual_20[ref], 5) != 0:
            avg_user.append(dict_actual_5[ref] / min(dict_actual_20[ref], 5))
            avg_w_user.append(dict_actual_5[ref] / 5)
        avg_w.append(dict_actual_5[ref] / 5)
        if dict_actual_20[ref] not in lenw:
            lenw[dict_actual_20[ref]] = 0
        lenw[dict_actual_20[ref]] += 1
        if min(dict_actual_20[ref], 5) not in lenm:
            lenm[min(dict_actual_20[ref], 5)] = 0
        lenm[min(dict_actual_20[ref], 5)] += 1
    print(np.round(np.average(avg_user) * 100, 2))
    print(np.round(np.average(avg_w_user) * 100, 2))
    print(np.round(np.average(avg_w) * 100, 2))
    for user_id in dict_user_clus:
        print(lenw)
        print(lenm)
        break

    for cls in [True, False]:
        avg_user = []
        avg_w_user = []
        avg_w = []
        lenw = dict()
        lenm = dict()
        for ref in dict_user_clus[list(dict_user_clus.keys())[0]]:
            if class_of_ref[ref] != cls:
                continue
            if min(dict_actual_20[ref], 5) != 0:
                avg_user.append(dict_actual_5[ref] / min(dict_actual_20[ref], 5))
                avg_w_user.append(dict_actual_5[ref] / 5)
            avg_w.append(dict_actual_5[ref] / 5)
            if dict_actual_20[ref] not in lenw:
                lenw[dict_actual_20[ref]] = 0
            lenw[dict_actual_20[ref]] += 1
            if min(dict_actual_20[ref], 5) not in lenm:
                lenm[min(dict_actual_20[ref], 5)] = 0
            lenm[min(dict_actual_20[ref], 5)] += 1
        if len(avg_w) < 1:
            continue
        print(np.round(np.average(avg_user) * 100, 2))
        print(np.round(np.average(avg_w_user) * 100, 2))
        print(np.round(np.average(avg_w) * 100, 2))
        for user_id in dict_user_clus:
            print(lenw)
            print(lenm)
            break

cluster_for_ref_10, minimaxdict10, dict_how_many_classes10 = process_ws(10)
cluster_for_ref_20, minimaxdict20, dict_how_many_classes20 = process_ws(20)

labels10 = labels_to_use("_all_percent_1_10")
labels20 = labels_to_use("_all_percent_1_20")

for algo in cluster_for_ref_10:
    for num_clus in cluster_for_ref_10[algo]:
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
        if algo == "KMeans" and num_clus == 2:
            print(algo, num_clus, np.round(equal_num / (equal_num + not_equal_num) * 100, 2), np.round(len(in_both_smallest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(len(in_one_smallest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(minsize10 / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(minsize20 / len(cluster_for_ref_20[algo][num_clus]) * 100, 2))
            print(algo, num_clus, np.round(equal_num / (equal_num + not_equal_num) * 100, 2), np.round(len(not_in_both_largest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(len(not_in_one_largest) / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(100 - maxsize10 / len(cluster_for_ref_10[algo][num_clus]) * 100, 2), np.round(100 - maxsize20 / len(cluster_for_ref_20[algo][num_clus]) * 100, 2))
            for set_ref in [dict_how_many_classes20[algo][num_clus][minclus20]]:
                #avg_yes_no(set_ref, labels10) 
                avg_yes_no(set_ref, labels20) 
                #euclid_yes_no(set_ref, 10)
                euclid_yes_no(set_ref, 20)
                #did_choose_set(set_ref, 10)
                did_choose_set(set_ref, 20)