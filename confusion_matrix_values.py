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
  
    return {"actual": binary_actual, "user": binary_user, "other_reference": dict_actual}

def calculate_conf_matrix(actual, predicted):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for ix in range(len(actual)):
        if actual[ix] == 1:
            if predicted[ix] == 1:
                tp += 1
            else:
                fn += 1
        else:
            if predicted[ix] == 0:
                tn += 1
            else:
                fp += 1
    dicti_metrics = {"TP": tp, "TN": tn, "FP": fp, "FN": fn}
    #calculate_metrics(dicti_metrics)
    return dicti_metrics

def calculate_metrics(metric_set):
    tp, tn, fp, fn = metric_set["TP"], metric_set["TN"], metric_set["FP"], metric_set["FN"]
    tpr = "NA"
    fnr = "NA"
    if tp + fn > 0:
        tpr = tp / (tp + fn)
        fnr = 1 - tpr
    tnr = "NA"
    fpr = "NA"
    if tn + fp > 0:
        tnr = tn / (tn + fp)
        fpr = 1 - tnr
    ppv = "NA"
    fdr = "NA"
    if tp + fp > 0:
        ppv = tp / (tp + fp)
        fdr = 1 - ppv
    npv = "NA"
    for_new = "NA"
    if tn + fn > 0:
        npv = tn / (tn + fn)
        for_new = 1 - npv
    prev_y = (tp + fn) / (tp + fp + fn + tn)
    det_prev_y = (tp + fp) / (tp + fp + fn + tn)
    prev_n = (tn + fp) / (tp + fp + fn + tn)
    det_prev_n = (tn + fn) / (tp + fp + fn + tn)
    dr_y = tp / (tp + fp + fn + tn)
    dr_n = tn / (tp + fp + fn + tn)
    acc = (tp + tn) / (tp + fp + fn + tn)
    ba = "NA"
    if tpr != "NA" and tnr != "NA":
        ba = (tpr + tnr) / 2
    f1 = "NA"
    if ppv != "NA" and tpr != "NA" and ppv + tpr > 0:
        f1 = 2 * ppv * tpr / (ppv + tpr)
    #print(tp, tn, fp, fn, tp + fn, tn + fp, tp + fn + tn + fp)
    #print(tpr, tnr, ppv, npv)
    #print(fnr, fpr, fdr, for_new)
    #print(prev_y, det_prev_y, dr_y)
    #print(prev_n, det_prev_n, dr_n)
    #print(acc, ba, f1)
    return {"Sensitivity": tpr,
            "FNR": fnr,
            "Specificity": tnr,
            "FPR": fpr,
            "PPV": ppv,
            "FDR": fdr,
            "NPV": npv,
            "FOR": for_new,
            "DR (P)": dr_y,
            "DR (N)": dr_n,
            "DP (P)": det_prev_y,
            "DP (N)": det_prev_n,
            "P (P)": prev_y,
            "P (N)": prev_n,
            "Acc": acc,
            "BA": ba,
            "F1": f1}

def get_clusters_for_refere(file_cluster_name):
    pd_file = pd.read_csv(file_cluster_name, index_col = False)
    dicti_clus = dict()
    add_val = int(-1 in pd_file["cluster"])
    for ix in range(len(pd_file["cluster"])):
        clus = pd_file["cluster"][ix] + add_val
        vehicle = pd_file["vehicle"][ix]
        ride = pd_file["ride"][ix]
        refe = vehicle.split("_")[-1] + "_" + ride.split("_")[-1]
        dicti_clus[refe] = clus
    return dicti_clus

cluster_dict = {"KMeans": dict()}

for method in os.listdir("clustered_new/DBSCAN"):
    dir_path = "clustered_new/DBSCAN/" + method + "/346/all_percent_1/"
    file_names = os.listdir(dir_path)
    cluster_dict["DBSCAN_" + method] = dict()
    for file_path in file_names:
        ws = int(file_path.replace(".csv", "").split("_")[-1])
        cluster_dict["DBSCAN_" + method][ws] = get_clusters_for_refere(dir_path + file_path)

