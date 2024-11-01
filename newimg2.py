from utilities import *
import matplotlib.pyplot as plt
from matplotlib import rc
cm = 1/2.54  # centimeters in inches

def step_from_seq(seq):
    xs = 0
    ys = 0

    yr1 = 1

    xr2 = 1
    yr2 = 1

    ords = 1
    positionsx = [xs]
    positionsy = [ys]
    positionss = [ords]
    for s in seq:
        s_int = int("0x" + s, 16)
        binstr = str(bin(s_int)).replace("0b", "")
        while len(binstr) < 4:
            binstr = "0" + binstr
        xd1, xd2, yd1, yd2 = int(binstr[0]), int(binstr[1]), int(binstr[2]), int(binstr[3])

        if xd1 != xd2 and yd1 != yd2:
            xr1 = np.sqrt(2)
        else:
            xr1 = 1

        xs = xs - xr1 + 2 * xd1 * xr1
        ys = ys - xr2 + 2 * xd2 * xr2
        positionsx.append(xs)
        positionsy.append(ys)
        positionss.append(ords)
        xs = xs - yr1 + 2 * yd1 * yr1
        ys = ys - yr2 + 2 * yd2 * yr2
        positionsx.append(xs)
        positionsy.append(ys)
        positionss.append(ords)
        ords += 1

    plt.ylim(min(min(positionsx), min(positionsy)) - 1, 1 + max(max(positionsx), max(positionsy)))
    plt.xlim(min(min(positionsx), min(positionsy)) - 1, 1 + max(max(positionsx), max(positionsy)))
    plt.plot(positionsx, positionsy)
    plt.scatter(positionsx, positionsy, s = 3)
    print(len(positionsx))
    for ix_p in range(len(positionsx)):
        textp_prev = str(ix_p - 1) + " 3"
        textp_curr = str(ix_p) + " 2"
        textp_next = str(ix_p + 1) + " 1"
        textp = ""
        if ix_p > 1:
            textp += textp_prev + "\n"
        if ix_p > 0 and ix_p < len(positionsx) - 1:
            textp += textp_curr + "\n"
        if ix_p < len(positionsx) - 2:
            textp += textp_next + "\n"
        textp += str(positionss[ix_p])
        if (ix_p - 2) % 2 == 0 and ix_p > 0 and ix_p < len(positionss) - 1:
            textp += ", " + str(positionss[ix_p] + 1)
        #plt.text(positionsx[ix_p], positionsy[ix_p], textp)

    plt.show()
    plt.close()

all_subdirs = os.listdir("markers")
 
classes = {"I": 0, "D": 0, "NF": 0, "NM": 0}
num_infls_long = dict()
num_infls_lat = dict()
num_infls_all = dict()
num_infls_mrkr = dict()

anomaly_classes = set()
non_anomaly_classes = set()

included = [
    "1_4695799",
    "1_4718376",
    "2_9309752",
    "2_9485205",
    "3_9018208",
    "3_9149814",
    "4_9381297",
    "4_9471375",
    "6_8364490",
    "6_9433629",
    "8_8366414",
    "8_9151191",
    "9_8712338",
    "9_8892048",
    "10_9014243",
    "10_9039658",
    "11_8604891",
    "11_9003337",
    "12_8478762",
    "12_8804925",
    "13_8521037",
    "13_8569512",
    "15_9114544",
    "15_9151549",
    "16_8972258",
    "16_9206091",
    "17_8597316",
    "17_9142047"
]
#ededede8b212edede
arr10 = [
    "e",
    "ede", 
    "ed", 
    "eded", 
    "edede", 
    "e8", 
    "ededed"
]
arr20 = [
    "e",
    "ede",
    "ed", 
    "edede",
    "eded", 
    "ededed", 
    "ededede", 
    "e8",
    "b2",
    "edededed",
    "edededede",
    "e81"
]
#step_from_seq('dededededede8b8b8b8b8b8')
#for a in arr10:
    #step_from_seq(a)
#for a in arr20:
    #step_from_seq(a)

for subdir_name in all_subdirs:
    break
    for ws in [10]:
        for some_file in os.listdir("markers/" + subdir_name + "/" + str(ws) + "/"):    
            
            events = subdir_name.replace("Vehicle_", "") + some_file.replace("events", "").replace(".csv", "")

            if events in included:
                
                file_marker = pd.read_csv("markers/" + subdir_name + "/" + str(ws) + "/" + some_file, sep = ";", index_col = False)
                prev_ix = 0
                mrk_arr = []
                for ix_mrk in range(len(file_marker["marker"])):
                    if ix_mrk > 0 and file_marker["marker"][ix_mrk] != file_marker["marker"][ix_mrk - 1]:
                        if len(str(file_marker["marker"][prev_ix]).replace("nan", "")) > 0:    
                            mrk_arr.append((prev_ix, prev_ix + 10, str(file_marker["marker"][prev_ix]).replace("nan", "")))
                        prev_ix = ix_mrk
                if len(str(file_marker["marker"][prev_ix]).replace("nan", "")) > 0: 
                    mrk_arr.append((prev_ix, prev_ix + 10, str(file_marker["marker"][prev_ix]).replace("nan", "")))
                if len(mrk_arr) < 100:
                    print(events)
                    print(len(mrk_arr))
                    print(mrk_arr)
                    mrk_arr_merge = mrk_arr
                    for ix in range(len(mrk_arr_merge) - 1):
                        if str(mrk_arr_merge[ix][2]) == "nan":
                            mrk_arr_merge[ix] = ""
                    while len(mrk_arr_merge) > 1:
                        arr_new = []
                        for ix1 in range(len(mrk_arr_merge) - 1):
                            s1, e1, m1 = mrk_arr_merge[ix1]
                            s2, e2, m2 = mrk_arr_merge[ix1 + 1]
                            if (s1 >= s2 and s1 <= e2) or (e1 >= s2 and e1 <= e2):
                                s3 = min(s1, s2)
                                e3 = max(e1, e2)
                                m3 = m1 + m2
                                for ix1 in range(len(m1)):
                                    for ix2 in range(len(m2)):
                                        if m1[ix1:] == m2[:len(m2)-ix2] and len(m1[:ix1] + m2) < len(m3):
                                            m3 = m1[:ix1] + m2
                                arr_new.append((s3, e3, m3))
                        mrk_arr_merge = arr_new
                    last_ix = mrk_arr[-1][1]
                    print(last_ix)
                    print(mrk_arr_merge)
                    step_from_seq(mrk_arr_merge[0][2], last_ix)

                    dict_mrk_overlaps = {ix: [] for ix in range(last_ix)}
                    for ix_mrk in range(len(mrk_arr)):
                        for ix_new in range(mrk_arr[ix_mrk][0], mrk_arr[ix_mrk][1]):
                            dict_mrk_overlaps[ix_new].append(mrk_arr[ix_mrk])

                    dict_mrk_start_after = {ix: [] for ix in range(last_ix)}
                    for ix_mrk1 in range(last_ix):
                        for ix_mrk2 in range(len(mrk_arr)):
                            if mrk_arr[ix_mrk2][0] >= ix_mrk1:
                                dict_mrk_start_after[ix_mrk1].append(mrk_arr[ix_mrk2])

