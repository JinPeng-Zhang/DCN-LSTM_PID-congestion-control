from  model.model import model_cc,seq_len,input_size,num_layers,hidden_size
import torch
import time
cc = model_cc(100)
inputs1 = torch.randn(seq_len,5, input_size)
h0 = torch.zeros(num_layers, 5, hidden_size)
start = time.time()
num = 10000
for i in range(num):
    cc(inputs1,h0)
end = time.time()
print((end-start)/num)