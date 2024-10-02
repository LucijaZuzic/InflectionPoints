import os
import pandas as pd 
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

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

    print("Remove", euclidean_max_max_usable, euclidean_min_min_usable, euclidean_max_to_min_usable)
 
    euclidean_actual = dict()
    binary_actual = dict()
    selected_actual = dict()
    
    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        if user_id in banned: 
            continue  
        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])): 
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            euclidean_actual[merge_reference] = []
            for other_reference in dict_actual[merge_reference]:
                euclidean_actual[merge_reference].append(dict_actual[merge_reference][other_reference][1])
            euclidean_actual[merge_reference] = sorted(euclidean_actual[merge_reference])[:5]
            binary_actual[merge_reference] = [0 for ix in range(0, 20)]
            for ix in range(0, 5):
                binary_actual[merge_reference][ix] = 1
            selected_actual[merge_reference] = list(range(0, 5))
        break
  
    dict_user = dict()

    euclidean_user = dict()
    binary_user = dict()
    selected_user = dict()

    euclidean_flat_actual_all = []
    binary_flat_actual_all = []
    selected_flat_actual_all = []

    euclidean_flat_predicted_all = []
    binary_flat_predicted_all = []
    selected_flat_predicted_all = []

    euclidean_flat_actual_user = dict()
    binary_flat_actual_user = dict()
    selected_flat_actual_user = dict()

    euclidean_flat_predicted_user = dict()
    binary_flat_predicted_user = dict()
    selected_flat_predicted_user = dict()
      
    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        if user_id in banned: 
            continue  

        dict_user[user_id] = dict()
        binary_user[user_id] = dict()
        selected_user[user_id] = dict()
        euclidean_user[user_id] = dict()

        euclidean_flat_actual_user[user_id] = []
        binary_flat_actual_user[user_id] = []
        selected_flat_actual_user[user_id] = []

        euclidean_flat_predicted_user[user_id] = []
        binary_flat_predicted_user[user_id] = []
        selected_flat_predicted_user[user_id] = []

        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])):
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            binary_user[user_id][merge_reference] = [0 for ix in range(0, 20)]
            selected_user[user_id][merge_reference] = []
            euclidean_user[user_id][merge_reference] = []
            dict_user[user_id][merge_reference] = file_user_id["chosen"][ix].split(":")
            dict_user[user_id][merge_reference] = [oi.split("_")[0] + "_" + oi.split("_")[1] for oi in dict_user[user_id][merge_reference]]
            for other_reference in dict_user[user_id][merge_reference]:
                num_use = (dict_actual[merge_reference][other_reference][0] - 1) // 114
                binary_user[user_id][merge_reference][num_use] += 1 
                selected_user[user_id][merge_reference].append(num_use)
                euclidean_user[user_id][merge_reference].append(dict_actual[merge_reference][other_reference][1])
            selected_user[user_id][merge_reference] = sorted(selected_user[user_id][merge_reference])
            for s_ix in range(len(selected_user[user_id][merge_reference])):
                selected_flat_actual_user[user_id].append(selected_actual[merge_reference][s_ix])
                selected_flat_predicted_user[user_id].append(selected_user[user_id][merge_reference][s_ix])
                selected_flat_actual_all.append(selected_actual[merge_reference][s_ix])
                selected_flat_predicted_all.append(selected_user[user_id][merge_reference][s_ix])
            euclidean_user[user_id][merge_reference] = sorted(euclidean_user[user_id][merge_reference])
            for e_ix in range(len(euclidean_user[user_id][merge_reference])):
                euclidean_flat_actual_user[user_id].append(euclidean_actual[merge_reference][e_ix])
                euclidean_flat_predicted_user[user_id].append(euclidean_user[user_id][merge_reference][e_ix])
                euclidean_flat_actual_all.append(euclidean_actual[merge_reference][e_ix])
                euclidean_flat_predicted_all.append(euclidean_user[user_id][merge_reference][e_ix])
            for b_ix in range(len(binary_user[user_id][merge_reference])):
                binary_flat_actual_user[user_id].append(binary_actual[merge_reference][b_ix])
                binary_flat_predicted_user[user_id].append(binary_user[user_id][merge_reference][b_ix])
                binary_flat_actual_all.append(binary_actual[merge_reference][b_ix])
                binary_flat_predicted_all.append(binary_user[user_id][merge_reference][b_ix]) 
            if len(euclidean_actual[merge_reference]) != len(euclidean_user[user_id][merge_reference]):
                print("ERROR", user_id, merge_reference)
           
    printed = False
    sel = []
    euc = []
    fq = []
    dd = dict()
    for i in range(5):
        dd[i] = []
    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        if user_id in banned: 
            continue
        for ix in range(len(file_user_id["vehicle"])):
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            sel.append(abs(np.sum(selected_actual[merge_reference]) - np.sum(selected_user[user_id][merge_reference])))
            euc.append(abs(np.sum(euclidean_actual[merge_reference]) - np.sum(euclidean_user[user_id][merge_reference])))
            fq.append(sum([x < 5 for x in selected_user[user_id][merge_reference]]) / len(selected_user[user_id][merge_reference]))
            for i in range(5):
                dd[i].append(int(i in selected_user[user_id][merge_reference]))
            if not printed and abs(np.sum(euclidean_actual[merge_reference]) - np.sum(euclidean_user[user_id][merge_reference])) > euclidean_min_min_usable:
                printed = True
                print(euclidean_user[user_id][merge_reference])
                print(euclidean_actual[merge_reference])
                print(np.sum(euclidean_actual[merge_reference]),)
                print(np.sum(euclidean_user[user_id][merge_reference]))
                print(abs(np.sum(euclidean_actual[merge_reference]) - np.sum(euclidean_user[user_id][merge_reference])))
                print(euclidean_max_to_min_usable, euclidean_max_max_usable, euclidean_min_min_usable)
                print(abs(np.sum(euclidean_actual[merge_reference]) - np.sum(euclidean_user[user_id][merge_reference])) / euclidean_max_to_min_usable)
                print(selected_actual[merge_reference])
                print([x * 114 + 1 for x in selected_actual[merge_reference]])
                print(selected_user[user_id][merge_reference])
                print([x * 114 + 1 for x in selected_user[user_id][merge_reference]])
                print(np.sum(selected_actual[merge_reference]), np.sum(selected_user[user_id][merge_reference]), abs(np.sum(selected_actual[merge_reference]) - np.sum(selected_user[user_id][merge_reference])), abs(np.sum(selected_actual[merge_reference]) - np.sum(selected_user[user_id][merge_reference])) / 75)
                print(sum([x < 5 for x in selected_user[user_id][merge_reference]]), sum([x < 5 for x in selected_user[user_id][merge_reference]]) / len(selected_user[user_id][merge_reference]))
                #print(sel[-1], euc[-1], fq[-1])
                #for i in range(5):
                    #print(dd[i][-1])

    return sel, euc, fq, dd
            
