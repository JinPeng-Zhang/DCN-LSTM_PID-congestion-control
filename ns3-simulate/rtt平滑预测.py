import torch
from model.four import bp
from torch import nn,optim
import matplotlib.pyplot as plt
file = open("timely/0.txt")
line = file.readline()
model = torch.load("pt2/four.pt")
input = []
ouput = []
while line:
    i2,i1,i0,l = line.split(" ")
    input.append([float(i0),float(i1),float(i2)])
    ouput.append(float(l))
    line = file.readline()

loss_fn = nn.L1Loss()
optimizer = optim.Adam(model.parameters(),lr=2*1e-3)
los = []
pre = []
outs = []

for i in range(len(ouput)-2000):
    x = torch.tensor(input[i]).reshape((1, 3, 1))
    y = torch.tensor(ouput[i]).reshape((1, 1))
    out = model(x)
    loss = loss_fn(out, y)  # 计算每一个网络的损失值
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(float(loss))
    pre.append(float(abs((out - y)/(1+y))))
    outs.append(float(out))
    #print(pre[i])
# plt.plot(outs)
# plt.plot(ouput,color='green')
# print(torch.mean(torch.tensor(pre)))
# plt.show()
print(torch.mean(torch.tensor(pre)))
pre = []
for i in range(2000):
    i = i+len(ouput)-2000
    x = torch.tensor(input[i]).reshape((1, 3, 1))
    y = torch.tensor(ouput[i]).reshape((1, 1))
    out = model(x)
    outs.append(float(out))
    #print(float(abs((out - y)/y)))
    pre.append(float(abs((out - y)/(1+y))))
print(torch.mean(torch.tensor(pre)))
#torch.save(model, "pt2/four.pt")
plt.plot(outs)
plt.plot(ouput,color='green')
plt.show()