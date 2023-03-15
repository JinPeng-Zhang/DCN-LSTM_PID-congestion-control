import  matplotlib.pyplot as plt

file = open("2.txt","r")
line = file.readline()
rtt = []
rate = []
while line:
    line = line.split(",")
    rtt.append(int(line[0].split("[")[1]))
    rate.append(float(line[1].split(" ")[1]))
    line = file.readline()

plt.plot(rtt)
#plt.plot(rate)
plt.show()