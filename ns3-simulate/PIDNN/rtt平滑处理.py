'''
原始处理后的文件保存在Graduation-Design\pid_rate_control\PIDNN\target_5us处
'''
from torch import  nn,optim
import torch
import  matplotlib.pyplot as plt
import math
import numpy as np

#model = bp()
#input_size, hidden_size, num_layers, output_size, batch_size
file = open("target5us.txt","w")
def get_i_l(x):
    input = []
    output = (rttl[x+1]-rtts[x])/rtts[x]
    for i in range(3):
        input.append((rttl[x-i]-rtts[x-i])/rtts[x-i])
    return input,output
count = [0,0,0,0]
for k in range(16):
    file1 = open("../../pid_rate_control/PIDNN/target_5us/{}.txt".format(k+2))
    line = file1.readline()
    rttl = []
    while line:
        rtt,_ = line.split(" ")
        rtt = float(rtt)
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
    for i in range(len(rtts)-3):
        input,output = get_i_l(i+2)
        o = abs(output)
        if o >= 0 and o < 0.02:
            #if abs(torch.randn(1))<6000/20691:
                file.write("{} {} {} {}\n".format(input[0], input[1], input[2], output))
                count[0] = count[0]+1
        elif o >= 0.02 and o < 0.08:
            if abs(torch.randn(1))<3035/4649 :
                file.write("{} {} {} {}\n".format(input[0], input[1], input[2], output))
                count[1] = count[1]+1
        elif o >= 0.08 and o < 0.15:
            if abs(torch.randn(1)) < 2135 / 4649:
                file.write("{} {} {} {}\n".format(input[0],input[1],input[2],output))
                count[2] = count[2]+1
        elif o >= 0.15 and o<1:
            if abs(torch.randn(1))<2800/13341:
                file.write("{} {} {} {}\n".format(input[0], input[1], input[2], output))
                count[3] = count[3]+1
    #########
print(count)
file.close()
