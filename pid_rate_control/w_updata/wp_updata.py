import  matplotlib.pyplot as plt
import  torch

plt.rcParams["font.sans-serif"]=["SimHei"]
W = []
MAP = []

file = open("PID_WP0.5.txt")
line = file.readline()
W = []
rt = []
rtp = []
MAPE = []
rate = []
while line:

    nod,wp,rat,rtt,_,rttp,_ = line.split(" ")
    W.append(float(wp.split(":")[1]))
    rt.append(float(rtt.split("t")[-1]))
    rate.append(float(rat.split(":")[1]))
    rtp.append(float(rttp.split(":")[1])/1000)
    line = file.readline()

rt = sorted(rt)
print(rt[int(len(rt)/2)])
plt.plot(rt)
plt.show()
print(torch.mean(torch.tensor(rt)),torch.mean(torch.tensor(rate)))
