'''
30%LOAD+INCAST
1000000flows+500KB*60
time = 0.1s incast:266.7
'''
import  numpy as np
import  random
nums = np.random.poisson(2.667,10)
RATE = 2.667

file = open("tmp_traffic.txt","r")
line = file.readline()

file2 = open("flow1.txt","w")
file2.write(line)
line = file.readline()

rat = 1000000/266.7
time = 2
num = 0
insert = []
for i in range(nums[0]):
    insert.append(int((i+1)*9000/(nums[0]+1)))

while line  :
    num = num +1
    if num%10000 == 0:
        insert = []
        step = int(num/10000)
        for i in range(nums[step]):
            insert.append(int((i + 1) * 9000 / (nums[0] + 1)))
    if num%10000 in insert:
        send = random.sample(range(0,320),61)
        for k in send[0:-1]:
            file2.write("{} {} 3 100 500000 {}\n".format(k,send[-1],time))

    if num==98803:
        break
    line = file.readline()
    print(line.split(" "))
    time = float(line.split(" ")[-1]) + 0.000000001
    time = round(time,9)
    file2.write(line)
print(len(nums),sum(nums),nums)


