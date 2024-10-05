import os
import pandas as pd 
import numpy as np

list_clus = [2]

def process_ws(ws):

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

def euclid_yes_no(set_ref, ws, algo, num_clus, df_use):

    vals_list = ["one_euclid", "one_ord", 
                 "one_not_euclid", "one_not_ord", 
                 "first_euclid", "first_ord", 
                 "second_euclid", "second_ord", 
                 "first_not_euclid", "first_not_ord", 
                 "second_not_euclid", "second_not_ord", 
                 "yes_no_euclid", "yes_no_ord", 
                 "no_yes_euclid", "no_yes_ord", 
                 "both_euclid", "both_ord", 
                 "none_euclid", "none_ord", 
                 "one_one_euclid", "one_one_ord", 
                 "ws", "algo", "num_clus"]
    for v in vals_list:
        if v not in df_use:
            df_use[v] = []

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
    df_use["one_euclid"].append(np.average(one_euclid))
    df_use["one_ord"].append(np.average(one_ord))
    #print(np.average(one_not_euclid), np.average(one_not_ord))
    df_use["one_not_euclid"].append(np.average(one_not_euclid))
    df_use["one_not_ord"].append(np.average(one_not_ord))
    #print(np.average(first_euclid), np.average(first_ord))
    df_use["first_euclid"].append(np.average(first_euclid))
    df_use["first_ord"].append(np.average(first_ord))
    #print(np.average(second_euclid), np.average(second_ord))
    df_use["second_euclid"].append(np.average(second_euclid))
    df_use["second_ord"].append(np.average(second_ord))
    #print(np.average(first_not_euclid), np.average(first_not_ord))
    df_use["first_not_euclid"].append(np.average(first_not_euclid))
    df_use["first_not_ord"].append(np.average(first_not_ord))
    #print(np.average(second_not_euclid), np.average(second_not_ord))
    df_use["second_not_euclid"].append(np.average(second_not_euclid))
    df_use["second_not_ord"].append(np.average(second_not_ord))
    #print(np.average(yes_no_euclid), np.average(yes_no_ord))
    df_use["yes_no_euclid"].append(np.average(yes_no_euclid))
    df_use["yes_no_ord"].append(np.average(yes_no_ord))
    #print(np.average(no_yes_euclid), np.average(no_yes_ord))
    df_use["no_yes_euclid"].append(np.average(no_yes_euclid))
    df_use["no_yes_ord"].append(np.average(no_yes_ord))
    #print(np.round(np.average(both_euclid), 4), np.round(np.average(both_ord), 2))
    df_use["both_euclid"].append(np.average(both_euclid))
    df_use["both_ord"].append(np.average(both_ord))
    #print(np.round(np.average(none_euclid), 4), np.round(np.average(none_ord), 2))
    df_use["none_euclid"].append(np.average(none_euclid))
    df_use["none_ord"].append(np.average(none_ord))
    #print(np.round(np.average(one_one_euclid), 4), np.round(np.average(one_one_ord), 2))
    df_use["one_one_euclid"].append(np.average(one_one_euclid))
    df_use["one_one_ord"].append(np.average(one_one_ord))
    df_use["ws"].append(ws)
    df_use["algo"].append(algo)
    df_use["num_clus"].append(num_clus)
    return (both_euclid, both_ord, none_euclid, none_ord, one_one_euclid, one_one_ord)

