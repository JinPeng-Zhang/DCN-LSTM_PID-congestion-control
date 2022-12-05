import torch
from torch import nn
from torch import tensor
import numpy as np
from torch import optim
import torch.nn.functional as F

batch_size = 5     # 批量大小
seq_len = 3        # 序列长度
input_size = 2     # 特征维度
hidden_size = 1    #隐藏层神经元个数 or 输出yi特征维度
num_layers = 2 #隐藏层层数
#RSN
# nonlinearity：激活函数，默认为 tanh
# bias：是否使用偏置，默认为True
# input 的维度为 (seqLen, batch_size, input_size)，
#初始化隐藏变量h0的维度是 (num_layers, batch_size, hidden_size)；
#out 的维度为 (seqlen, batch, hidden_size)
#
class model_srn(nn.Module):
    def __init__(self):
        super(model_srn, self).__init__()
        self.cell = torch.nn.RNN(input_size, hidden_size, num_layers=num_layers, bias=True)
        self.linear = nn.Linear(in_features=3, out_features=1)
    def forward(self,x,h0):
        out, hidden = self.cell(x, h0)
        out = torch.reshape(out, (3, -1))
        out = out.T
        out = self.linear(out)
        print(out.shape)
        out = torch.tanh(out)
        return out,hidden
class model_pid(nn.Module):
    def __init__(self,lens):
        super(model_pid, self).__init__()
        self.p = p_cell()
        self.i = i_cell(lens)
        self.d = d_cell()
        self.bias = nn.Parameter(torch.randn(batch_size, hidden_size))
        self.linear = nn.Linear(in_features=3, out_features=1)
    def forward(self,x):
        outp = torch.as_tensor(self.p.forward(x))
        outi,clear = self.i.forward(x)
        outi = torch.as_tensor(outi)
        outd=  torch.as_tensor(self.d.forward(x))
        out = torch.cat([outp,outi,outd],1)
        #out = self .linear(out)
        return torch.sum(out,axis=1,keepdim=True)+self.bias,clear
class model_cc(nn.Module):
    def __init__(self,lens):
        super(model_cc, self).__init__()
        self.rsn = model_srn()
        self.dip = model_pid(lens)
    def forward(self,x,h0):
        out,hidden = self.rsn.forward(x,h0)
        return self.dip.forward(out),hidden
class p_cell(nn.Module):
    def __init__(self):
        super(p_cell,self).__init__()
        self.weight = nn.Parameter(torch.randn(1,1))
    def forward(self,inputs):
        return self.weight*inputs
class i_cell(nn.Module):
    def __init__(self,lens):
        super(i_cell,self).__init__()
        self.weight = nn.Parameter(torch.randn(1,1))
        self.sum = torch.zeros(batch_size,hidden_size)
        self.len = 0
        self.lens = lens
    def forward(self, inputs):
        self.len = self.len+1
        if self.len>self.lens:
            self.len = 0
            self.sum = torch.zeros(batch_size,hidden_size)
        out = self.weight * (inputs + self.sum)
        self.sum = self.sum+inputs
        return out,not self.len
class d_cell(nn.Module):
    def __init__(self):
        super(d_cell,self).__init__()
        self.weight = nn.Parameter(torch.randn(1,1))
        self.old = 0
    def forward(self, inputs):
        out = self.weight * (inputs-self.old)
        self.old = inputs
        return out
# model = model_srn()
# #优化器
# print(model)
# optimizer = optim.Adam(model.parameters(),lr=1e-3)
#
# for name, param in model.named_parameters(): #查看可优化的参数有哪些
#   if param.requires_grad:
#     print(name)
#
# #损失函数
# loss_fn = nn.MSELoss()
# #数据集，save
# inputs1 = torch.randn(seq_len, batch_size, input_size)
# inputs2 = torch.randn(seq_len, batch_size, input_size)
# h0 = torch.zeros(num_layers, batch_size, hidden_size)
# out,hidden = model.forward(inputs1,h0)
# out,hidden = model.forward(inputs2,h0)
# #out 的维度为 (batch)
# print("Output size:", out.shape)
# print("Output:", out)
# print("Hidden size:",hidden.shape)
# print("Hidden:",hidden)
#训练流程