import matplotlib.pyplot as plt
import  torch
rtt = []
rate = []
file = open("pid2/2.txt","r")
line = file.readline()
while line:
    rt,rateo,raten = line.split(" ")
    rtt.append(float(rt))
    rate.append(float(rateo))
    line = file.readline()
print(torch.mean(torch.tensor(rtt)))
plt.plot(rtt)
plt.show()