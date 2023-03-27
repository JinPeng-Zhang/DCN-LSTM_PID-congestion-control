'''
训练PID神经网络，寻找合适的参数
输入input:(rttpre - rttnew);input_size = (1)
输出output:▲rate = −(𝑟𝑡𝑡_𝑛𝑒𝑤−𝑟𝑡𝑡𝑜𝑙𝑑)/𝑟𝑡𝑡𝑜𝑙𝑑;output_size = (1)
使用PID3的数据进行训练
'''


from model.pid_rate  import model_pid
import  torch
from torch import optim,nn
import  matplotlib.pyplot as plt

model = model_pid(3)
optimizer = optim.Adam(model.parameters(),lr=2e-3)
loss_fn = nn.MSELoss()

los = []
file = open("dataset/pid1/data.txt","r")
rtt = 0
for step in range(100000):
    line = file.readline()
    x,y = line.split(" ")
    x =torch.tensor(float(x)).reshape((1,1))
    y = torch.tensor(float(y))
    output = model(x)

    loss = loss_fn(output, y)  # 计算每一个网络的损失值
    optimizer.zero_grad()  # 在下一次求导之前将保留的grad清空
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 应用求导到优化器上去
    los.append(loss.detach().numpy())
    if step % 500 == 0:
        print("loss:{}".format(float(loss)))
        print(model.p.weight,model.i.weight,model.d.weight,model.bias)
yy = []
out = []
for i in range(100):
    line = file.readline()
    if not line:
        break
    x,y = line.split(" ")
    x =torch.tensor(float(x)).reshape((1,1))
    y = torch.tensor(float(y))
    output = model(x)
    yy.append(float(y))
    out.append(float(output[0]))

plt.plot(yy)
plt.plot(out,color="green")
plt.show()
