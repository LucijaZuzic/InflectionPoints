import os
import pandas as pd
import matplotlib.pyplot as plt
#import cmap

#cm = cmap.Colormap('cividis:cividis')
#print(cm)

plt.figure()
ix = 0
red_list = []
green_list = []
blue_list = []
cyan_list = []
magenta_list = []
yellow_list = []
for num in range(19, -1, -1):
    component = str(hex(135 + num * 6)).replace("0x", "")
    while len(component) < 2:
        component = "0" + component
    red_list.append("#" + component + "00" * 2)
    plt.scatter(ix, ix, color = "#" + component + "00" * 2)
    green_list.append("#00" + component + "00")
    plt.scatter(20 + ix, 20 + ix, color = "#00" + component + "00")
    blue_list.append("#0000" + component)
    plt.scatter(40 + ix, 40 +  ix, color = "#0000" + component)
    cyan_list.append("#00" + component * 2)
    plt.scatter(60 + ix, 60 + ix, color = "#00" + component * 2)
    magenta_list.append("#" + component + "00" + component)
    plt.scatter(80 + ix, 80 + ix, color = "#" + component + "00" + component)
    yellow_list.append("#" + component * 2 + "00")
    plt.scatter(100 + ix, 100 + ix, color = "#" + component * 2 + "00")
    ix += 1
plt.show()
plt.close()

color_used = []
step = len(red_list)
while len(color_used) < 6 * len(red_list) and step >= 1:
    for sp in range(0, len(red_list), step):
        if red_list[sp] not in color_used:
            color_used.append(red_list[sp])
        if green_list[sp] not in color_used:
            color_used.append(green_list[sp])
        if blue_list[sp] not in color_used:
            color_used.append(blue_list[sp])
        if cyan_list[sp] not in color_used:
            color_used.append(cyan_list[sp])
        if magenta_list[sp] not in color_used:
            color_used.append(magenta_list[sp])
        if yellow_list[sp] not in color_used:
            color_used.append(yellow_list[sp])
    step = step // 2

plt.figure()
ix = 0
for num in range(len(color_used)):
    plt.scatter(ix, ix, color = color_used[num])
    ix += 1
plt.show()
plt.close()

plt.figure()
ix = 0
yellow_list = []
blue_list = []
for num in range(60):
    blue_part = str(hex(15 + num * 2)).replace("0x", "")
    while len(blue_part) < 2:
        blue_part = "0" + blue_part
    yellow_part = str(hex(240 - num * 2)).replace("0x", "")
    while len(yellow_part) < 2:
        yellow_part = "0" + yellow_part
    yellow_list.append("#" + yellow_part * 2 + blue_part)
    plt.scatter(119 - ix, 119 - ix, color = "#" + yellow_part * 2 + blue_part)
    blue_list.append("#" + blue_part * 2 + yellow_part)
    plt.scatter(ix, ix, color = "#" + blue_part * 2 + yellow_part)
    ix += 1
plt.show()
plt.close()

color_used = []
step = len(yellow_list)
while len(color_used) < 2 * len(yellow_list) and step >= 1:
    for sp in range(0, len(yellow_list), step):
        if yellow_list[sp] not in color_used:
            color_used.append(yellow_list[sp])
        if blue_list[sp] not in color_used:
            color_used.append(blue_list[sp])
    step = step // 2

plt.figure()
ix = 0
for num in range(len(color_used)):
    plt.scatter(ix, ix, color = color_used[num])
    ix += 1
plt.show()
plt.close()

ix = 0
color_dict = dict()
for num1 in range(11):
    p1 = str(hex(243 - 23 * num1)).replace("0x", "")
    while len(p1) < 2:
        p1 = "0" + p1
    for num2 in range(11):
        p2 = str(hex(243 - 23 * num2)).replace("0x", "")
        while len(p2) < 2:
            p2 = "0" + p2
        if num1 not in color_dict:
            color_dict[num1] = dict()
        color_dict[num1][num2] = "#" + p1 * 2 + p2

color_used = []

for sum in range(255, -1, -1):
    for c1 in sorted(list(color_dict.keys())):
        for c3 in sorted(list(color_dict[c1].keys()), reverse = True):
            if c1 > c3 and c1 + c3 == sum and color_dict[c1][c3] not in color_used:
                color_used.append(color_dict[c1][c3])

for sum in range(256):
    for c1 in sorted(list(color_dict.keys())):
        for c3 in sorted(list(color_dict[c1].keys()), reverse = True):
            if c1 <= c3 and c3 + c1 == sum and color_dict[c1][c3] not in color_used:
                color_used.append(color_dict[c1][c3])

plt.figure()
ix = 0
for num in range(len(color_used)):
    plt.scatter(ix, ix, color = color_used[num])
    ix += 1
plt.show()
plt.close()