sel1, euc1, fq1, dd1 = process_ws(10)
sel2, euc2, fq2, dd2 = process_ws(20)
pairs_to_test = {"Selection": (sel1, sel2), "Euclid": (euc1, euc2),  "Quartile": (fq1, fq2)}
for i in dd1:
    pairs_to_test[i] = (dd1[i], dd2[i])

for kp in pairs_to_test:
    p = pairs_to_test[kp]
    for ix in [0, 1]:
        un, pvn = stats.normaltest(p[ix]) 
        us, pvs = stats.shapiro(p[ix])
        uk, pvk = stats.kstest(p[ix], 'norm')
        #if pvn < 0.05 or pvs < 0.05 or pvk < 0.05:
            #print(kp, "not normal for ws", ix)
    #print(stats.ttest_ind(p[0], p[1], equal_var = False))
    if False:
        plt.figure()
        plt.title(kp)
        plt.hist(p[0], label = "10")
        plt.hist(p[1], label = "20")
        plt.legend()
        plt.show()
        plt.close()
    urs, pvrs = stats.ranksums(p[0], p[1])
    umw, pvmw = stats.mannwhitneyu(p[0], p[1])
    #if pvn < 0.05 or pvs < 0.05 or pvk < 0.05:
        #print(kp, "not equal for ws")
        #print(urs, pvrs)
        #print(umw, pvmw)
        #print(np.mean(p[0]), np.mean(p[1]))