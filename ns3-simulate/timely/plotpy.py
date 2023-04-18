import  matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import  ConnectionPatch
import torch
plt.rcParams["font.sans-serif"]=["SimHei"]
rtt = []
rate = []
for i in range(19):
    file = open("{}.txt".format(i+2),"r")
    line = file.readline()
    for i in range(5):
        line = file.readline()
    while line:
        line = line.split(",")
        if float(line[0].split("[")[1])<110000:
            rtt.append(float(line[0].split("[")[1]))
            rate.append(float(line[1].split(" ")[1]))
        line = file.readline()


def zone_and_linked(ax, axins, zone_left, zone_right, x, y, linked='bottom',
                    x_ratio=0.05, y_ratio=0.05):
    """缩放内嵌图形，并且进行连线
    ax:         调用plt.subplots返回的画布。例如： fig,ax = plt.subplots(1,1)
    axins:      内嵌图的画布。 例如 axins = ax.inset_axes((0.4,0.1,0.4,0.3))
    zone_left:  要放大区域的横坐标左端点
    zone_right: 要放大区域的横坐标右端点
    x:          X轴标签
    y:          列表，所有y值
    linked:     进行连线的位置，{'bottom','top','left','right'}
    x_ratio:    X轴缩放比例
    y_ratio:    Y轴缩放比例
    """
    xlim_left = x[zone_left] - (x[zone_right] - x[zone_left]) * x_ratio
    xlim_right = x[zone_right] + (x[zone_right] - x[zone_left]) * x_ratio

    y_data = np.hstack([yi[zone_left:zone_right] for yi in y])
    ylim_bottom = np.min(y_data) - (np.max(y_data) - np.min(y_data)) * y_ratio
    ylim_top = np.max(y_data) + (np.max(y_data) - np.min(y_data)) * y_ratio

    axins.set_xlim(xlim_left, xlim_right)
    axins.set_ylim(ylim_bottom, ylim_top)

    ax.plot([xlim_left, xlim_right, xlim_right, xlim_left, xlim_left],
            [ylim_bottom, ylim_bottom, ylim_top, ylim_top, ylim_bottom], "black")

    if linked == 'bottom':
        xyA_1, xyB_1 = (xlim_left, ylim_top), (xlim_left, ylim_bottom)
        xyA_2, xyB_2 = (xlim_right, ylim_top), (xlim_right, ylim_bottom)
    elif linked == 'top':
        xyA_1, xyB_1 = (xlim_left, ylim_bottom), (xlim_left, ylim_top)
        xyA_2, xyB_2 = (xlim_right, ylim_bottom), (xlim_right, ylim_top)
    elif linked == 'left':
        xyA_1, xyB_1 = (xlim_right, ylim_top), (xlim_left, ylim_top)
        xyA_2, xyB_2 = (xlim_right, ylim_bottom), (xlim_left, ylim_bottom)
    elif linked == 'right':
        xyA_1, xyB_1 = (xlim_left, ylim_top), (xlim_right, ylim_top)
        xyA_2, xyB_2 = (xlim_left, ylim_bottom), (xlim_right, ylim_bottom)

    con = ConnectionPatch(xyA=xyA_1, xyB=xyB_1, coordsA="data",
                          coordsB="data", axesA=axins, axesB=ax)
    axins.add_artist(con)
    con = ConnectionPatch(xyA=xyA_2, xyB=xyB_2, coordsA="data",
                          coordsB="data", axesA=axins, axesB=ax)
    axins.add_artist(con)

#print(rtt,rate)

# print(torch.mean(torch.tensor(rtt))/1000,torch.mean(torch.tensor(rate)),max(rtt)/1000)
# rtt = sorted(rtt)
# print(rtt[int(len(rtt)*0.99)]/1000)
# fig, ax = plt.subplots(1,1,figsize=(12,7))
# ax.plot(rtt,".")
# plt.xlabel("RTT采集次数")
# plt.ylabel("RTT/us")
# axins = ax.inset_axes((0.3, 0.4, 0.3, 0.3))
# axins.plot(rtt,".")
# zone_and_linked(ax, axins, 700, 1200, np.arange(1,len(rtt)+1) ,[np.array(rtt)], 'right')
# plt.plot(rtt)
# plt.show()

print(torch.mean(torch.tensor(rtt))/1000)
print(torch.sum(torch.tensor(rtt)*torch.tensor(rtt)*torch.tensor(rate))/(1000*torch.sum(torch.tensor(rtt)*torch.tensor(rate))))
print(torch.sum(torch.tensor(rate)*torch.tensor(rtt))/torch.sum(torch.tensor(rtt)))
print(max(rtt)/1000)
rtt = sorted(rtt)
print(rtt[int(len(rtt)*0.99)]/1000)
