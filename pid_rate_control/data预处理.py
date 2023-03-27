'''
训练PID神经网络，寻找合适的参数
输入input:(rttpre - rttnew);input_size = (1)
输出output:▲rate;output_size = (1)
'''

'''
rate_new = rate_old(1+output)
output = (rate_new-rate_old)/rate_old or rate_new-rate_old
'''
file = open("dataset/pid1/2.txt")
line = file.readline()
rtt = 0
diff = []
while line:
    rttold = rtt
    rtt,rateo,raten = line.split(" ")
    if float(rttold) != 0:
        diff.append([(float(rtt)-float(rttold))/float(rttold)])
    line = file.readline()
file.close()

file = open("dataset/pid1/data.txt","w")
for rttdif,rttdifn in zip(diff[1:-1],diff[2:]):
    file.write("{} {}\n".format(rttdif[0],-rttdifn[0]))
file.close()
