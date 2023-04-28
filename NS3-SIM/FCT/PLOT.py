import matplotlib.pyplot as plt
import  math
file = open("timely.txt")
line = file.readline()
siz = []
FCT = []
while line:
    print(line.split(" "))
    _,size,fct_95,_ = line.split(" ")
    if float(size.split("\t")[0])<1000:
        siz.append(int(size.split("\t")[0]))
    elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
        siz.append("{}K".format(round(float(size.split("\t")[0])/1000)))
    else:
        siz.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
    FCT.append(math.log10(float(fct_95)))
    line = file.readline()

plt.xticks(range(0,len(siz),1),siz,rotation=90)
plt.yticks(range(0,3),[1,10,100])
plt.plot(FCT,label="timely")
#plt.show()


file = open("HPPC.txt")
line = file.readline()
siz1 = []
FCT1 = []
while line:
    print(line.split(" "))
    _,size,fct_95,_ = line.split(" ")
    if float(size.split("\t")[0])<1000:
        siz1.append(int(size.split("\t")[0]))
    elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
        siz1.append("{}K".format(round(float(size.split("\t")[0])/1000)))
    else:
        siz1.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
    FCT1.append(math.log10(float(fct_95)))
    line = file.readline()




#plt.xticks(range(0,len(siz)+1),siz,rotation=90)
# plt.xlim(0,None)
plt.ylim(0,None)
print(siz,FCT)
plt.plot(FCT1,label="HPCC")




file = open("dctcp.txt")
line = file.readline()
siz2 = []
FCT2 = []
while line:
    print(line.split(" "))
    _,size,fct_95,_ = line.split(" ")
    if float(size.split("\t")[0])<1000:
        siz2.append(int(size.split("\t")[0]))
    elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
        siz2.append("{}K".format(round(float(size.split("\t")[0])/1000)))
    else:
        siz2.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
    FCT2.append(math.log10(float(fct_95)))
    line = file.readline()
plt.plot(FCT2,label="dctcp")

file = open("PIDNN.txt")
line = file.readline()
siz3 = []
FCT3 = []
while line:
    print(line.split(" "))
    _,size,fct_95,_ = line.split(" ")
    if float(size.split("\t")[0])<1000:
        siz3.append(int(size.split("\t")[0]))
    elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
        siz3.append("{}K".format(round(float(size.split("\t")[0])/1000)))
    else:
        siz3.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
    FCT3.append(math.log10(float(fct_95)))
    line = file.readline()
plt.plot(FCT3,label="PIDNN")



file = open("DCQCN.txt")
line = file.readline()
siz4 = []
FCT4 = []
while line:
    print(line.split(" "))
    _,size,fct_95,_ = line.split(" ")
    if float(size.split("\t")[0])<1000:
        siz4.append(int(size.split("\t")[0]))
    elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
        siz4.append("{}K".format(round(float(size.split("\t")[0])/1000)))
    else:
        siz4.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
    FCT4.append(math.log10(float(fct_95)))
    line = file.readline()
plt.plot(FCT4,label="DCQCN")

file = open("PIDNN_4_22/PIDNN_CHMIN1RTT5.txt")
line = file.readline()
siz5 = []
FCT5 = []
while line:
    print(line.split(" "))
    _,size,fct_95,_ = line.split(" ")
    if float(size.split("\t")[0])<1000:
        siz5.append(int(size.split("\t")[0]))
    elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
        siz5.append("{}K".format(round(float(size.split("\t")[0])/1000)))
    else:
        siz5.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
    FCT5.append(math.log10(float(fct_95)))
    line = file.readline()
plt.plot(FCT5,label="PIDNN+RTTMIN")

# file = open("PIDNN_4_22/PIDNN_CH6RTT5_vwin.txt")
# line = file.readline()
# siz6 = []
# FCT6 = []
# while line:
#     print(line.split(" "))
#     _,size,fct_95,_ = line.split(" ")
#     if float(size.split("\t")[0])<1000:
#         siz6.append(int(size.split("\t")[0]))
#     elif float(size.split("\t")[0])>1000 and float(size.split("\t")[0])<1000000:
#         siz6.append("{}K".format(round(float(size.split("\t")[0])/1000)))
#     else:
#         siz6.append("{}M".format(round(float(size.split("\t")[0]) / 1000000)))
#     FCT6.append(math.log10(float(fct_95)))
#     line = file.readline()
# plt.plot(FCT6,label="PIDNN+RTTch+win")

plt.xlabel("size")
plt.ylabel("FCT slowdown")
plt.legend()
plt.show()