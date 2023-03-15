from model.model import model_srnn
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch import  nn
srn= torch.load("6.pt")



optimizer = torch.optim.Adam(srn.parameters(), lr=0.002)
loss_func = torch.nn.MSELoss()

h_state = None


f= open("data_random5.txt")
line = f.readline()
train_data =[]
output = []
rate, rtt, pdrop,pipeline,_ =np.around(np.array(line.split(),dtype = np.float64),decimals=2)
train_data.append([rate/50,rtt/1000])
output.append(pipeline/1000)
while line:
    line = f.readline()
    if not line:
        break
    rate, rtt, pdrop,pipeline,_ =np.around(np.array(line.split(),dtype = np.float64),decimals=2)
    train_data.append([rate/50,rtt/1000])
    output.append(pipeline/1000)
f.close()


train_data = torch.tensor(train_data).reshape((-1,3,2))
output =  torch.tensor(output).reshape((-1,3))
los =[]
h_state = torch.tensor([[[ 0.4034]],[[-0.5696]]])
for step in range(len(output)):
    x = train_data[step].reshape((1,3,2)).to(torch.float32)
    y = torch.tensor(output[step]).reshape((1,3,1)).to(torch.float32)

    prediction, h_state = srn(x, h_state)
    # 每一组input，都对应了一个h_state和一个prediction

    h_state = h_state.data
    # 将对应的h_state向后传
    print(prediction,y)
    loss = loss_func(prediction, y)
    los.append(loss.detach().numpy())
    optimizer.zero_grad()
    # 清空上一步的参与更新参数值

    loss.backward(retain_graph=True)
    # 误差反向传播，计算参数更新值

    optimizer.step()
    # 将参数更新值施加到rnn的parameters上
torch.save(srn, "7.pt")
print(h_state)
plt.plot(los)
plt.show()
