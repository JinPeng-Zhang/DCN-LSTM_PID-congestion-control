
'''
读取ns仿真timely算法的数据进行训练
'''

import torch
class datareader():
    def __init__(self,path):
        self.path = path
    def learnable(self,ratediff):
        if ratediff == -99:
            return False
        return True
    def dataset(self):
        file = open(self.path,"r")
        line = file.readline()
        input = []
        output = []
        while line:
            #print(line.split(" "))
            _, node, rtt, rttdiff, gradient,_,rateold, ratenew = line.split(" ")
            if(self.learnable(float(ratenew.split(":")[1].split("\n")[0])-float(rateold.split(":")[1]))):
                input.append([float(rtt.split(":")[1]), float(rttdiff.split(":")[1]), float(rateold.split(":")[1])])
                output.append(float(ratenew.split(":")[1].split("\n")[0])-float(rateold.split(":")[1]))
            line = file.readline()
        return input,output
    def setshape(self,input,input_size):
        input = torch.tensor(input)
        batch_size, seq_len, input_size = input_size
        input = torch.reshape(input,[-1,seq_len, input_size])
        return input


reader = datareader("data2.txt")
input,output = reader.dataset()
input = input[:-(len(input)%3)]
output = output[:-(len(output)%3)]
input = reader.setshape(input,[1,3,3])
output= reader.setshape(output,[1,3,1])
print(input)


###数据预处理
##模型
##数据集训练
##结果显示
