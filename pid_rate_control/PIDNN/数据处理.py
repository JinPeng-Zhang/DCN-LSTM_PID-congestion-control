


file = open("D:\\Graduation-Design\\ns3-simulate\\LINUX-NS3-SIMULATE\\pidnn.txt")
line = file.readline()

rtt = []
node = []
rate = []
while line:
    rttold = rtt
    nod,_,_,_,rat,rt,_ = line.split(" ")
    node.append(int(nod.split(":")[1]))
    rate.append(float(rat.split(":")[1]))
    rtt.append(float(rt.split("t")[2]))
    line = file.readline()
file.close()
for i in range(20):
    file = open("target_5us/{}.txt".format(i+2),"w")
    for nod,rt,rat in zip(node,rtt,rate):
        print(nod)
        if (i+2) == nod:
            file.write("{} {}\n".format(rt,rat))
    file.close()
