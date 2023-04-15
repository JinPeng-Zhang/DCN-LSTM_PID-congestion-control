import matplotlib.pyplot as plt
import  matplotlib
import torch
matplotlib.rcParams['axes.unicode_minus']=False
plt.rcParams["font.sans-serif"]=["SimHei"]
file = open("../../LINUX-NS3-SIMULATE/pid_rtt6us.txt")

line = file.readline()
nod = []
rate = []
rtt = []
while line:
    node,_,_,_,rat,rt,_,_ = line.split(" ")
    nod.append(float(node.split(":")[1]))
    rate.append(float(rat.split(":")[1]))
    rtt.append(float(rt.split("t")[-1]))
    line = file.readline()
file.close()
print(torch.mean(torch.tensor(rtt)),torch.mean(torch.tensor(rate)))