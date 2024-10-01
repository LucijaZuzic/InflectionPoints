import matplotlib.pyplot as plt
import numpy as np
from utilities import *

def make_arrow(bx, by, len_arrow, angle = np.pi / 4):
    ax = bx - np.cos((angle + np.pi / 8 + 360) % 360) * len_arrow
    ay = by - np.sin((angle + np.pi / 8 + 360) % 360) * len_arrow
    plt.plot([ax, bx], [ay, by], c = "k", linestyle = "dashed", linewidth = 1)
    ax = bx - np.cos((angle - np.pi / 8 + 360) % 360) * len_arrow
    ay = by - np.sin((angle - np.pi / 8 + 360) % 360) * len_arrow
    plt.plot([ax, bx], [ay, by], c = "k", linestyle = "dashed", linewidth = 1)

def draw_dx(o, x0, y0, dx1, dx2, dy1, dy2):
    x1 = x0 + dx1
    y1 = y0 + dy1
    x2 = x1 + dx2
    y2 = y1 + dy2
    plt.subplot(4, 4, ord + 1)
    plt.rcParams['font.size'] = 20
    plt.rcParams['font.family'] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.axis("equal") 
    plt.axis("off") 
    binstr = str(bin(o).replace("0b", ""))
    while len(binstr) < 4:
        binstr = "0" + binstr
    plt.title(str(hex(o)).replace("0x", "").capitalize() + " (" + binstr + ")")
    minx = min(min(x0, x1), x2) - 0.2
    miny = min(min(y0, y1), y2) - 0.2
    maxx = max(max(x0, x1), x2) + 0.2
    maxy = max(max(y0, y1), y2) + 0.2
    if binstr in ["0000", "0011", "1100", "1111"]:
        print("yes")
        plt.fill_between([minx, maxx], miny, maxy, color = "yellow")
    plt.plot([0, 0], [miny, maxy], c = "k", linestyle = "dashed", linewidth = 1)
    plt.plot([minx, maxx], [0, 0], c = "k", linestyle = "dashed", linewidth = 1)
    if y2 > y0 or y1 > y0:
        make_arrow(0, maxy, 0.1, angle = np.pi / 2)
    else:
        make_arrow(0, miny, 0.1, angle = 3 * np.pi / 2)
    if x2 > x0 or x1 > x0:
        make_arrow(maxx, 0, 0.1, angle = np.pi * 2)
    else:
        make_arrow(minx, 0, 0.1, angle = np.pi)
    plt.plot([x0, x1, x2], [y0, y1, y2], c = "k", linewidth = 2)
    plt.scatter([x0], [y0], c = "r", zorder = 2, linewidth = 3)
    plt.scatter([x1], [y1], c = "g", zorder = 2, linewidth = 3)
    plt.scatter([x2], [y2], c = "b", zorder = 2, linewidth = 3)

xs = 0
ys = 0

yr1 = 1

xr2 = 1
yr2 = 1

ord = 0

plt.figure(figsize=(10, 10), dpi = 80)
for xd1 in range(2):
    for xd2 in range(2):
        for yd1 in range(2):
            for yd2 in range(2):
                if xd1 != xd2 and yd1 != yd2:
                    xr1 = np.sqrt(2)
                else:
                    xr1 = 1
                draw_dx(ord, xs, ys, - xr1 + 2 * xd1 * xr1, - xr2 + 2 * xd2 * xr2, - yr1 + 2 * yd1 * yr1, - yr2 + 2 * yd2 * yr2)
                ord += 1
plt.savefig("class_illustrate_3.png", bbox_inches = "tight")
plt.close()
 
plt.figure(figsize=(10, 12), dpi = 80)
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.axis("equal") 
plt.axis("off") 
long = np.arange(1,3,0.1)
print(len(long))
lat = np.cos(long) 

long_diff = [long[i] - long[0] for i in range(len(long))]
lat_diff = [lat[i] - lat[0] for i in range(len(long))] 
points = set([(long[i], lat[i]) for i in range(len(long))])
    
angle_all = []
radius_all = []
for i in range(1, len(long_diff)):
    radius_all.append(np.sqrt(lat_diff[i] ** 2 + long_diff[i] ** 2)) 
    angle_all.append(np.arctan2(lat_diff[i], long_diff[i])) 

long_new = [radius_all[i] * np.cos(angle_all[i] - angle_all[-1]) for i in range(len(radius_all))]
lat_new = [radius_all[i] * np.sin(angle_all[i] - angle_all[-1]) for i in range(len(radius_all))] 

long_new.insert(0, 0)
lat_new.insert(0, 0)

long_new2, lat_new2 = preprocess_long_lat(long_new, lat_new)

minx = min(min(min(long), min(long_new2)), min(long_new)) - 0.2
miny = min(min(min(lat), min(lat_new2)), min(lat_new)) - 0.2
maxx = max(max(max(long), max(long_new2)), max(long_new)) + 0.2
maxy = max(max(max(lat), max(lat_new2)), max(lat_new)) + 0.2

plt.title("Visual demonstration of trajectory preprocessing")
plt.plot([0, 0], [miny, maxy], c = "k", linestyle = "dashed", linewidth = 1)
plt.plot([minx, maxx], [0, 0], c = "k", linestyle = "dashed", linewidth = 1)
make_arrow(0, maxy, 0.1, angle = np.pi / 2)
make_arrow(maxx, 0, 0.1, angle = np.pi * 2)
plt.plot(long, lat, linewidth = 2, label = "Original trajectory")
plt.plot(long_new, lat_new, linewidth = 2, label = "Translated to a $0$ $x$ and $y$ starting coordinate and rotated")
plt.plot(long_new2, lat_new2, linewidth = 2, label = "Translated trajectory to eliminate negative values")
plt.scatter(long_new2, lat_new2, c = "b", zorder = 2, linewidth = 3, label = "Other points")

long_sgn = [long_new2[i + 1] > long_new2[i] for i in range(len(long_new2) - 1)]
lat_sgn = [lat_new2[i + 1] > lat_new2[i] for i in range(len(lat_new2) - 1)]

long_change_sgn = [long_sgn[i + 1] != long_sgn[i] for i in range(len(long_sgn) - 1)]
lat_change_sgn = [lat_sgn[i + 1] != lat_sgn[i] for i in range(len(lat_sgn) - 1)]

infls_long = []
infls_lat = []
infls_long_lat = []
mrkr = ""
for i in range(len(long_change_sgn)):
    if long_change_sgn[i] or lat_change_sgn[i] :
        infls_long_lat.append(i + 1)
        comp_str_long = str(int(long_sgn[i])) + str(int(long_sgn[i + 1]))
        comp_str_lat= str(int(lat_sgn[i])) + str(int(lat_sgn[i + 1]))
        int_comp = int(comp_str_long + comp_str_lat, base = 2)
        mrkr += str(hex(int_comp))[2:]
    if long_change_sgn[i]:
        infls_long.append(i + 1)
    if lat_change_sgn[i]:
        infls_lat.append(i + 1) 

print(mrkr)
print(infls_long)
print(infls_lat)

for num in infls_long:
    plt.scatter(long_new2[num], lat_new2[num], c = "r", zorder = 2, linewidth = 3)
for num in infls_lat:
    plt.scatter(long_new2[num], lat_new2[num], c = "r", zorder = 2, linewidth = 3, label = "Inflection point")
plt.legend()
plt.savefig("rotate_illustrate_3.png", bbox_inches = "tight")
plt.close()