import torch
from torch import  nn

class models(nn.Module):
    def __init__(self):
        super(models, self).__init__()
        self.lstm = nn.LSTM(1, 16, 1, batch_first=True)
        #out ;(batch,seqlen,32)
        self.linear0 = nn.Linear(in_features=16, out_features=1)
    def forward(self,x):
        h_0 = torch.zeros((1, 1, 16))
        c_0 = torch.zeros((1, 1, 16))
        out,_= self.lstm(x,(h_0,c_0))
        return self.linear0(out[:,-1,:])
        #return self.linear2(self.drop(self.linear(out[:,-1,:])))

