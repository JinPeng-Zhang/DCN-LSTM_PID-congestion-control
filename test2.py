#############
##这个代码主要是验证PID神经网络搭建的是否正确
############
from  model.model import model_dip
import torch
from torch import nn
p = model_dip(10)
from torch import optim

optimizer = optim.Adam(p.parameters(),lr=1e-3)
loss_fn = nn.MSELoss()
EPOCH = 5
y = torch.zeros(1,5)

for epoch in range(EPOCH):
    for step in range(5000):
        flag = 0
        x = torch.randn(1,5)

        output,clear = p.forward(x)  # 得到网络中的输出数据
        if clear:
            y = torch.zeros(1,5)
            flag = 1

        y = y+2*x
        if flag:
            print("========================================")
            print(output,y,x)
        loss = loss_fn(output, y)  # 计算每一个网络的损失值
        optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
        loss.backward()  # 反向传播，计算梯度
        optimizer.step()  # 应用求导到优化器上去

        if step % 500 == 0:#表示已经进行了50的倍数了
            # test_x = torch.randn(1,5)
            # test_y = 5*test_x
            # test_output = p.forward(test_x)
            #
            # print("out,y,x:")
            # print(test_output,test_y,test_x)
            print("wei,bias,h")
            print(p.weight,p.bias)
            #print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)
