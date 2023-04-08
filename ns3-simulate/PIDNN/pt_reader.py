'''
此py创建为了读取训练好的pt文件,获取权重后使用c++复现神经网络
'''
import torch

x = torch.load("pid_5us.pt")

wi = x.lstm.weight_ih_l0
wh = x.lstm.weight_hh_l0
bi = x.lstm.bias_ih_l0
bh = x.lstm.bias_hh_l0
linearw = x.linear0.weight
linearb = x.linear0.bias


h_0 = torch.zeros((1, 1, 16))
c_0 = torch.zeros((1, 1, 16))
x1 = torch.tensor([1.]).reshape((1, 1, 1))

it = torch.sigmoid((wi[0:16]*x1).reshape((16,1))+bi[0:16].reshape((16,1))+torch.mm(wh[0:16],h_0[0].T)+bh[0:16].reshape((16,1)))
fi = torch.sigmoid((wi[16:32]*x1).reshape((16,1))+bi[16:32].reshape((16,1))+torch.mm(wh[16:32],h_0[0].T)+bh[16:32].reshape((16,1)))
gt = torch.tanh((wi[32:48]*x1).reshape((16,1))+bi[32:48].reshape((16,1))+torch.mm(wh[32:48],h_0[0].T)+bh[32:48].reshape((16,1)))
ot = torch.sigmoid((wi[48:64]*x1).reshape((16,1))+bi[48:64].reshape((16,1))+torch.mm(wh[48:64],h_0[0].T)+bh[48:64].reshape((16,1)))
ct = fi*c_0.reshape((16,1))+it*gt
ht = ot*torch.tanh(ct)

print(ct,ht)
print(x.lstm(x1,(h_0,c_0)))