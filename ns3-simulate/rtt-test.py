
from torch import  nn,optim
import torch
import  matplotlib.pyplot as plt
import math
import numpy as np

model = torch.load("pt/dctcp-srn.pt")
#input_size, hidden_size, num_layers, output_size, batch_size
for k in range(3):

    file = open("dctcp/{}.txt".format(k+16))
    line = file.readline()
    rated = []
    rate = []
    rttl = []
    while line:
        rtt, rateo, raten = line.split(",")
        rtt = float(rtt.split("[")[1])
        rateo = float(rateo)
        raten = float(raten.split("]")[0])
        rttl.append(rtt)
        rated.append((raten - rateo))
        rate.append(raten)
        # print(rtt,rateo,raten)
        line = file.readline()
    rttl = torch.tensor(rttl) / max(rttl)

    def ava_filter(x, filt_length):
        N = len(x)
        res = []
        for i in range(N):
            if i <= filt_length // 2 or i >= N - (filt_length // 2):
                temp = x[i]
            else:
                sum = 0
                for j in range(filt_length):
                    sum += x[i - filt_length // 2 + j]
                temp = sum * 1.0 / filt_length
            res.append(temp)
        return res


    # rttl = ava_filter(rttl,3)
    # rated = ava_filter(rated,3)


    input = []
    output = []
    #output = rttl
    for i in range(len(rttl)):
        input.append(rttl[i])
        output.append(rttl[i])
        # input.append(rttl[i])
    ff= []
    outs = []
    seqlen = 10
    for i in range(len(input)-seqlen-2):
        x = torch.tensor(input[i:i + seqlen]).reshape((1, seqlen, 1))
        # print(x)
        # x = torch.randn((1,3,2))
        # x= torch.randn(seq_len, batch_size, input_size)
        out = model.forward(x)  # 得到网络中的输出数据
        y = torch.tensor(output[i + seqlen]).reshape((1, 1))

        outs.append(float(out))
        #print(y,out,i)
        ff.append(float(abs(out-rttl[i+seqlen])/rttl[i+seqlen]))
    print(torch.mean(torch.tensor(ff)))
    plt.plot(rttl[seqlen:len(input)-2],color='green')
    plt.plot(outs)
    plt.show()

