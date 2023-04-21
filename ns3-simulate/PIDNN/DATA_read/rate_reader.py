import  torch
file = open("../../PAPER_DATA/PIDNN/fct_target6us.txt")

line = file.readline()
siz = []
fcts = []
while line:
    _,_,_,_,size,_,fct,_ = line.split(" ")
    siz.append(float(size))
    fcts.append(float(fct))
    line = file.readline()
print(siz)
print(8*torch.sum(torch.tensor(siz))/torch.sum(torch.tensor(fcts)))
print(torch.mean(torch.tensor(fcts)))
print(sum(torch.tensor(siz)))
print(sum(torch.tensor(fcts)))

