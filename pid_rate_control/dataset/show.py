'''
PID1 是使用HPCC跑出来的数据
PID2 是使用PIDCC跑出来的数据
PID3 时使用TIMELY算法跑出来的数据
PID2 PID设置的条件一致
'''

import matplotlib.pyplot as plt
import  torch
rtt = []
rate = []
file = open("pid2/2.txt","r")
line = file.readline()
while line:
    rt,rateo,raten = line.split(" ")
    rtt.append(float(rt))
    rate.append(float(rateo))
    line = file.readline()
print(torch.mean(torch.tensor(rtt)))
plt.plot(rtt)
plt.show()