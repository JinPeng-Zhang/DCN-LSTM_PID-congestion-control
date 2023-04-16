import  matplotlib.pyplot as plt
import  torch
rtt = []
rate = []

file = open("10.txt","r")
line = file.readline()

while line:
    line = line.split(" ")
    rtt.append(float(line[1]))
    rate.append(float(line[0]))
    line = file.readline()
print(torch.mean(torch.tensor(rtt)),torch.mean(torch.tensor(rate)))
plt.plot([i+500 for i in range(500)],rate[500:1000],color = "green")
plt.xlabel("times")
plt.ylabel("rate/Gbps")
plt.show()
