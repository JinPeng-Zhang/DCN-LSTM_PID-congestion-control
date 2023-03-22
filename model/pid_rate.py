from torch import  nn
import torch
batch_size = 1
hidden_size = 1
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
        return out,not self.len#clear,积分一定长度len，避免长时间累积影响
class d_cell(nn.Module):
    def __init__(self):
        super(d_cell,self).__init__()
        self.weight = nn.Parameter(torch.randn(1,1))
        self.old = 0
    def forward(self, inputs):
        out = self.weight * (inputs-self.old)
        self.old = inputs
        return out