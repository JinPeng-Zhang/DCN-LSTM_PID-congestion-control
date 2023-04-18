import  torch
file = open("../../LINUX-NS3-SIMULATE/fct_pid5.txt")

line = file.readline()
siz = []
fcts = []
while line:
    _,_,_,_,size,_,fct,_ = line.split(" ")
    siz.append(float(size)/1000000)
    fcts.append(float(fct))
    line = file.readline()
print(siz)
print(torch.sum(torch.tensor(siz)*torch.tensor(fcts))/torch.sum(torch.tensor(siz)))
print(torch.mean(torch.tensor(fcts)))
print(sum(torch.tensor(siz)))
print(sum(torch.tensor(fcts)))