dir_path = "clustered_new/KMeans/2/all_percent_1/"
file_names = os.listdir(dir_path)
for file_path in file_names:
    ws = int(file_path.replace(".csv", "").split("_")[-1])
    cluster_dict["KMeans"][ws] = get_clusters_for_refere(dir_path + file_path)
    
cluster_other = dict()
list_ret = dict()
for ws in cluster_dict["KMeans"]:
    cluster_other[ws] = dict()
    list_ret[ws] = process_ws(ws)
    for model in cluster_dict:
        cluster_other[ws][model] = dict()
        for refe in cluster_dict[model][ws]:
            cluster_original = cluster_dict[model][ws][refe]
            cluster_other[ws][model][refe] = []
            for other_reference in list_ret[ws]["other_reference"][refe]:
                cluster_other[ws][model][refe].append(cluster_dict[model][ws][other_reference] == cluster_original)

values_metrics = {"no clus": dict()}
for model in cluster_dict:
    values_metrics[model] = dict()
for ws in cluster_other:
    values_metrics["no clus"][ws] = dict()
    for user in list_ret[ws]["user"]:
        values_metrics["no clus"][ws][user] = dict()
        for refe in list_ret[ws]["user"][user]:
            values_metrics["no clus"][ws][user][refe] = calculate_conf_matrix(list_ret[ws]["actual"][refe], list_ret[ws]["user"][user][refe])
    for model in cluster_dict:
        values_metrics[model][ws] = dict()
        values_metrics[model][ws]["actual"] = dict()
        for refe in list_ret[ws]["actual"]:
            values_metrics[model][ws]["actual"][refe] = calculate_conf_matrix(cluster_other[ws][model][refe], list_ret[ws]["actual"][refe])
        for user in list_ret[ws]["user"]:
            values_metrics[model][ws][user] = dict()
            for refe in list_ret[ws]["user"][user]:
                values_metrics[model][ws][user][refe] = calculate_conf_matrix(cluster_other[ws][model][refe], list_ret[ws]["user"][user][refe])
             
merge_by_user = dict()
merge_all = dict()
merge_all_user = dict()
merge_all_actual = dict()

for model in values_metrics:
    merge_by_user[model] = dict()
    if "clus" in model:
        merge_all[model] = dict()
    else:
        merge_all_user[model] = dict()
        merge_all_actual[model] = dict()
    for ws in values_metrics[model]:
        merge_by_user[model][ws] = dict()
        if "clus" in model:
            merge_all[model][ws] = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
        else:
            merge_all_user[model][ws] = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
            merge_all_actual[model][ws] = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
        for user in values_metrics[model][ws]:
            merge_by_user[model][ws][user] = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
            for refe in values_metrics[model][ws][user]:
                tp, tn, fp, fn = values_metrics[model][ws][user][refe]["TP"], values_metrics[model][ws][user][refe]["TN"], values_metrics[model][ws][user][refe]["FP"], values_metrics[model][ws][user][refe]["FN"]
                old_user_tp, old_user_tn, old_user_fp, old_user_fn = merge_by_user[model][ws][user]["TP"], merge_by_user[model][ws][user]["TN"], merge_by_user[model][ws][user]["FP"], merge_by_user[model][ws][user]["FN"]
                merge_by_user[model][ws][user] = {"TP": old_user_tp + tp, "TN": old_user_tn + tn, "FP": old_user_fp + fp, "FN": old_user_fn + fn}
                if "clus" in model:
                    old_tp, old_tn, old_fp, old_fn = merge_all[model][ws]["TP"], merge_all[model][ws]["TN"], merge_all[model][ws]["FP"], merge_all[model][ws]["FN"]
                    merge_all[model][ws] = {"TP": old_tp + tp, "TN": old_tn + tn, "FP": old_fp + fp, "FN": old_fn + fn}
                else:
                    if "actual" in user:
                        old_all_user_tp, old_all_user_tn, old_all_user_fp, old_all_user_fn = merge_all_actual[model][ws]["TP"], merge_all_actual[model][ws]["TN"], merge_all_actual[model][ws]["FP"], merge_all_actual[model][ws]["FN"]
                        merge_all_actual[model][ws] = {"TP": old_all_user_tp + tp, "TN": old_all_user_tn + tn, "FP": old_all_user_fp + fp, "FN": old_all_user_fn + fn}
                    else:
                        old_all_user_tp, old_all_user_tn, old_all_user_fp, old_all_user_fn = merge_all_user[model][ws]["TP"], merge_all_user[model][ws]["TN"], merge_all_user[model][ws]["FP"], merge_all_user[model][ws]["FN"]
                        merge_all_user[model][ws] = {"TP": old_all_user_tp + tp, "TN": old_all_user_tn + tn, "FP": old_all_user_fp + fp, "FN": old_all_user_fn + fn}

