
from torch import  nn,optim
import torch
import  matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"]
import math
import numpy as np
import  random
#model = bp()
#input_size, hidden_size, num_layers, output_size, batch_size
#file = open("timely/0.txt","w")
def get_i_l(x):
    input = []
    output = (rttl[x+1]-rtts[x])/rtts[x]
    for i in range(3):
        input.append((rttl[x-i]-rtts[x-i])/rtts[x-i])
    return input,output
count = [0,0,0,0]
lt = []
for k in range(16):
    file1 = open("dctcp/20.txt".format(k+2))
    line = file1.readline()
    rttl = []
    while line:
        rtt,rateo,raten = line.split(",")
        rtt = float(rtt.split("[")[1])
        rttl.append(rtt)
        line = file1.readline()
    a = 0.8###平滑值对于模型预测十分重要，经测试0.8的处理效果最好
    rtts = []
    rttlable = []

    for i in range(len(rttl)):
        if i == 0:
            rtts.append(rttl[i])
        else:
            rtts.append((1-a)*rttl[i]+a*rtts[i-1])
    plt.plot(rttl,label="原始RTT")
    plt.plot(rtts,label="平滑RTT")
    plt.legend()
    plt.show()
    for i in range(len(rtts)-3):
        input,output = get_i_l(i+2)
        o = abs(output)

        x = torch.randn(1)
        if x >2:
            lt.append(output)
            print(x)
        if o >= 0 and o < 0.02:
            #if abs(torch.randn(1))<6000/20691:
                #file.write("{} {} {} {}\n".format(input[0], input[1], input[2], output))
                count[0] = count[0]+1
        elif o >= 0.02 and o < 0.08:
            #if abs(torch.randn(1))<3535/4649 :
                #file.write("{} {} {} {}\n".format(input[0], input[1], input[2], output))
                count[1] = count[1]+1
        elif o >= 0.08 and o < 0.15:
            #file.write("{} {} {} {}\n".format(input[0],input[1],input[2],output))
            count[2] = count[2]+1
        elif o >= 0.15 and o<1:
            #if abs(torch.randn(1))<1850/13341:
                #file.write("{} {} {} {}\n".format(input[0], input[1], input[2], output))
                count[3] = count[3]+1
    #########
print(count)
plt.xlabel("t")
plt.ylabel("Lt")
plt.plot(lt ,".")
plt.show()
print(len(lt),sum(count))
#file.close()
