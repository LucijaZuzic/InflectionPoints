from utilities import *

for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        if "_all_percent_1_" not in csv_file:
            
            continue 

        if "_all_percent_1_5" in csv_file:
            
            continue 

        if "_all_percent_1_15" in csv_file:
            
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

        used_dict = []
        for colname in set_used:
            used_dict.append((colname_sum[colname] / sumsums, colname_sum[colname], colname))
        used_dict = sorted(used_dict)
        for val in used_dict:
            if val[0] > 10 ** -2:
                print(val)

        minisum = (1000000, 1, 1, 1)
        maxisum = (-1000000, 1, 1, 1)
        for ix in range(len(file_csv)):
            totalsum = 0
            for colname in file_csv.columns[3:]:
                totalsum += file_csv[colname][ix]
            somesum = 0
            for colname in set_used:
                somesum += file_csv[colname][ix] 
            if totalsum != 0 and somesum / totalsum > maxisum[0]:
                maxisum = (somesum / totalsum, somesum, totalsum, ix)
            if totalsum != 0 and somesum / totalsum < minisum[0]:
                minisum = (somesum / totalsum, somesum, totalsum, ix)
        print(minisum, maxisum)