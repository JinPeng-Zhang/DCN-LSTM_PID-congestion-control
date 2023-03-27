'''
经过pid_test.py验证，dip_rate.py中的model_pid神经网络，经过训练能够模拟出pid算法
因此希望通过ns数据集的训练,为model_pid寻找合适的参数
'''


'''
数据集预处理，有了预测模块的过拟合经验，因此此次数据集也使用相同的采样方法进行预处理
处理由TIMELY算法导出的raw数据
模型修改i_cell VERSION1 to VERSION2,将累计清零求和模块改成滑动求和，降低了模型复杂程度同时更适应仿真环境
'''
send_num = 0
recv_num = 0
rate_num = 0
rtt = []
oldrate = []
newrate = []
node = []

datafile = "D:\\Graduation-Design\\ns3-simulate\\LINUX-NS3-SIMULATE\\timely-rateinit1.txt"
# python run.py --cc hpcc --trace flow --bw 100 --topo topology --hpai 50 >> hpcc_pid1.txt

file = open(datafile,"r")
line = file.readline()
node_num = 20
while line:
    data = line.split(" ")

    if len(data) == 8:
        _,nod,rt,_,_,_,rateold,ratenew = data
        rtt.append(float(rt.split(":")[1]))
        oldrate.append(float(rateold.split(":")[1]))
        newrate.append(float(ratenew.split(",")[0].split(":")[1]))
        node.append(float(nod.split(":")[1]))
    line = file.readline()

for i in range(2,21):
    file = open("dataset/pid3/{}.txt".format(i),"w")
    for t,rateo,raten,nod in zip(rtt,oldrate,newrate,node):
        if nod == i :
            file.write("{} {} {}".format(t,rateo,raten))
            file.write("\n")
    file.close()
print(rtt)



