
'''
用于处理timely算法的原始数据，default:node = 20

'''
oldrate = []
newrate = []
rtt = []
rttdiff = []
node = []
file = open("data2.txt","r")
line = file.readline()
node_num = 20
while line:
    _, nod, rt, rttdif, gradient,_,rateold, ratenew = line.split(" ")
    rtt.append(int(rt.split(":")[1]))
    rttdiff.append(int(rttdif.split(":")[1]))
    node.append(int(nod.split(":")[1]))
    oldrate.append(float(rateold.split(":")[1]))
    newrate.append(float(ratenew.split(":")[1]))
    line = file.readline()

for i in range(2,21):
    file = open("timely/{}.txt".format(i),"w")
    for t,rateo,raten,nod,diff in zip(rtt,oldrate,newrate,node,rttdiff):
        if nod == i :
            file.write(str([t,rateo,raten]))
            file.write("\n")
    file.close()

