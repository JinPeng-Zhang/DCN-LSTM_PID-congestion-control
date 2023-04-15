'''
将训练好的时间序列预测模块部署到仿真平台，进行测试，统计预测准确度
'''
import matplotlib.pyplot as plt
MAPE = 0
le = 0
for node in range(20):
    file = open("LINUX-NS3-SIMULATE/rtt_pred2.txt")
    line = file.readline()
    rtt = []
    pred = []
    while line:
        _,nod,_,rt,rttp,_,_,_ = line.split(" ")
        nod = int(nod.split(":")[1])
        if nod == node:
            rtt.append(float(rt))
            pred.append(float(rttp.split(":")[1]))

        line = file.readline()


    for i in range(len(rtt)-1):
        MAPE = MAPE + abs((rtt[i+1]-pred[i])/rtt[i+1])
        #print(abs((rtt[i+1]-pred[i])/rtt[i+1]),rtt[i+1],pred[i])

    le  = le+len(rtt)-1
    plt.plot(rtt[1:],label="rtt",color = "green")
    plt.plot(pred[:-1],label="rttpred")
    plt.xlabel("times")
    plt.ylabel("RTT/us")
    plt.legend()
    plt.show()
    print(MAPE/le)
    file.close()
print(MAPE/le)