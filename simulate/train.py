
import numpy as np
from torch import nn,optim
import torch
import matplotlib.pyplot as plt
from  model.model import model_srn,seq_len,batch_size,input_size,num_layers,hidden_size
import  math
f= open("data0.txt")
line = f.readline() # 调用文件的 readline()方法
train_data = []
train = []
num = 1
output  = []
result = []
rate, rtt, pdrop,pipeline =np.around(np.array(line.split(),dtype = np.float64),decimals=2)
train_data.append([rate,rtt])
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
    train_data.append([rate/50,rtt])
    num = num + 1
    if num%3 == 1:
        output.append(pipeline/1000)
f.close()

input = torch.tensor(train).to(torch.float32)

output = np.array(output[0:len(input)]).reshape(len(input),1)
output = torch.tensor(output).to(torch.float32)
#预测模型SRN
# input:[rtt_old rate ] ,size :(seqLen = 3, batch_size = 5, input_size = 2)
#output:[pcongest],size:(batch_size = 5, input_size = 1)

srn = model_srn()
loss_fn = nn.MSELoss()
optimizer = optim.Adam(srn.parameters(),lr=2*1e-3)
los = []

h0 = torch.zeros(num_layers, batch_size, hidden_size)

print(len(input))
y1 = []
ll = 0
lls = []
diff = []
for step in range(len(input)):
    x = input[step]
    #x= torch.randn(seq_len, batch_size, input_size)
    out,hiddl = srn.forward(x,h0)  # 得到网络中的输出数据
    y = output[step]

    h0 = hiddl.detach()

    loss = loss_fn(out, y)  # 计算每一个网络的损失值
    print(out,y)
    diff.append(abs((out.detach().numpy()[0][0]-y.detach().numpy())/y.detach().numpy()))
    ll = ll+(loss-ll)/(step+1)
    lls.append(ll.detach().numpy())
    y1.append(out.detach().numpy()[0][0])
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(loss.detach().numpy())
#torch.save(srn, "1.pt")
plt.plot(diff)
plt.show()
