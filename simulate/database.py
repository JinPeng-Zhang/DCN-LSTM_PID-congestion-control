'''
此py文件已被放弃，只作为算法设计过程中的思考记录文档
'''


####################
#基于预测模块的神经网络数据集database
#加载数据集database train,test = input,output
#input是神经网络输入，size = [seq_len,batch_size,input_size] = [3,1,2] drtt+rate_old
#output是rsn神经网络的输出out，size = [seqlen, batch, hidden_size] = [3,1,2] delta
#####################
def GetTrainData(FILENAME):
    input =1
    output =1
    return input,output

def GetTestDate(FILENAME):
    input =11
    output =11
    return input, output