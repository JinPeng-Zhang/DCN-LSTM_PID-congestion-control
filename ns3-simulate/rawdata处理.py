'''
用于处理hpcc,dctcp算法的原始数据，default:node = 20

'''



send_num = 0
recv_num = 0
rate_num = 0
send_time = []
recv_time = []
oldrate = []
newrate = []
node = []
file = open("dctcp2.txt","r")
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
            #print(i)
            recv_time.append(int(i.split("=node")[1]))
            node.append(int(i.split("=node")[0]))
            recv_num = recv_num + 1
    print(send_num,recv_num,rate_num)
    line = file.readline()
rtt = list(map(lambda x: x[0]-x[1], zip(recv_time, send_time)))
file = open("dctcp/rtt.txt","w")

for t,rateo,raten,nod in zip(rtt,oldrate,newrate,node):
    file.write(str([t,rateo,raten]))
    file.write("\n")
file.close()
print(rtt)