def did_choose_set(set_ref, ws, algo, num_clus, df_use): 
    vals_list = ["sum_main", "len_main", "avg_main",
                 "sum_20", "len_20", "avg_20",
                 "sum_5", "len_5", "avg_5",
                 "number_20_average", "number_5_average", 
                 "user_avg", "user_avg_5", "user_avg_no_skip",
                 "ws", "algo", "num_clus"]
    for v in vals_list:
        if v not in df_use:
            df_use[v] = []
            if "user_" in v:
                df_use[v.replace("user_", "algo_")] = []
                for cls in [True, False]:
                    df_use[v.replace("user_", "algo_") + "_" + str(cls)] = []
                    df_use[v + "_" + str(cls)] = []

    df_use_classes = dict()    
    for start in ["user", "algo"]:
        df_use_classes[start + "_classes_class"] = []
        df_use_classes[start + "_classes_size"] = []
        df_use_classes[start + "_classes_5_class"] = []
        df_use_classes[start + "_classes_5_size"] = []
        for cls in [True, False]:
            df_use_classes[start + "_classes_" + str(cls) + "_class"] = []
            df_use_classes[start + "_classes_" + str(cls) + "_size"] = []
            df_use_classes[start + "_classes_5_" + str(cls) + "_class"] = []
            df_use_classes[start + "_classes_5_" + str(cls) + "_size"] = []

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
        #print(np.sum(main_number) / len(main_number), np.sum(main_number), len(main_number))
        #print(np.sum(number_20) / len(number_20), np.sum(number_20), len(number_20))
        #print(np.sum(number_5) / len(number_5), np.sum(number_5), len(number_5))
        #print(np.average(number_20_average), np.average(number_5_average))
        
        df_use["sum_main"].append(np.sum(main_number))
        df_use["len_main"].append(len(main_number))
        df_use["avg_main"].append(np.sum(main_number) / len(main_number))

        df_use["sum_20"].append(np.sum(number_20))
        df_use["len_20"].append(len(number_20))
        df_use["avg_20"].append(np.sum(number_20) / len(number_20))

        df_use["sum_5"].append(np.sum(number_5))
        df_use["len_5"].append(len(number_5))
        df_use["avg_5"].append(np.sum(number_5) / len(number_5))
        
        df_use["number_20_average"].append(np.average(number_20_average))
        df_use["number_5_average"].append(np.average(number_5_average))

        break

    for cls in [True, False]:
        avg_one_cls_user_user = dict()
        avg_one_cls_user_avg_one_cls_user_user = dict()
        avg_one_cls_user_w_user = dict()
        avg_one_cls_user_avg_one_cls_user_w_user = dict()
        avg_one_cls_user_w = dict()
        avg_one_cls_user_avg_one_cls_user_w = dict()
        lenw_one_cls_user = dict()
        lenm_one_cls_user = dict()
        for user_id in dict_user_clus:
            avg_one_cls_user_user[user_id] = []
            avg_one_cls_user_w_user[user_id] = []
            avg_one_cls_user_w[user_id] = []
            lenw_one_cls_user[user_id] = dict()
            lenm_one_cls_user[user_id] = dict()
            for ref in dict_user_clus[user_id]:
                if class_of_ref[ref] != cls:
                    continue
                if min(dict_actual_20[ref], 5) != 0:
                    avg_one_cls_user_user[user_id].append(dict_user_clus[user_id][ref] / min(dict_actual_20[ref], 5))
                    avg_one_cls_user_w_user[user_id].append(dict_user_clus[user_id][ref] / 5)
                avg_one_cls_user_w[user_id].append(dict_user_clus[user_id][ref] / 5)
                if dict_actual_20[ref] not in lenw_one_cls_user[user_id]:
                    lenw_one_cls_user[user_id][dict_actual_20[ref]] = 0
                lenw_one_cls_user[user_id][dict_actual_20[ref]] += 1
                if min(dict_actual_20[ref], 5) not in lenm_one_cls_user[user_id]:
                    lenm_one_cls_user[user_id][min(dict_actual_20[ref], 5)] = 0
                lenm_one_cls_user[user_id][min(dict_actual_20[ref], 5)] += 1
            if len(avg_one_cls_user_w[user_id]) < 1:
                continue
            avg_one_cls_user_avg_one_cls_user_user[user_id] = np.average(avg_one_cls_user_user[user_id])
            avg_one_cls_user_avg_one_cls_user_w_user[user_id] = np.average(avg_one_cls_user_w_user[user_id])
            avg_one_cls_user_avg_one_cls_user_w[user_id] = np.average(avg_one_cls_user_w[user_id])
        if len(avg_one_cls_user_avg_one_cls_user_w) < 1:
            df_use["user_avg_" + str(cls)].append(0)
            df_use["user_avg_5_" + str(cls)].append(0)
            df_use["user_avg_no_skip_" + str(cls)].append(0)
            continue
        #print(np.round(np.average(list(avg_one_cls_user_avg_one_cls_user_user.values())) * 100, 2))
        #print(np.round(np.average(list(avg_one_cls_user_avg_one_cls_user_w_user.values())) * 100, 2))
        #print(np.round(np.average(list(avg_one_cls_user_avg_one_cls_user_w.values())) * 100, 2))
        df_use["user_avg_" + str(cls)].append(np.average(list(avg_one_cls_user_avg_one_cls_user_user.values())) * 100)
        df_use["user_avg_5_" + str(cls)].append(np.average(list(avg_one_cls_user_avg_one_cls_user_w_user.values())) * 100)
        df_use["user_avg_no_skip_" + str(cls)].append(np.average(list(avg_one_cls_user_avg_one_cls_user_w.values())) * 100)
        for user_id in dict_user_clus:
            #print(lenw_one_cls_user[user_id])
            #print(lenm_one_cls_user[user_id])
            for cls_v in lenw_one_cls_user[user_id]:
                df_use_classes["user_classes_" + str(cls) + "_class"].append(cls_v)
                df_use_classes["user_classes_" + str(cls) + "_size"].append(lenw_one_cls_user[user_id][cls_v])
            for cls_v in lenm_one_cls_user[user_id]:
                df_use_classes["user_classes_5_" + str(cls) + "_class"].append(cls_v)
                df_use_classes["user_classes_5_" + str(cls) + "_size"].append(lenm_one_cls_user[user_id][cls_v])
            break

    avg_all_cls_user_user = dict()
    avg_all_cls_user_avg_all_cls_user_user = dict()
    avg_all_cls_user_w_user = dict()
    avg_all_cls_user_avg_all_cls_user_w_user = dict()
    avg_all_cls_user_w = dict()
    avg_all_cls_user_avg_all_cls_user_w = dict()
    lenw_all_cls_user = dict()
    lenm_all_cls_user = dict()
    for user_id in dict_user_clus:
        avg_all_cls_user_user[user_id] = []
        avg_all_cls_user_w_user[user_id] = []
        avg_all_cls_user_w[user_id] = []
        lenw_all_cls_user[user_id] = dict()
        lenm_all_cls_user[user_id] = dict()
        for ref in dict_user_clus[user_id]:
            if min(dict_actual_20[ref], 5) != 0:
                avg_all_cls_user_user[user_id].append(dict_user_clus[user_id][ref] / min(dict_actual_20[ref], 5))
                avg_all_cls_user_w_user[user_id].append(dict_user_clus[user_id][ref] / 5)
            avg_all_cls_user_w[user_id].append(dict_user_clus[user_id][ref] / 5)
            if dict_actual_20[ref] not in lenw_all_cls_user[user_id]:
                lenw_all_cls_user[user_id][dict_actual_20[ref]] = 0
            lenw_all_cls_user[user_id][dict_actual_20[ref]] += 1
            if min(dict_actual_20[ref], 5) not in lenm_all_cls_user[user_id]:
                lenm_all_cls_user[user_id][min(dict_actual_20[ref], 5)] = 0
            lenm_all_cls_user[user_id][min(dict_actual_20[ref], 5)] += 1
        avg_all_cls_user_avg_all_cls_user_user[user_id] = np.average(avg_all_cls_user_user[user_id])
        avg_all_cls_user_avg_all_cls_user_w_user[user_id] = np.average(avg_all_cls_user_w_user[user_id])
        avg_all_cls_user_avg_all_cls_user_w[user_id] = np.average(avg_all_cls_user_w[user_id])
    #print(np.round(np.average(list(avg_all_cls_user_avg_all_cls_user_user.values())) * 100, 2), np.round(np.average(list(avg_all_cls_user_avg_all_cls_user_w_user.values())) * 100, 2), np.round(np.average(list(avg_all_cls_user_avg_all_cls_user_w.values())) * 100, 2))
    df_use["user_avg"].append(np.average(list(avg_all_cls_user_avg_all_cls_user_user.values())) * 100)
    df_use["user_avg_5"].append(np.average(list(avg_all_cls_user_avg_all_cls_user_w_user.values())) * 100)
    df_use["user_avg_no_skip"].append(np.average(list(avg_all_cls_user_avg_all_cls_user_w.values())) * 100)
    for user_id in dict_user_clus:
        #print(lenw_all_cls_user[user_id])
        #print(lenm_all_cls_user[user_id])
        for cls_v in lenw_all_cls_user[user_id]:
            df_use_classes["user_classes_class"].append(cls_v)
            df_use_classes["user_classes_size"].append(lenw_all_cls_user[user_id][cls_v])
        for cls_v in lenm_all_cls_user[user_id]:
            df_use_classes["user_classes_5_class"].append(cls_v)
            df_use_classes["user_classes_5_size"].append(lenm_all_cls_user[user_id][cls_v])
        break

    avg_all_cls_user = []
    avg_all_cls_w_user = []
    avg_all_cls_w = []
    lenw_all_cls = dict()
    lenm_all_cls = dict()
    for ref in dict_user_clus[list(dict_user_clus.keys())[0]]:
        if min(dict_actual_20[ref], 5) != 0:
            avg_all_cls_user.append(dict_actual_5[ref] / min(dict_actual_20[ref], 5))
            avg_all_cls_w_user.append(dict_actual_5[ref] / 5)
        avg_all_cls_w.append(dict_actual_5[ref] / 5)
        if dict_actual_20[ref] not in lenw_all_cls:
            lenw_all_cls[dict_actual_20[ref]] = 0
        lenw_all_cls[dict_actual_20[ref]] += 1
        if min(dict_actual_20[ref], 5) not in lenm_all_cls:
            lenm_all_cls[min(dict_actual_20[ref], 5)] = 0
        lenm_all_cls[min(dict_actual_20[ref], 5)] += 1
    #print(np.round(np.average(avg_all_cls_user) * 100, 2), np.round(np.average(avg_all_cls_w_user) * 100, 2), np.round(np.average(avg_all_cls_w) * 100, 2))
    df_use["algo_avg"].append(np.average(avg_all_cls_user) * 100)
    df_use["algo_avg_5"].append(np.average(avg_all_cls_w_user) * 100)
    df_use["algo_avg_no_skip"].append(np.average(avg_all_cls_w) * 100)
    for user_id in dict_user_clus:
        #print(lenw_all_cls)
        #print(lenm_all_cls)
        for cls_v in lenw_all_cls:
            df_use_classes["algo_classes_class"].append(cls_v)
            df_use_classes["algo_classes_size"].append(lenw_all_cls[cls_v])
        for cls_v in lenm_all_cls:
            df_use_classes["algo_classes_5_class"].append(cls_v)
            df_use_classes["algo_classes_5_size"].append(lenm_all_cls[cls_v])
        break

    for cls in [True, False]:
        avg_one_cls_user = []
        avg_one_cls_w_user = []
        avg_one_cls_w = []
        lenw_one_cls = dict()
        lenm_one_cls = dict()
        for ref in dict_user_clus[list(dict_user_clus.keys())[0]]:
            if class_of_ref[ref] != cls:
                continue
            if min(dict_actual_20[ref], 5) != 0:
                avg_one_cls_user.append(dict_actual_5[ref] / min(dict_actual_20[ref], 5))
                avg_one_cls_w_user.append(dict_actual_5[ref] / 5)
            avg_one_cls_w.append(dict_actual_5[ref] / 5)
            if dict_actual_20[ref] not in lenw_one_cls:
                lenw_one_cls[dict_actual_20[ref]] = 0
            lenw_one_cls[dict_actual_20[ref]] += 1
            if min(dict_actual_20[ref], 5) not in lenm_one_cls:
                lenm_one_cls[min(dict_actual_20[ref], 5)] = 0
            lenm_one_cls[min(dict_actual_20[ref], 5)] += 1
        if len(avg_one_cls_w) < 1:
            df_use["algo_avg_" + str(cls)].append(0)
            df_use["algo_avg_5_" + str(cls)].append(0)
            df_use["algo_avg_no_skip_" + str(cls)].append(0)
            continue
        #print(np.round(np.average(avg_one_cls_user) * 100, 2))
        #print(np.round(np.average(avg_one_cls_w_user) * 100, 2))
        #print(np.round(np.average(avg_one_cls_w) * 100, 2))
        df_use["algo_avg_" + str(cls)].append(np.average(avg_one_cls_user) * 100)
        df_use["algo_avg_5_" + str(cls)].append(np.average(avg_one_cls_w_user) * 100)
        df_use["algo_avg_no_skip_" + str(cls)].append(np.average(avg_one_cls_w) * 100)
        for user_id in dict_user_clus:
            #print(lenw_one_cls)
            #print(lenm_one_cls)
            for cls_v in lenw_one_cls:
                df_use_classes["algo_classes_" + str(cls) + "_class"].append(cls_v)
                df_use_classes["algo_classes_" + str(cls) + "_size"].append(lenw_one_cls[cls_v])
            for cls_v in lenm_one_cls:
                df_use_classes["algo_classes_5_" + str(cls) + "_class"].append(cls_v)
                df_use_classes["algo_classes_5_" + str(cls) + "_size"].append(lenm_one_cls[cls_v])
            break

    #print(np.round(np.average(list(avg_all_cls_user_avg_all_cls_user_user.values())) * 100, 2), np.round(np.average(avg_all_cls_user) * 100, 2))
    df_use["ws"].append(ws)
    df_use["algo"].append(algo)
    df_use["num_clus"].append(num_clus)

    begin_dir = "new_df_use_classes/" + str(ws) + "/" + str(algo) + "/" + str(num_clus) + "/"

    if not os.path.isdir(begin_dir):
        os.makedirs(begin_dir)
    
    for start in ["user", "algo"]:

        new_dict = {start + "_classes_class": df_use_classes[start + "_classes_class"], 
                    start + "_classes_size": df_use_classes[start + "_classes_size"]}
        df_use_classes_csv = pd.DataFrame(new_dict)
        df_use_classes_csv.to_csv(begin_dir + "df_use_classes_" + start + ".csv")

        new_dict = {start + "_classes_5_class": df_use_classes[start + "_classes_5_class"], 
                    start + "_classes_5_size": df_use_classes[start + "_classes_5_size"]}
        df_use_classes_csv = pd.DataFrame(new_dict)
        df_use_classes_csv.to_csv(begin_dir + "df_use_classes_5_" + start + ".csv")
        
        for cls in [True, False]:
            
            new_dict = {start + "_classes_" + str(cls) + "_class": df_use_classes[start + "_classes_" + str(cls) + "_class"], 
                        start + "_classes_" + str(cls) + "_size": df_use_classes[start + "_classes_" + str(cls) + "_size"]}
            df_use_classes_csv = pd.DataFrame(new_dict)
            df_use_classes_csv.to_csv(begin_dir + "df_use_classes_" + str(cls) + "_" + start + ".csv")

            new_dict = {start + "_classes_5_" + str(cls) + "_class": df_use_classes[start + "_classes_5_" + str(cls) + "_class"], 
                        start + "_classes_5_" + str(cls) + "_size": df_use_classes[start + "_classes_5_" + str(cls) + "_size"]}
            df_use_classes_csv = pd.DataFrame(new_dict)
            df_use_classes_csv.to_csv(begin_dir + "df_use_classes_5_" + str(cls) + "_" + start + ".csv")

    return np.average(list(avg_all_cls_user_avg_all_cls_user_user.values())) * 100

