
import numpy as np
from torch import nn,optim
import torch
import matplotlib.pyplot as plt
from  model.model import model_srn,seq_len,batch_size,input_size,num_layers,hidden_size

srn = torch.load("trained_model/1.pt")

h0 = torch.tensor([0.6248,0.0100])
h0 = torch.reshape(h0,[num_layers, batch_size, hidden_size])
f= open("data/data1.txt")
line = f.readline() # 调用文件的 readline()方法
train_data = []
train = []
num = 1
output  = []
result = []
rate, rtt, pdrop,pipeline =np.around(np.array(line.split(),dtype = np.float64),decimals=2)
train_data.append([rate/50,rtt/1000])
grmma = 0.2

while line:
    #print(line, end = '') # 在 Python 3中使用
    #四舍五入，保留两位小数
    #print(rate,rtt)
    if num == 3:
        train.append(np.array(train_data).reshape((seq_len,batch_size,input_size),order='F'))

        #print(train[len(train)-1])
        train_data = []
        num = 0
    line = f.readline()
    if not line:
        break
    rate, rtt, pdrop,pipeline =np.around(np.array(line.split(),dtype = np.float64),decimals=2)
    train_data.append([rate/50,rtt/1000])
    num = num + 1
    if num%3 == 1:
        output.append(pipeline/800)
f.close()

input = torch.tensor(train).to(torch.float32)

output = np.array(output[0:len(input)]).reshape(len(input),1)
output = torch.tensor(output).to(torch.float32)

p1 = []
p2 = []
for step in range(len(input)):
    x = input[step]
    #x= torch.randn(seq_len, batch_size, input_size)
    out,hiddl = srn.forward(x,h0)  # 得到网络中的输出数据
    y = output[step]
    p1.append(y.detach().numpy())
    p2.append(out.detach().numpy()[0][0]-y.detach().numpy())

plt.plot(p2)
plt.show()