def make_arrow(bx, by, len_arrow, angle = np.pi / 4):
    ax = bx - np.cos((angle + np.pi / 8 + 360) % 360) * len_arrow
    ay = by - np.sin((angle + np.pi / 8 + 360) % 360) * len_arrow
    plt.plot([ax, bx], [ay, by], c = "k", linestyle = "dashed", linewidth = 0.25)
    ax = bx - np.cos((angle - np.pi / 8 + 360) % 360) * len_arrow
    ay = by - np.sin((angle - np.pi / 8 + 360) % 360) * len_arrow
    plt.plot([ax, bx], [ay, by], c = "k", linestyle = "dashed", linewidth = 0.25)

plt.rcParams["svg.fonttype"] = "none"
rc('font',**{'family':'Arial'})
#plt.rcParams.update({"font.size": 5})
SMALL_SIZE = 5
MEDIUM_SIZE = 5
BIGGER_SIZE = 5

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.figure(figsize=(29.7/4*cm, 29.7/5*cm), dpi = 300)
plt.axis("equal") 
plt.axis("off") 
long = np.arange(1,3.5,0.1)
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

plt.title("Visual demonstration of splitting a trajectory")
plt.plot([0, 0], [miny, maxy], c = "k", linestyle = "dashed", linewidth = 0.5)
plt.plot([minx, maxx], [0, 0], c = "k", linestyle = "dashed", linewidth = 0.5)
make_arrow(0, maxy, 0.1, angle = np.pi / 2)
make_arrow(maxx, 0, 0.1, angle = np.pi * 2)
plt.plot(long_new2, lat_new2, linewidth = 0.5, label = "Trajectory")
ofs = {1: 0.2, 2: -0.2}
linestyle_window = {1: {10: "dashdot", 20: "dotted"}, 2: {10: "dashed", 20: "solid"}}
start_marker_window = {1: "s", 2: "o"}
end_marker_window = {1: {10: "D", 20: "d"}, 2: {10: ">", 20: "<"}}
color_window = {1:"r", 2: "g"}
for ix in [1, 2]:
    for ws in [10, 20]:

        x1 = [long_new2[ix]]
        y1 = [lat_new2[ix]]
        if ws == 10:
            plt.scatter(x1, y1, c = color_window[ix], marker = start_marker_window[ix], s = 3, zorder = 3, label = "Start of window " + str(ix))
        else:
            plt.scatter(x1, y1, c = color_window[ix], marker = start_marker_window[ix], s = 3, zorder = 3)

        x2 = [long_new2[ix], long_new2[ix]]
        y2 = [lat_new2[ix], lat_new2[ix] + ofs[ix] * ws / 10]
        plt.plot(x2, y2, linewidth = 0.5, c = color_window[ix], linestyle = linestyle_window[ix][ws])
        
        x3 = [long_new2[ix + ws], long_new2[ix + ws]]
        y3 = [lat_new2[ix + ws], lat_new2[ix + ws] + ofs[ix] * ws / 10]
        plt.plot(x3, y3, linewidth = 0.5, c = color_window[ix], linestyle = linestyle_window[ix][ws], label = "Points in window " + str(ix) + " for window size " + str(ws))
        
        x4 = [long_new2[ix + ws]]
        y4 = [lat_new2[ix + ws]]
        plt.scatter(x4, y4, c = color_window[ix], marker = end_marker_window[ix][ws], s = 3, zorder = 3, label = "End of window " + str(ix) + " for window size " + str(ws))
        
        for nix in range(ix, ix + ws):
            x5 = [long_new2[nix], long_new2[nix + 1]]
            y5 = [lat_new2[nix] + ofs[ix] * ws / 10, lat_new2[nix + 1] + ofs[ix] * ws / 10]
            plt.plot(x5, y5, linewidth = 0.5, c = color_window[ix], linestyle = linestyle_window[ix][ws])
plt.xlim(minx, maxx)
plt.ylim(miny, maxy - 1)
plt.legend(ncol = 2, loc = "upper left", bbox_to_anchor = (0.1, 0.6))
plt.savefig("splitting_new1.png", bbox_inches = "tight")
plt.savefig("splitting_new1.pdf", bbox_inches = "tight")
plt.savefig("splitting_new1.svg", bbox_inches = "tight")
plt.close()