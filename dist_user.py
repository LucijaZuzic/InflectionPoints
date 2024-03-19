import os
import pandas as pd
import numpy as np

def process_ws(ws):
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

    usable_ref = set()
    for user_id_file in os.listdir("marked/" + str(ws)):
        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])):
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            usable_ref.add(merge_reference)
        break

    all_euclidean = []
    usable_euclidean = []

    euclidean_min_min = 10000
    euclidean_max_min = -10000
    euclidean_min_max = 10000
    euclidean_max_max = -10000

    euclidean_min_min_usable = 10000
    euclidean_max_min_usable = -10000
    euclidean_min_max_usable = 10000
    euclidean_max_max_usable = -10000

    euclidean_min = dict()
    euclidean_max = dict()
    for merge_reference in dict_actual:
        euclidean_min[merge_reference] = 0
        euclidean_max[merge_reference] = 0
        for other_reference in dict_actual[merge_reference]:
            if dict_actual[merge_reference][other_reference][0] < 1 + 114 * 5:
                euclidean_min[merge_reference] += dict_actual[merge_reference][other_reference][1]
            if dict_actual[merge_reference][other_reference][0] > 1 + 114 * 14:
                euclidean_max[merge_reference] += dict_actual[merge_reference][other_reference][1]
        euclidean_min_min = min(euclidean_min_min, euclidean_min[merge_reference])
        euclidean_max_min = max(euclidean_max_min, euclidean_min[merge_reference])
        euclidean_min_max = min(euclidean_min_max, euclidean_max[merge_reference])
        euclidean_max_max = max(euclidean_max_max, euclidean_max[merge_reference])
        all_euclidean.append(euclidean_max[merge_reference] - euclidean_min[merge_reference])
        if merge_reference in usable_ref:
            usable_euclidean.append(euclidean_max[merge_reference] - euclidean_min[merge_reference])
            euclidean_min_min_usable = min(euclidean_min_min_usable, euclidean_min[merge_reference])
            euclidean_max_min_usable = max(euclidean_max_min_usable, euclidean_min[merge_reference])
            euclidean_min_max_usable = min(euclidean_min_max_usable, euclidean_max[merge_reference])
            euclidean_max_max_usable = max(euclidean_max_max_usable, euclidean_max[merge_reference])

    euclidean_min_to_max = abs(euclidean_min_max - euclidean_max_min)
    euclidean_max_to_min = euclidean_max_max - euclidean_min_min

    euclidean_min_to_max_usable = abs(euclidean_min_max_usable - euclidean_max_min_usable)
    euclidean_max_to_min_usable = euclidean_max_max_usable - euclidean_min_min_usable

    dict_user = dict()
    euclidean_user = dict()
    euclidean_percent_user = dict()
    ord_user = dict()
    ix_user = dict()
    fq_user = dict()

    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        dict_user[user_id] = dict()
        euclidean_user[user_id] = dict()
        euclidean_percent_user[user_id] = dict()
        ord_user[user_id] = dict()
        ix_user[user_id] = {ix: 0 for ix in range(0, 20)}
        fq_user[user_id] = dict()
        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])):
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            euclidean_user[user_id][merge_reference] = 0
            euclidean_percent_user[user_id][merge_reference] = 0
            ord_user[user_id][merge_reference] = 0
            fq_user[user_id][merge_reference] = 0
            dict_user[user_id][merge_reference] = file_user_id["chosen"][ix].split(":")
            dict_user[user_id][merge_reference] = [oi.split("_")[0] + "_" + oi.split("_")[1] for oi in dict_user[user_id][merge_reference]]
            for other_reference in dict_user[user_id][merge_reference]:
                num_use = (dict_actual[merge_reference][other_reference][0] - 1) // 114
                ix_user[user_id][num_use] += 1
                if num_use < 5:
                    fq_user[user_id][merge_reference] += 1
                ord_user[user_id][merge_reference] += num_use
                euclidean_user[user_id][merge_reference] += dict_actual[merge_reference][other_reference][1]
            euclidean_user[user_id][merge_reference] -= euclidean_min[merge_reference]
            euclidean_percent_user[user_id][merge_reference] = euclidean_user[user_id][merge_reference] / (euclidean_max[merge_reference] - euclidean_min[merge_reference]) * 100
            ord_user[user_id][merge_reference] -= np.sum(list(range(5)))
        print(np.sum(list(ord_user[user_id].values())), len(ord_user[user_id]), np.sum(list(ord_user[user_id].values())) / len(ord_user[user_id]), np.sum(list(range(15, 20))), np.sum(list(range(5))), np.sum(list(range(15, 20))) - np.sum(list(range(5))), np.sum(list(ord_user[user_id].values())) / len(ord_user[user_id]) / (np.sum(list(range(15, 20))) - np.sum(list(range(5)))) * 100)
        print(np.sum(list(fq_user[user_id].values())), len(fq_user[user_id]), np.sum(list(fq_user[user_id].values())) / len(fq_user[user_id]), np.sum(list(fq_user[user_id].values())) / len(fq_user[user_id]) / 5 * 100) 
        for ix in range(0, 5):
            print(ix, ix_user[user_id][ix], len(ord_user[user_id]), ix_user[user_id][ix] / len(ord_user[user_id]) * 100)
        print(np.sum(list(euclidean_user[user_id].values())), len(euclidean_user[user_id]), np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]))
        print(np.sum(list(euclidean_percent_user[user_id].values())), len(euclidean_percent_user[user_id]), np.sum(list(euclidean_percent_user[user_id].values())) / len(euclidean_percent_user[user_id]))
        print(np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]), np.average(usable_euclidean), np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]) / np.average(usable_euclidean) * 100)
        print(np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]), np.quantile(usable_euclidean, 0.5), np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]) / np.quantile(usable_euclidean, 0.5) * 100)
        print(np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]), np.max(usable_euclidean), np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]) / np.max(usable_euclidean) * 100)
        print(np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]), np.min(usable_euclidean), np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]) / np.min(usable_euclidean) * 100)
        print(euclidean_min_max_usable, euclidean_max_min_usable, euclidean_min_to_max_usable, np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]), euclidean_min_to_max_usable, np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]) / euclidean_min_to_max_usable * 100)
        print(euclidean_max_max_usable, euclidean_min_min_usable, euclidean_max_to_min_usable, np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]), euclidean_max_to_min_usable, np.sum(list(euclidean_user[user_id].values())) / len(euclidean_user[user_id]) / euclidean_max_to_min_usable * 100)
  
    dict_all = dict()
    euclidean_all = dict()
    euclidean_percent_all = dict()
    ord_all = dict()
    ix_all = {ix: 0 for ix in range(0, 20)}
    fq_all = dict()

    for user_id in dict_user:
        for ix in range(0, 20):
            ix_all[ix] += ix_user[user_id][ix]
        for merge_reference in dict_user[user_id]:
            nr = user_id + "_" + merge_reference
            dict_all[nr] = dict_user[user_id][merge_reference]
            euclidean_all[nr] = euclidean_user[user_id][merge_reference]
            euclidean_percent_all[nr] = euclidean_percent_user[user_id][merge_reference]
            ord_all[nr] = ord_user[user_id][merge_reference] 
            fq_all[nr] = fq_user[user_id][merge_reference]
    
    print(np.sum(list(ord_all.values())), len(ord_all), np.sum(list(ord_all.values())) / len(ord_all), np.sum(list(range(15, 20))), np.sum(list(range(5))), np.sum(list(range(15, 20))) - np.sum(list(range(5))), np.sum(list(ord_all.values())) / len(ord_all) / (np.sum(list(range(15, 20))) - np.sum(list(range(5)))) * 100)
    print(np.sum(list(fq_all.values())), len(fq_all), np.sum(list(fq_all.values())) / len(fq_all), np.sum(list(fq_all.values())) / len(fq_all) / 5 * 100) 
    for ix in range(0, 5):
        print(ix, ix_all[ix], len(ord_all), ix_all[ix] / len(ord_all) * 100)
    print(np.sum(list(euclidean_all.values())), len(euclidean_all), np.sum(list(euclidean_all.values())) / len(euclidean_all))
    print(np.sum(list(euclidean_percent_all.values())), len(euclidean_percent_all), np.sum(list(euclidean_percent_all.values())) / len(euclidean_percent_all))
    print(np.sum(list(euclidean_all.values())) / len(euclidean_all), np.average(usable_euclidean), np.sum(list(euclidean_all.values())) / len(euclidean_all) / np.average(usable_euclidean) * 100)
    print(np.sum(list(euclidean_all.values())) / len(euclidean_all), np.quantile(usable_euclidean, 0.5), np.sum(list(euclidean_all.values())) / len(euclidean_all) / np.quantile(usable_euclidean, 0.5) * 100)
    print(np.sum(list(euclidean_all.values())) / len(euclidean_all), np.max(usable_euclidean), np.sum(list(euclidean_all.values())) / len(euclidean_all) / np.max(usable_euclidean) * 100)
    print(np.sum(list(euclidean_all.values())) / len(euclidean_all), np.min(usable_euclidean), np.sum(list(euclidean_all.values())) / len(euclidean_all) / np.min(usable_euclidean) * 100)
    print(euclidean_min_max_usable, euclidean_max_min_usable, euclidean_min_to_max_usable, np.sum(list(euclidean_all.values())) / len(euclidean_all), euclidean_min_to_max_usable, np.sum(list(euclidean_all.values())) / len(euclidean_all) / euclidean_min_to_max_usable * 100)
    print(euclidean_max_max_usable, euclidean_min_min_usable, euclidean_max_to_min_usable, np.sum(list(euclidean_all.values())) / len(euclidean_all), euclidean_max_to_min_usable, np.sum(list(euclidean_all.values())) / len(euclidean_all) / euclidean_max_to_min_usable * 100)
  
process_ws(10)
process_ws(20)