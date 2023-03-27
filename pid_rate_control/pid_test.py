'''
即D:\Graduation-Design\test.pyD:\Graduation-Design\test.py后再一次测试pid速率调节模块
此时由于神经网络预测模块已经实现，因此pid模块的输入输出规模由此可以确定

输出PID RATE = P(input)+i(input)+D(input)
P(input) = Kp*(input)
I(input) = Ki∫1->3(input) = Ki(input_0 + input_1+input_2)即前三个时间点INPUT输入累计
D(input) = Kd(input') = Kd(input_0 - input_1)

'''
'''
test1 ，input x0 output 2x0

from model.dip_rate import p_cell
import  torch
from torch import optim,nn
import  matplotlib.pyplot as plt

model = p_cell()
optimizer = optim.Adam(model.parameters(),lr=2e-3)
loss_fn = nn.MSELoss()

los = []
y = torch.zeros(1,1)
x = torch.zeros((1,1))
for step in range(10000):
    flag = 0
    x = torch.randn(1,1)

    output = model.forward(x)  # 得到网络中的输出数据

    y = 2*x
    #print(output,y,x)
    loss = loss_fn(output, y)  # 计算每一个网络的损失值
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(loss.detach().numpy())
    if step % 500 == 0:
        print("param:")
        print(model.weight)
print(model.weight)
plt.plot(los)
plt.show()

'''



'''
#test2 ，input x0 output 3*(x0+x1+x2)

from model.pid_rate  import i_cell
import  torch
from torch import optim,nn
import  matplotlib.pyplot as plt

model = i_cell(3)
optimizer = optim.Adam(model.parameters(),lr=2e-3)
loss_fn = nn.MSELoss()

los = []
y = torch.zeros(1,1)
x = torch.zeros((1,1))
x1 = torch.zeros((1,1))
x2 = torch.zeros((1,1))
for step in range(10000):
    x2 = x1
    x1 = x
    x = torch.randn(1,1)
    output = model.forward(x)  # 得到网络中的输出数据
    y = 2*(x+x1+x2)
    #print(output,y,x,x1,x2)
    loss = loss_fn(output, y)  # 计算每一个网络的损失值
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(loss.detach().numpy())
    if step % 500 == 0:
        print("param:")
        print(model.weight)
print(model.weight)
plt.plot(los)
plt.show()


'''
'''
#test3 ，input x0 output 4(x0-x1)

from model.dip_rate import d_cell
import  torch
from torch import optim,nn
import  matplotlib.pyplot as plt

model = d_cell()
optimizer = optim.Adam(model.parameters(),lr=2e-3)
loss_fn = nn.MSELoss()

los = []
y = torch.zeros(1,1)
x = torch.zeros((1,1))

for step in range(10000):
    xold = x
    x = torch.randn(1,1)

    output = model.forward(x)  # 得到网络中的输出数据

    y = 4*(x-xold)
    print(output,y,x,xold)
    loss = loss_fn(output, y)  # 计算每一个网络的损失值
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(loss.detach().numpy())
    if step % 500 == 0:
        print("param:")
        print(model.weight)
print(model.weight)
plt.plot(los)
plt.show()
'''


#test4 ，input x0 output test1+test2+test3

from model.pid_rate import model_pid
import  torch
from torch import optim,nn
import  matplotlib.pyplot as plt

model = model_pid(3)
optimizer = optim.Adam(model.parameters(),lr=2e-3)
loss_fn = nn.MSELoss()

los = []
y3 = torch.zeros(1,1)
x = torch.zeros((1,1))
for step in range(10000):
    flag = 0
    xold = x
    x = torch.randn(1,1)

    output,clear = model.forward(x)  # 得到网络中的输出数据

    y1 = 2*x
    y2 = 4*(x-xold)
    if clear:
        y3 = torch.zeros((1,1))
    y3 = y3+3*x
    y = y1+y2+y3
    #print(output,y,x)
    loss = loss_fn(output, y)  # 计算每一个网络的损失值
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(loss.detach().numpy())
    if step % 500 == 0:
        print("param:2,3,4")
        print(model.p.weight,model.i.weight,model.d.weight)
print(model.p.weight,model.i.weight,model.d.weight)
plt.plot(los)
plt.show()



