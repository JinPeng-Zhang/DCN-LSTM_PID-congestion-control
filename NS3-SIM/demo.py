'''
30%LOAD+INCAST
1000000flows+500KB*60
time = 0.1s incast:266.7
'''
import  numpy as np
import  random

file2 = open("flow1.txt","r")

line = file2.readline()
line = file2.readline()
flow = 0
num = 0
ma =0
while line:
    flow = flow+1
    nod1,nod2,_,_,size,_ = line.split(" ")
    ma = max(int(nod1),int(nod2),ma)
    if float(size)==500000:
       num = num +1
    line = file2.readline()
    print(line.split(" "))
print(flow,num/60,num)
print(ma)
#1011274
#[5 3 1 6 4 4 2 3 4 2]