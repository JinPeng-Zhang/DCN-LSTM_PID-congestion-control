import  matplotlib.pyplot as plt
import  torch
file = open("2.txt","r")
line = file.readline()
rtt = []
rate = []
while line:
    line = line.split(" ")
    if float(line[1])!=100:
        rtt.append(float(line[0]))
        rate.append(float(line[1]))
    line = file.readline()
print(torch.mean(torch.tensor(rate)))
plt.plot(rtt)
plt.plot(rate,color="green")
plt.show()
#22752.6660