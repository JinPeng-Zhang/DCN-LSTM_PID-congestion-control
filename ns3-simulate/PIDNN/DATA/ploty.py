import  matplotlib.pyplot as plt
import  torch
rtt = []
rate = []
for i in range(20):
    file = open("{}.txt".format(i+2),"r")
    line = file.readline()

    while line:
        line = line.split(" ")
        rtt.append(float(line[1]))
        rate.append(float(line[0]))
        line = file.readline()
print(torch.mean(torch.tensor(rtt)),torch.mean(torch.tensor(rate)))
