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

    dict_actual_5 = dict()
    dict_actual_20 = dict()
    dict_how_many_classes = dict()
    for algo in ["DBSCAN", "KMeans"]:
        dict_actual_5[algo] = dict()
        dict_actual_20[algo] = dict()
        dict_how_many_classes[algo] = dict()
        for num_clus in list_clus:
            dict_actual_5[algo][num_clus] = dict()
            dict_actual_20[algo][num_clus] = dict()
            dict_how_many_classes[algo][num_clus] = set()

    for ix in range(len(distance_json["compare_to"])):
        merge_reference = str(distance_json["compare_to"][ix]["vehicle"]) + "_" + str(distance_json["compare_to"][ix]["ride"])
        dict_actual[merge_reference] = dict() 
        for algo in ["DBSCAN", "KMeans"]:
            for num_clus in list_clus:
                dict_actual_5[algo][num_clus][merge_reference] = 0
                dict_actual_20[algo][num_clus][merge_reference] = 0
        for other_ix in range(len(distance_json["compare_to"][ix]["similar"])):
            other_reference = str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_vehicle"]) + "_" + str(distance_json["compare_to"][ix]["similar"][other_ix]["compare_ride"])
            dist_ref = distance_json["compare_to"][ix]["similar"][other_ix]["distance"]
            ord_ref = distance_json["compare_to"][ix]["similar"][other_ix]["order"]
            dict_actual[merge_reference][other_reference] = (ord_ref, dist_ref)
            for algo in ["DBSCAN", "KMeans"]:
                for num_clus in list_clus:
                    cls_me = class_file[algo][num_clus][merge_reference]
                    cls_other = class_file[algo][num_clus][other_reference]
                    dict_how_many_classes[algo][num_clus].add(cls_me)
                    dict_how_many_classes[algo][num_clus].add(cls_other)
                    if cls_me == cls_other:
                        dict_actual_20[algo][num_clus][merge_reference] += 1
                        if ord_ref < 5 * 114 + 1:
                            dict_actual_5[algo][num_clus][merge_reference] += 1
    
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
    for algo in ["DBSCAN", "KMeans"]:
        dict_user_clus[algo] = dict()
        for num_clus in list_clus:
            dict_user_clus[algo][num_clus] = dict()

    for user_id_file in os.listdir("marked/" + str(ws)):
        user_id = user_id_file.replace("_" + str(ws) + ".csv", "")
        if user_id in banned: 
            continue  
        dict_user[user_id] = dict()
        for algo in ["DBSCAN", "KMeans"]:
            for num_clus in list_clus:
                dict_user_clus[algo][num_clus][user_id] = dict()
        file_user_id = pd.read_csv("marked/" + str(ws) + "/" + user_id_file, sep = ";", index_col = False)
        for ix in range(len(file_user_id["vehicle"])): 
            merge_reference = str(file_user_id["vehicle"][ix]) + "_" + str(file_user_id["ride"][ix])
            dict_user[user_id][merge_reference] = file_user_id["chosen"][ix].split(":")
            dict_user[user_id][merge_reference] = [oi.split("_")[0] + "_" + oi.split("_")[1] for oi in dict_user[user_id][merge_reference]]
            for algo in ["DBSCAN", "KMeans"]:
                for num_clus in list_clus:
                    dict_user_clus[algo][num_clus][user_id][merge_reference] = 0
                    for other_reference in dict_user[user_id][merge_reference]:
                        cls_me = class_file[algo][num_clus][merge_reference]
                        cls_other = class_file[algo][num_clus][other_reference]
                        dict_how_many_classes[algo][num_clus].add(cls_me)
                        dict_how_many_classes[algo][num_clus].add(cls_other)
                        if cls_me == cls_other:
                            dict_user_clus[algo][num_clus][user_id][merge_reference] += 1 

    for algo in dict_user_clus:
        strtarget = algo + " Target classes " + str(ws)
        strclus = algo + " Actual classes " + str(ws)
        str1 = algo + " 5 " + str(ws)
        str2 = algo + " 20 " + str(ws)
        str3 = algo + " user " + str(ws)
        if "DBSCAN" == algo:
            print(strtarget, "&", strclus, "&", str2, "&", str1, "&", str3, "\\\\ \\hline")
        else:
            print(strtarget, "&", str2, "&", str1, "&", str3, "\\\\ \\hline")
        for num_clus in dict_user_clus[algo]:
            avg_5 = list(dict_actual_5[algo][num_clus].values())
            avg_20 = list(dict_actual_20[algo][num_clus].values())
            avg_user = dict()
            avg_avg_user = dict()
            for user_id in dict_user_clus[algo][num_clus]:
                avg_user[user_id] = list(dict_user_clus[algo][num_clus][user_id].values())
                avg_avg_user[user_id] = np.average(avg_user[user_id])
            avg_avg_avg_user = list(avg_avg_user.values())
            v1 = np.round(np.average(avg_5) / 5 * 100, 2)
            v2 = np.round(np.average(avg_20) / 20 * 100, 2)
            v3 = np.round(np.average(avg_avg_avg_user) / 5 * 100, 2)
            strtarget += " & $" + str(num_clus) + "$"
            strclus += " & $" + str(len(dict_how_many_classes[algo][num_clus])) + "$"
            str1 += " & $" + str(v1) + "$"
            str2 += " & $" + str(v2) + "$"
            str3 += " & $" + str(v3) + "$"
            #print(algo, num_clus, np.average(avg_20), np.average(avg_5), np.average(avg_avg_avg_user))
            if "DBSCAN" == algo:
                print(num_clus, "&", len(dict_how_many_classes[algo][num_clus]), "&", v2, "&", v1, "&", v3, "\\\\ \\hline")
            else:
                print(num_clus, "&", v2, "&", v1, "&", v3, "\\\\ \\hline")
        print(strtarget, "\\\\ \\hline")
        if "DBSCAN" == algo:
            print(strclus, "\\\\ \\hline")
        print(str2, "\\\\ \\hline")
        print(str1, "\\\\ \\hline")
        print(str3, "\\\\ \\hline")

    return dict_user_clus, dict_actual_5, dict_actual_20, dict_how_many_classes

