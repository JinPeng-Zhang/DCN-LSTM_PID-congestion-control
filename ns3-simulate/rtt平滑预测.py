import torch
from model.rtt_pred import models
from torch import nn,optim
import random
import matplotlib.pyplot as plt
file = open("PIDNN/0.txt")
line = file.readline()
#model = torch.load("PIDNN/pid_5us.pt")
model = models()
input = []
ouput = []
while line:
    i2,i1,i0,l = line.split(" ")
    input.append([float(i0),float(i1),float(i2)])
    ouput.append(float(l))
    line = file.readline()

loss_fn = nn.L1Loss()
optimizer = optim.Adam(model.parameters(),lr=1*1e-3)
print((len(input)))

los1 = []
los2 = []
for epcoh in range(19):
    #

    outs = []
    pre = []
    for i in range(800):
        index = random.randint(0,len(input)-1)
        x = torch.tensor(input[index]).reshape((1, 3, 1))
        y = torch.tensor(ouput[index]).reshape((1, 1))
        out = model(x)
        loss = loss_fn(out, y)  # 计算每一个网络的损失值
        optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
        loss.backward()  # 反向传播，计算梯度
        optimizer.step()  # 应用求导到优化器上去
        if len(los1)!=0:
            los1.append((float(loss)+len(los1)*los1[-1])/(len(los1)+1))
        else:
            los1.append(float(loss))
        pre.append(float(abs((out - y)/(1+y))))
        outs.append(float(out))
        input.pop(index)
        ouput.pop(index)
    print(epcoh)
    print(torch.mean(torch.tensor(pre)))
    pre = []

    for i in range(200):
        index = random.randint(0, len(input)-1)
        x = torch.tensor(input[index]).reshape((1, 3, 1))
        y = torch.tensor(ouput[index]).reshape((1, 1))
        out = model(x)
        loss = loss_fn(out, y)
        # if len(los1) != 0:
        #     los1.append((float(loss) + len(los1) * los1[-1]) / (len(los1) + 1))
        # else:
        #     los1.append(float(loss))
        outs.append(float(out))
        pre.append(float(abs((out - y)/(1+y))))
        input.pop(index)
        ouput.pop(index)
        #print(out.tolist(),y.tolist(),pre[-1])
    print(torch.mean(torch.tensor(pre)))
#torch.save(model, "PIDNN/pid_5us.pt")
plt.xlabel("times")
plt.ylabel("loss")
# plt.title("19epoch-train")
plt.plot(los1)
plt.show()

# plt.xlabel("times")
# plt.ylabel("loss")
# plt.title("19epoch-test")
# plt.plot(los2)
# plt.show()