from  model.model import p_cell
import torch
p = p_cell()
x = torch.randn(2,5)
for i in x:
    print("eee:")
    print(p.forward(i))
    print("old:")
    print(p.old)