def merge_ws(dict_user_clus1, dict_actual_51, dict_actual_201, dict_how_many_classes1, dict_user_clus2, dict_actual_52, dict_actual_202, dict_how_many_classes2):
    for algo in dict_user_clus1:
        strtarget = algo + " Target classes 10"
        strclus = algo + " Actual classes 10"
        str1 = algo + " 5 10"
        str2 = algo + " 20 10"
        str3 = algo + " user 10"
        strtarget2 = algo + " Target classes 20"
        strclus2 = algo + " Actual classes 20"
        str4 = algo + " 5 20"
        str5 = algo + " 20 20"
        str6 = algo + " user 20"
        if "DBSCAN" == algo:
            print(strtarget, "&", strclus, "&", str2, "&", str1, "&", str3, "&", strclus2, "&", str5, "&", str4, "&", str6, "\\\\ \\hline")
        else:
            print(strtarget, "&", str2, "&", str1, "&", str3, "&", str5, "&", str4, "&", str6, "\\\\ \\hline")
        for num_clus in dict_user_clus1[algo]:
            avg_5 = list(dict_actual_51[algo][num_clus].values())
            avg_20 = list(dict_actual_201[algo][num_clus].values())
            avg_user = dict()
            avg_avg_user = dict()
            for user_id in dict_user_clus1[algo][num_clus]:
                avg_user[user_id] = list(dict_user_clus1[algo][num_clus][user_id].values())
                avg_avg_user[user_id] = np.average(avg_user[user_id])
            avg_avg_avg_user = list(avg_avg_user.values())
            v1 = np.round(np.average(avg_5) / 5 * 100, 2)
            v2 = np.round(np.average(avg_20) / 20 * 100, 2)
            v3 = np.round(np.average(avg_avg_avg_user) / 5 * 100, 2)
            strtarget += " & $" + str(num_clus) + "$"
            strclus += " & $" + str(len(dict_how_many_classes1[algo][num_clus])) + "$"
            str1 += " & $" + str(v1) + "$"
            str2 += " & $" + str(v2) + "$"
            str3 += " & $" + str(v3) + "$"
            avg_25 = list(dict_actual_52[algo][num_clus].values())
            avg_220 = list(dict_actual_202[algo][num_clus].values())
            avg_2user = dict()
            avg_2avg_2user = dict()
            for user_id in dict_user_clus2[algo][num_clus]:
                avg_2user[user_id] = list(dict_user_clus2[algo][num_clus][user_id].values())
                avg_2avg_2user[user_id] = np.average(avg_2user[user_id])
            avg_2avg_2avg_2user = list(avg_2avg_2user.values())
            v4 = np.round(np.average(avg_25) / 5 * 100, 2)
            v5 = np.round(np.average(avg_220) / 20 * 100, 2)
            v6 = np.round(np.average(avg_2avg_2avg_2user) / 5 * 100, 2)
            strtarget2 += " & $" + str(num_clus) + "$"
            strclus2 += " & $" + str(len(dict_how_many_classes2[algo][num_clus])) + "$"
            str4 += " & $" + str(v4) + "$"
            str5 += " & $" + str(v5) + "$"
            str6 += " & $" + str(v6) + "$"
            if "DBSCAN" == algo:
                print(num_clus, "&", len(dict_how_many_classes1[algo][num_clus]), "&", v2, "&", v1, "&", v3, "&", len(dict_how_many_classes2[algo][num_clus]), "&", v5, "&", v4, "&", v6, "\\\\ \\hline")
            else:
                print(num_clus, "&", v2, "&", v1, "&", v3, "&", v5, "&", v4, "&", v6, "\\\\ \\hline")
        print(strtarget, "\\\\ \\hline")
        if "DBSCAN" == algo:
            print(strclus, "\\\\ \\hline")
        print(str2, "\\\\ \\hline")
        print(str1, "\\\\ \\hline")
        print(str3, "\\\\ \\hline")
        if "DBSCAN" == algo:
            print(strclus2, "\\\\ \\hline")
        print(str5, "\\\\ \\hline")
        print(str4, "\\\\ \\hline")
        print(str6, "\\\\ \\hline")

dict_user_clus1, dict_actual_51, dict_actual_201, dict_how_many_classes1 = process_ws(10)
dict_user_clus2, dict_actual_52, dict_actual_202, dict_how_many_classes2 = process_ws(20)

merge_ws(dict_user_clus1, dict_actual_51, dict_actual_201, dict_how_many_classes1, dict_user_clus2, dict_actual_52, dict_actual_202, dict_how_many_classes2)