import  matplotlib.pyplot as plt
import  math
import torch
file = open("2.txt","r")
line = file.readline()
rtt = []
rate = []
while line:
    line = line.split(",")
    rtt.append(float(line[0].split("[")[1]))
    # if rtt[len(rtt)-1]>10000:
    #     rtt.pop()
    rate.append(float(line[1].split(" ")[1]))
    line = file.readline()
print(torch.mean(torch.tensor(rate)))
#plt.plot(rtt)
plt.plot(rate,color="green")
plt.show()