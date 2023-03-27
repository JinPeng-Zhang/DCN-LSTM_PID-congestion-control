import  matplotlib.pyplot as plt
import  torch
file = open("2.txt","r")
line = file.readline()
rtt = []
rate = []
while line:
    line = line.split(",")
    rtt.append(float(line[0].split("[")[1]))
    rate.append(float(line[1].split(" ")[1]))
    line = file.readline()
print(torch.mean(torch.tensor(rtt)))
#plt.plot(rtt)
plt.plot(rate)
plt.show()