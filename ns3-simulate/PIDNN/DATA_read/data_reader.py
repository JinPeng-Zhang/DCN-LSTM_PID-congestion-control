import matplotlib.pyplot as plt
import  matplotlib
import torch
matplotlib.rcParams['axes.unicode_minus']=False
plt.rcParams["font.sans-serif"]=["SimHei"]
file = open("../../PAPER_DATA/PIDNN/rtt_5us_without_pred.txt")
#file = open("../../LINUX-NS3-SIMULATE/pidnn_data.txt")
line = file.readline()
nod = []
rate = []
rtt = []
# for i in range(160):
#     line = file.readline()
while line:
    node,_,rat,rt,_,_,_ = line.split(" ")
    # _,node,rt,_,_,rat = line.split(" ")
    #rt,_,rat = line.split((" "))
    #nod.append(float(node.split("]")[0]))
    # rate.append(float(rat.split("]")[0]))
    # rtt.append(float(rt.split("[")[-1].split(",")[0]))
    if float(node.split(":")[1])==2:
        nod.append(float(node.split(":")[1]))
        rate.append(float(rat.split(":")[1]))
        #rtt.append(float(rt.split(":")[-1]))
        rtt.append(float(rt.split("t")[-1]))
    line = file.readline()
file.close()

#print(torch.mean(torch.tensor(rtt))/1000,torch.mean(torch.tensor(rate)),max(rtt)/1000)
print(torch.mean(torch.tensor(rtt)),torch.mean(torch.tensor(rate)),max(rtt))
# rtt = sorted(rtt)
# print(rtt[int(len(rtt)*0.99)])

# print(torch.sum(torch.tensor(rtt)*torch.tensor(rtt)*torch.tensor(rate))/torch.sum(torch.tensor(rtt)*torch.tensor(rate)))
# print(torch.sum(torch.tensor(rate)*torch.tensor(rtt))/torch.sum(torch.tensor(rtt)))
print(torch.mean(torch.tensor(rtt)),torch.mean(torch.tensor(rate)))
print(max(rtt))
plt.plot(rate,color="green")
plt.xlabel("times")
plt.ylabel("rate/Gbps")
plt.title("node:2")
plt.show()
rtt = sorted(rtt)
print(rtt[int(len(rtt)*0.99)])
