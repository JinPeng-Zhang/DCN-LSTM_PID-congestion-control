import matplotlib.pyplot as plt
import  matplotlib
matplotlib.rcParams['axes.unicode_minus']=False
plt.rcParams["font.sans-serif"]=["SimHei"]
file = open("LINUX-NS3-SIMULATE/pidw2.txt")

line = file.readline()
ws = [[-0.2],[-0.05],[0.1]]
while line:
    node,w,_,_,_,_,_,_ = line.split(" ")
    node = float(node.split(":")[1])
    if node== 4:
        ws[0].append((float(w.split("|")[0].split(":")[1])+len(ws[0])*ws[0][-1])/(len(ws[0])+1))
        ws[1].append((float(w.split("|")[1])+len(ws[1])*ws[1][-1])/(len(ws[1])+1))
        ws[2].append((float(w.split("|")[2])+len(ws[2])*ws[2][-1])/(len(ws[2])+1))

    line = file.readline()


plt.plot(ws[0],label="kp")
plt.plot(ws[1],label="ki")
plt.plot(ws[2],label="kd")
plt.xlabel("优化次数")
plt.ylabel("参数大小")
plt.legend()
plt.show()