print_dict = dict()
for model in merge_by_user:
    if "clus" in model:
        print_dict["User vs. Algo."] = dict()
    else:
        print_dict["User vs. " + model] = dict()
        print_dict["Algo. vs. " + model] = dict()
    for ws in merge_by_user[model]:
        if "clus" in model:
            print_dict["User vs. Algo."][ws] = merge_all[model][ws]
            cm = calculate_metrics(merge_all[model][ws])
            for c in cm:
                print_dict["User vs. Algo."][ws][c] = cm[c]
        else:
            print_dict["User vs. " + model][ws] = merge_all_user[model][ws]
            cm = calculate_metrics(merge_all_user[model][ws])
            for c in cm:
                print_dict["User vs. " + model][ws][c] = cm[c]
            print_dict["Algo. vs. " + model][ws] = merge_all_actual[model][ws]
            cm = calculate_metrics(merge_all_actual[model][ws])
            for c in cm:
                print_dict["Algo. vs. " + model][ws][c] = cm[c]
                
str_pr = "Model"
for model in print_dict:
    if "knee" in model:
        continue
    str_pr += " & \\multicolumn{" + str(len(print_dict[model])) + "}{|c|}{" + model.split("_")[0] + "}"
print("\t\t" + str_pr + " \\\\ \\hline")
str_pr = "Window size"
for model in print_dict:
    if "knee" in model:
        continue
    for ws in print_dict[model]:
        str_pr += " & $" + str(ws) + "$"
print("\t\t" + str_pr + " \\\\ \\hline")
str_pr = "P"
for model in print_dict:
    if "knee" in model:
        continue
    for ws in print_dict[model]:
        v = print_dict[model][ws]["TP"] + print_dict[model][ws]["FN"]
        str_pr += " & $" + str(v) + "$"
print("\t\t" + str_pr + " \\\\ \\hline")
str_pr = "N"
for model in print_dict:
    if "knee" in model:
        continue
    for ws in print_dict[model]:
        v = print_dict[model][ws]["TN"] + print_dict[model][ws]["FP"]
        str_pr += " & $" + str(v) + "$"
print("\t\t" + str_pr + " \\\\ \\hline")
str_pr = "T"
for model in print_dict:
    if "knee" in model:
        continue
    for ws in print_dict[model]:
        v = print_dict[model][ws]["TP"] + print_dict[model][ws]["FN"] + print_dict[model][ws]["TN"] + print_dict[model][ws]["FP"]
        str_pr += " & $" + str(v) + "$"
print("\t\t" + str_pr + " \\\\ \\hline")
for key_val in print_dict["User vs. Algo."][10]:
    str_pr = key_val
    for model in print_dict:
        if "knee" in model:
            continue
        for ws in print_dict[model]:
            v = print_dict[model][ws][key_val]
            if v != "NA":
                if v < 1:
                    v = "$" + str(np.round(v * 100, 2)) + "$"
                else:
                    v = "$" + str(v) + "$"
            str_pr += " & " + v
    print("\t\t" + str_pr + " \\\\ \\hline")