import  matplotlib.pyplot as plt
import  torch


rtt = []
rate = []
for i in range(19):
    file = open("{}.txt".format(i+2),"r")

    line = file.readline()

    while line:
        line = line.split(",")
        rtt.append(float(line[0].split("[")[1]))
        rate.append(float(line[1].split(" ")[1]))
        line = file.readline()


# print(torch.mean(torch.tensor(rtt))/1000,torch.mean(torch.tensor(rate)),max(rtt)/1000)
# rtt = sorted(rtt)
# print(rtt[int(len(rtt)*0.99)]/1000)

print(torch.sum(torch.tensor(rtt)*torch.tensor(rtt)*torch.tensor(rate))/(1000*torch.sum(torch.tensor(rtt)*torch.tensor(rate))))
print(torch.sum(torch.tensor(rate)*torch.tensor(rtt))/torch.sum(torch.tensor(rtt)))
print(max(rtt)/1000)
rtt = sorted(rtt)
print(rtt[int(len(rtt)*0.99)]/1000)