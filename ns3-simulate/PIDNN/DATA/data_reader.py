import matplotlib.pyplot as plt
import  matplotlib
matplotlib.rcParams['axes.unicode_minus']=False
plt.rcParams["font.sans-serif"]=["SimHei"]
file = open("../../LINUX-NS3-SIMULATE/pidnn_data.txt")

line = file.readline()
nod = []
rate = []
rtt = []

while line:

    node,_,_,_,rat,rt,_,_ = line.split(" ")
    nod.append(float(node.split(":")[1]))
    rate.append(float(rat.split(":")[1]))
    rtt.append(float(rt.split("t")[-1]))
    line = file.readline()
file.close()
rtt = sorted(rtt)
print(rtt[int(len(rtt)*0.99)])
# for i in range(20):
#     file = open("{}.txt".format(i+2),"w")
#     for node,rat,rt in zip(nod,rate,rtt):
#         if node == i+2:
#             file.write("{} {}\n".format(rat,rt))
#     file.close()
#
# plt.show()