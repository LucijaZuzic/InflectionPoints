from utilities import *
total = 0
for subdir_name in os.listdir("cleaned_json"):
    total_json = len(os.listdir("cleaned_json/" + subdir_name)) - 1 
    total_png = len(os.listdir("cleaned_png/" + subdir_name))
    total += total_png
    print(total_json, total_png)
print(total)


for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name): 
        if os.path.isfile("marker_count/" + subdir_name + "/" + csv_file.replace(".csv", ".npy")): 
            os.remove("marker_count/" + subdir_name + "/" + csv_file.replace(".csv", ".npy"))