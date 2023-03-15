import  torch
from torch import  nn
import matplotlib.pyplot as plt
model = torch.load("pt/timely-1.pt")
#model = Seq2Seq(2,12,3,1,1)





file = open("hpcc/9.txt")
line = file.readline()
rated = []
rttl = []
while line:
    rtt,rateo,raten = line.split(",")
    rtt = float(rtt.split("[")[1])/1000000
    rateo = float(rateo)
    raten = float(raten.split("]")[0])
    rttl.append(rtt)
    rated.append((raten-rateo)/rateo)
    #print(rtt,rateo,raten)
    line = file.readline()
rttll = rttl
input = []
output = rttl
for i in range(len(rttl)):
     input.append([rttl[i],rated[i]])
diff= []
outs = []
for i in range(int(len(input) / 2) - 13):
    x = torch.tensor(input[i:i + 10]).reshape((1, 10, 2))
    # print(x)
    # x = torch.randn((1,3,2))
    # x= torch.randn(seq_len, batch_size, input_size)
    out = model.forward(x, torch.tensor((output[i + 10])).reshape((1, 1, 1)))  # 得到网络中的输出数据
    outs.append(float(out))
    y = torch.tensor((output[i + 11])).reshape((1, 1, 1))
    diff.append(float(abs(out - rttl[i + 11]) / rttl[i + 11]))
    print(float(abs(out - rttl[i + 11]) / rttl[i + 11]))
    # torch.save(model, "pt/timely-1.pt")
print(torch.mean(torch.tensor(diff)))
plt.plot(rttl[11:int(len(input)/2)-2])
#plt.plot(outs)
plt.show()

