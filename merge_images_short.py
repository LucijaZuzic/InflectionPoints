from utilities import * 
import os
from PIL import Image
from copy import deepcopy

def merge_images(image_names, name_total_plots):
    maxx = 0
    maxy = 0
    for order_num in range(len(image_names)):
        image = Image.open(image_names[order_num])
        x, y = image.size
        maxx = max(maxx, x)
        maxy = max(maxy, y)
    images = []
    sizes_x = []
    sizes_y = []
    x_dim = int(np.sqrt(len(image_names)))
    y_dim = int(np.sqrt(len(image_names)))
    while x_dim * y_dim < len(image_names):
        y_dim += 1
    print(x_dim, y_dim, maxx, maxy)
    x_dim = 5
    y_dim = 4
    rownum = []
    colnum = []
    x_start = []
    y_start = []
    rownum_current = 0
    colnum_current = 0
    x_start_current = 0
    y_start_current = 0
    for order_num in range(len(image_names)):
        image = Image.open(image_names[order_num])
        x, y = image.size
        images.append(image)
        sizes_x.append(x)
        sizes_y.append(y)  
        rownum.append(rownum_current)
        colnum.append(colnum_current)
        x_start.append(x_start_current)
        y_start.append(y_start_current)
        if colnum_current == x_dim - 1:
            rownum_current += 1
            colnum_current = 0
            y_start_current += maxy
            x_start_current = 0
        else:
            colnum_current += 1
            x_start_current += maxx
    x_size = max(x_start) + maxx
    y_size = max(y_start) + maxy
    new_image = Image.new("RGB", (x_size, y_size), (255,255,255))
    for order_num in range(len(images)):
        new_image.paste(images[order_num], (x_start[order_num], y_start[order_num]))  
    new_image.save(name_total_plots, "PNG")   

list_clus = list(range(2, 21))

for subdir_name in os.listdir("marker_count"):
    
    for csv_file in os.listdir("marker_count/" + subdir_name):

        if ".csv" not in csv_file:
            
            continue  

        if "_all_percent_1_20" not in csv_file and "_all_percent_1_10" not in csv_file:
            
            continue

        print(csv_file) 

        for algo in ["DBSCAN", "KMeans"]:

            image_names = []

            for num_clus in list_clus:

                if not os.path.isdir("clustered/" + algo + "/" + str(num_clus) + "/" + subdir_name):
                    
                    os.makedirs("clustered/" + algo + "/" + str(num_clus) + "/" + subdir_name)  
                
                new_name_png = "clustered/" + algo + "/" + str(num_clus) + "/" + subdir_name + "/clustered_" + algo + "_" + str(num_clus) + "_" + csv_file
                new_name_png = new_name_png.replace(".csv", "_no_legend.png")
                image_names.append(new_name_png)

            ws = 10
            if "20" in csv_file:
                ws = 20
            print(len(image_names))
            merge_images(image_names, "clustered/" + algo + "/" + str(ws) + "_" + algo + "_merged_all_short.png")