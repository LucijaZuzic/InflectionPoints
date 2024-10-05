from utilities import * 
import os
from PIL import Image
from copy import deepcopy

def merge_images(x_dim, image_names, name_total_plots):
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
    #x_dim = int(np.sqrt(len(image_names)))
    #y_dim = int(np.sqrt(len(image_names)))
    #while x_dim * y_dim < len(image_names):
        #y_dim += 1
    #print(x_dim, y_dim, maxx, maxy)
    #x_dim = 7
    #y_dim = 4
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

image_names = [
    "imgmerge/1_4695799.png",
    "imgmerge/1_4718376.png",
    "imgmerge/2_9309752.png",
    "imgmerge/2_9485205.png",
    "imgmerge/3_9018208.png",
    "imgmerge/3_9149814.png",
    "imgmerge/4_9381297.png",
    "imgmerge/4_9471375.png",
    "imgmerge/6_8364490.png",
    "imgmerge/6_9433629.png",
    "imgmerge/8_8366414.png",
    "imgmerge/8_9151191.png",
    "imgmerge/9_8712338.png",
    "imgmerge/9_8892048.png",
    "imgmerge/10_9014243.png",
    "imgmerge/10_9039658.png",
    "imgmerge/11_8604891.png",
    "imgmerge/11_9003337.png",
    "imgmerge/12_8478762.png",
    "imgmerge/12_8804925.png",
    "imgmerge/13_8521037.png",
    "imgmerge/13_8569512.png",
    "imgmerge/15_9114544.png",
    "imgmerge/15_9151549.png",
    "imgmerge/16_8972258.png",
    "imgmerge/16_9206091.png",
    "imgmerge/17_8597316.png",
    "imgmerge/17_9142047.png",
]

merge_images(4, image_names, "imgmerge/image_traj_merged.png")
merge_images(7, image_names, "imgmerge/rotate_image_traj_merged.png")