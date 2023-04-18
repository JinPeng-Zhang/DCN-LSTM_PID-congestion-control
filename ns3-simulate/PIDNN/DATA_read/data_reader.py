import matplotlib.pyplot as plt
import  matplotlib
import torch
matplotlib.rcParams['axes.unicode_minus']=False
plt.rcParams["font.sans-serif"]=["SimHei"]
file = open("../../LINUX-NS3-SIMULATE/pid_rtt_pred7us.txt")
#file = open("../../LINUX-NS3-SIMULATE/pidnn_data.txt")
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

# print(torch.mean(torch.tensor(rtt)),torch.mean(torch.tensor(rate)),max(rtt))
# rtt = sorted(rtt)
# print(rtt[int(len(rtt)*0.99)])

print(torch.sum(torch.tensor(rtt)*torch.tensor(rtt)*torch.tensor(rate))/torch.sum(torch.tensor(rtt)*torch.tensor(rate)))
print(torch.sum(torch.tensor(rate)*torch.tensor(rtt))/torch.sum(torch.tensor(rtt)))
print(max(rtt))
rtt = sorted(rtt)
print(rtt[int(len(rtt)*0.99)])