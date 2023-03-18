'''
用于处理ns3调用dip cc算法所获得的原始数据，根据节点数储存在同目录的dipcc文件夹下
'''

nodes = []
for i in range(20):
    nodes.append([])
filed = "../LINUX-NS3-SIMULATE/dipcc4.txt"
file = open(filed,"r")
line = file.readline()
while line:
    data = line.split(" ")
    if len(data)==5:
        print(data)
        _,noderaw,rttraw,rateraw,_ = data
        node = int(noderaw.split(":")[1])
        rtt = int(rttraw.split(":")[1])
        rate = float(rateraw.split(":")[1])
        nodes[node-2].append([rtt,rate])
    line = file.readline()
file.close()
for i in range(20):
    file = open("dipcc_test3/{}.txt".format(i+2),"w")
    for k in range(len(nodes[i])):
        rtt,rate = nodes[i][k]
        file.write("{} {}\n".format(rtt,rate))
    file.close()