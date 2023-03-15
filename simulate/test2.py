#############
##这个代码主要是验证PID神经网络搭建的是否正确
############
from  model.model import model_pid,seq_len,batch_size,input_size
import torch
import time
from torch import nn
pid = model_pid(1000)
from torch import optim
import matplotlib.pyplot as plt
optimizer = optim.Adam(pid.parameters(),lr=2*1e-3)
loss_fn = nn.MSELoss()
EPOCH = 1
yp = torch.zeros(batch_size,1)
yi = torch.zeros(5,1)
yd = torch.zeros(5,1)
xold = torch.zeros(5,1)
los = []
start = time.time()
for epoch in range(EPOCH):
    for step in range(5000):
        x = torch.randn(5,1)
        yp = 5*x
        output, clear = pid.forward(x)  # 得到网络中的输出数据
        if clear:
            yi = torch.zeros(5, 1)

        yi = yi + 2 * x
        yd = 3*(x-xold)
        xold = x
        y = yp+yi+yd+torch.randn(5,1)


        loss = loss_fn(output, y)  # 计算每一个网络的损失值
        optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
        loss.backward()  # 反向传播，计算梯度
        optimizer.step()  # 应用求导到优化器上去
        los.append(loss.detach().numpy())
        if step % 500 == 0:#表示已经进行了50的倍数了
            # test_x = torch.randn(1,5)
            # test_y = 5*test_x
            # test_output = p.forward(test_x)
            #
            # print("out,y,x:")
            # print(test_output,test_y,test_x)
            print("P:wei,I:wei,D:wei,pid,bias")
            print(pid.p.weight,pid.i.weight,pid.d.weight,pid.bias)
            #print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)
end = time.time()
print("time:")
print(end-start)
plt.plot(los)
plt.show()
