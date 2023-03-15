
import  numpy as np
import  math
import matplotlib.pyplot as plt

##发送速率5Mbps-50Mbps
ratelow = 5
ratehigh = 50
##rtt往返时延5us-1000us,thre = 50
rttlow = 5
rtthigh = 1000
###flow_size GB
flownum = 20
flowsize = np.around(np.random.rand(flownum,1)*10000,decimals=2)
#print(flowsize)
flow_sum = np.sum(10*flowsize)
####pipeline
pipeline_contain = 1000 #MB
pipeline = float
pdrop = 1/200
#dealrate = 30+np.around(np.random.rand(1,1),decimals=2)
pipeline_congest = 600
pipeline_drop = 800
grmma = np.log(200)/1000

cctcp = 1
ccdip = 2
ccrand = 3



#policyΠ = rateup if dropnum = 0,rate += rand([0,1]),else rate -= rand([0,1])
T = 3600
rate = 5
drop_num = 0
pipeline = 0
cc_mode = ccrand
rtt = 5
base_rtt = 5
def policy_dip(rate,realdrop,rtt):
    pass
def policy_tcp(rate,realdrop,rtt):
    if realdrop==0:
        rate =  rate + np.around(np.random.rand(),decimals=2)
    else:
        rate =  rate - np.around(np.random.rand(),decimals=2)
    if rate>50:
        rate = 50
    if rate<5:
        rate = 5
    return  rate
def policy_rand(rate,realdrop,rtt):
    if realdrop>0:
        rate1 = 5
    else:
        rate1 = abs(60*np.around(np.random.rand(),decimals=2))
    return rate1
def policy(rate,realdrop,rtt,cc_mode):
    if(cc_mode == cctcp):
        return policy_tcp(rate,realdrop,rtt)
    elif(cc_mode == ccdip):
        return policy_dip(rate,realdrop,rtt)
    elif(cc_mode==ccrand):
        return  policy_rand(rate,realdrop,rtt)
    else :
        return 5




#####
##数据统计
data = []
#########
file = open("data_random5.txt","w")
while(flow_sum>0):
    if(flow_sum<rate):
        rate = flow_sum
    flow_sum = flow_sum-rate
    pipeline += rate
    T = T+1
    ##检查是否需要丢包

    drop_nums = 0
    if(pipeline>800):
        for check in range(int(pipeline)-800):
                drop_nums = drop_nums+np.around(np.random.rand(),decimals=2)*check*pdrop
    drop_num  = drop_num+drop_nums


    pipeline = pipeline - drop_nums
    dealrate = 30 + np.around(np.random.rand(), decimals=2)
    if(pipeline>dealrate):
        pipeline = pipeline-dealrate
    else:
        pipeline = 0
    rtt = pipeline + base_rtt + np.around(np.random.rand(), decimals=2)
    realdrop = drop_nums/rate


    print(rate,rtt,realdrop,pipeline+drop_nums+dealrate)
    file.write("{} {} {} {} {}\n".format(rate, rtt, realdrop, pipeline + drop_nums + dealrate, pipeline))
    rate = policy(rate,realdrop,rtt,cc_mode)
    data.append([rate,rtt,realdrop,pipeline+drop_nums+dealrate])
#print(drop_num,T)
file.close()
plt.plot(data)
plt.show()