cluster_for_ref_10, minimaxdict10, dict_how_many_classes10 = process_ws(10)
cluster_for_ref_20, minimaxdict20, dict_how_many_classes20 = process_ws(20)

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
        
        euclid_yes_no_dict[algo][num_clus][10] = euclid_yes_no(dict_how_many_classes10[algo][num_clus][minclus10], 10, algo, num_clus, df_use_euclid)
        euclid_yes_no_dict[algo][num_clus][20] = euclid_yes_no(dict_how_many_classes20[algo][num_clus][minclus20], 20, algo, num_clus, df_use_euclid)

        did_choose_set_dict[algo][num_clus][10] = did_choose_set(dict_how_many_classes10[algo][num_clus][minclus10], 10, algo, num_clus, df_use_choose)
        did_choose_set_dict[algo][num_clus][20] = did_choose_set(dict_how_many_classes20[algo][num_clus][minclus20], 20, algo, num_clus, df_use_choose)

df_use_choose_csv = pd.DataFrame(df_use_choose)
df_use_choose_csv.to_csv("new_df_use_choose.csv")

df_use_euclid_csv = pd.DataFrame(df_use_euclid)
df_use_euclid_csv.to_csv("new_df_use_euclid.csv")
        
for num_clus in did_choose_set_dict["KMeans"]:
    printer = ""
    for algo in ["KMeans", "DBSCAN"]:
        v3 = np.round(did_choose_set_dict[algo][num_clus][10], 2)
        v6 = np.round(did_choose_set_dict[algo][num_clus][20], 2)
        if "DBSCAN" == algo:
            printer += " & " + str(len(dict_how_many_classes10[algo][num_clus])) + " & " + str(v3) + " & " + str(len(dict_how_many_classes20[algo][num_clus])) + " & " + str(v6)
        else:                
            printer += str(num_clus) + " & " + str(v3) + " & " + str(v6)
    print(printer, "\\\\ \\hline")
    
for algo in ["KMeans", "DBSCAN"]:
    for ws in [10, 20]:
        printer = ""
        for num_clus in euclid_yes_no_dict["KMeans"]:
            both_euclid, both_ord, none_euclid, none_ord, one_one_euclid, one_one_ord = euclid_yes_no_dict[algo][num_clus][ws]
            printer += str(num_clus) + " & " + str(np.round(np.average(both_euclid), 4)) + " & " + str(np.round(np.average(both_ord), 2)) + " & " + str(np.round(np.average(none_euclid), 4)) + " & " + str(np.round(np.average(none_ord), 2)) + " & " + str(np.round(np.average(one_one_euclid), 4)) + " & " + str(np.round(np.average(one_one_ord), 2)) + " \\\\ \\hline\n"
        print(printer)