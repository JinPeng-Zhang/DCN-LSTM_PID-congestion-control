'''
经过dip_test.py验证，dip_rate.py中的model_pid神经网络，经过训练能够模拟出dip算法
因此希望通过ns数据集的训练,为model_pid寻找合适的参数
'''


'''
数据集预处理，有了预测模块的过拟合经验，因此此次数据集也使用相同的采样方法进行预处理
模型修改i_cell VERSION1 to VERSION2,将累计清零求和模块改成滑动求和，降低了模型复杂程度同时更适应仿真环境
'''
send_num = 0
recv_num = 0
rate_num = 0
send_time = []
recv_time = []
oldrate = []
newrate = []
node = []

datafile = "D:\\Graduation-Design\\ns3-simulate\\LINUX-NS3-SIMULATE\\hpcc_pid1.txt"
# python run.py --cc hpcc --trace flow --bw 100 --topo topology --hpai 50 >> hpcc_pid1.txt
                                                                                                                                                                                                                                                   
file = open(datafile,"r")
line = file.readline()
node_num = 20
while line:
    data = line.split(" ")
    for i in data:
        if len(i.split("--"))>1:
            send_time.append(int(i.split("--")[1]))
            send_num = send_num + 1
        elif len(i.split(":"))>1:
            if rate_num%2 == 0:
                oldrate.append(float(i.split(":")[1]))
            else:
                newrate.append(float(i.split(":")[1]))
            rate_num = rate_num + 1
        else:
            print(i)
            recv_time.append(int(i.split("=node")[1]))
            node.append(int(i.split("=node")[0]))
            recv_num = recv_num + 1
    print(send_num,recv_num,rate_num)
    line = file.readline()
rtt = list(map(lambda x: x[0]-x[1], zip(recv_time, send_time)))
for i in range(2,21):
    file = open("dataset/pid1/{}.txt".format(i),"w")
    for t,rateo,raten,nod in zip(rtt,oldrate,newrate,node):
        if nod == i :
            file.write("{} {} {}".format(t,rateo,raten))
            file.write("\n")
    file.close()
print(rtt)



