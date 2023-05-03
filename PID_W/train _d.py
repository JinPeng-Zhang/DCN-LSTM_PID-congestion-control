
import  numpy as np
class train():
    def __init__(self):
        self.p = -1
        self.i = 0
        self.d = 0
        self.target = 5.22
        self.learn_rate = 0.001
    def grad(self,newrtt,out,oldrate,oldrtt,c):
        if c>1.5:
            c=1.5
        elif c<0.4:
            c=0.4
        return  (newrtt-self.target)*out*((newrtt-oldrtt)/(c))
    def sgn(self,x):
        if x>0:
            return 1
        elif x==0:
            return 0
        else:
            return -1
'''
读取文件内容，去除算法启动数据及最后的非拥塞数据
'''
grad = []
for j in range(20):
    file = open("DATA2/{}.txt".format(j+2),"r")
    line  =file.readline()
    data = []
    num = 0
    for i in range(200):
        line =file.readline()
    while line:
        _,oldrate,oldrtt,c,_,_,_,e,eold,eavg,_ = line.split(" ")
        if num<5000:
            data.append([float(oldrate.split(":")[-1]),float(oldrtt.split("t")[-1]),float(c.split(":")[-1]),float(e.split(":")[-1])-float(eold.split(":")[-1])])
            num = num+1

        line = file.readline()
    ##rate out c e
    tra = train()

    for i in range(len(data)-14):
        grad.append()
        #grad.append(tra.grad(np.mean([t[1] for t in data[i + 1:i + 5]]), np.mean([t[3] for t in data[i :i + 4]]), np.mean([t[0] for t in data[i :i + 4]]), np.mean([t[1] for t in data[i :i + 4]]),  np.mean([t[2] for t in data[i :i + 4]])))
print(sum(grad)/len(grad))