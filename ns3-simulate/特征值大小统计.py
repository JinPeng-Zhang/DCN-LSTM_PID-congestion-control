'''
特征值绝对值CDF统计
'''
from torch import  nn,optim
import torch
import  matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"]
from matplotlib.pyplot import MultipleLocator
def get_i_l(x):
    input = []
    output = (rttl[x+1]-rtts[x])/rtts[x]
    for i in range(3):
        input.append((rttl[x-i]-rtts[x-i])/rtts[x-i])
    return input,output

lt = []
alls =[]
for k in range(16):
    file1 = open("dipcc/dipcc_test6/{}.txt".format(k+2))
    line = file1.readline()
    rttl = []
    # while line:
    #     rtt,rateo,raten = line.split(",")
    #     rtt = float(rtt.split("[")[1])
    #     rttl.append(rtt)
    #     line = file1.readline()


    while line:
        rtt,_ = line.split(" ")
        rtt = float(rtt)
        rttl.append(rtt)
        line = file1.readline()
    rttl = rttl[5:]
    a = 0.8###平滑值对于模型预测十分重要，经测试0.8的处理效果最好

    rtts = []
    rttlable = []
    for i in range(len(rttl)):
        if i == 0:
            rtts.append(rttl[i])
        else:
            rtts.append((1-a)*rttl[i]+a*rtts[i-1])
    for i in range(len(rtts)-3):
        input,output = get_i_l(i+2)
        o = abs(input[0])
        alls.append(o)

    #########

#hpcc
# print(max(alls)) #0.9066387484403156
# step = 92
# CDF = []
# for i in range(step):
#     CDF.append(sum(j<0.01*i for j in alls)/len(alls))
# plt.xlabel("Kt绝对值")
# plt.ylabel("CDF")
# plt.title("timely")
# x_major_locator=MultipleLocator(0.08)
# #把x轴的刻度间隔设置为1，并存在变量里
# y_major_locator=MultipleLocator(0.1)
# #把y轴的刻度间隔设置为10，并存在变量里
# ax=plt.gca()
# #ax为两条坐标轴的实例
# ax.xaxis.set_major_locator(x_major_locator)
# #把x轴的主刻度设置为1的倍数
# ax.yaxis.set_major_locator(y_major_locator)
#
# plt.plot([0.01*i for i in range(step)],CDF)
# plt.show()
#file.close()


#timely
#print(max(alls)) #3.771734403743888
# step = 379
# CDF = []
# for i in range(step):
#     CDF.append(sum(j<0.01*i for j in alls)/len(alls))
# print(CDF[-4:])
# plt.xlabel("Kt绝对值")
# plt.ylabel("CDF")
# plt.title("timely")
# x_major_locator=MultipleLocator(0.4)
# #把x轴的刻度间隔设置为1，并存在变量里
# y_major_locator=MultipleLocator(0.1)
# #把y轴的刻度间隔设置为10，并存在变量里
# ax=plt.gca()
# #ax为两条坐标轴的实例
# ax.xaxis.set_major_locator(x_major_locator)
# #把x轴的主刻度设置为1的倍数
# ax.yaxis.set_major_locator(y_major_locator)
#
# plt.plot([0.01*i for i in range(step)],CDF)
# plt.show()



#dctcp
print(max(alls)) #0.5279045918135108
# step = 54
# CDF = []
# for i in range(step):
#     CDF.append(sum(j<0.01*i for j in alls)/len(alls))
#
# plt.xlabel("Kt绝对值")
# plt.ylabel("CDF")
# plt.title("dctcp")
# x_major_locator=MultipleLocator(0.04)
# #把x轴的刻度间隔设置为1，并存在变量里
# y_major_locator=MultipleLocator(0.1)
# #把y轴的刻度间隔设置为10，并存在变量里
# ax=plt.gca()
# #ax为两条坐标轴的实例
# ax.xaxis.set_major_locator(x_major_locator)
# #把x轴的主刻度设置为1的倍数
# ax.yaxis.set_major_locator(y_major_locator)
#
# plt.plot([0.01*i for i in range(step)],CDF)
# plt.show()



#pid
#print(max(alls)) #0.8655382730514988
step = 88
CDF = []
for i in range(step):
    CDF.append(sum(j<0.01*i for j in alls)/len(alls))

plt.xlabel("Kt绝对值")
plt.ylabel("CDF")
plt.title("PIDnn")
x_major_locator=MultipleLocator(0.08)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(0.1)
#把y轴的刻度间隔设置为10，并存在变量里
ax=plt.gca()
#ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)

plt.plot([0.01*i for i in range(step)],CDF)
plt.show()
