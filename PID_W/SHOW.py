import matplotlib.pyplot as plt
rtt1 = []
rtt1s = 0

rtt2 = []
rtt2s = 0
rtt3 = []
rtt3s = 0
rtt_5len_max = 0
for i in range(20):
    file = open("p_-1/{}.txt".format(i+2))
    rtt_5len = -100

    line = file.readline()

    while line:
        _,_,newrtt,_,_,_,_,_ = line.split(" ")
        rtt1.append(float(newrtt.split("t")[-1]))
        if rtt1[-1]>5:
            rtt1s = rtt1s+1

        line = file.readline()
    file = open("p_-1.1/{}.txt".format(i+2))

    line = file.readline()

    while line:
        _,rate,newrtt,_,_,_,_,_ = line.split(" ")
        rtt2.append(float(newrtt.split("t")[-1]))
        if rtt2[-1] > 5:
            rtt2s = rtt2s + 1
            if rtt_5len_max < rtt_5len:
                rtt_5len_max = rtt_5len
                if rtt_5len_max == 17:
                    print(rate,newrtt)
            rtt_5len = 0
        else:
            rtt_5len = rtt_5len + 1
        line = file.readline()

    file = open("p_-2/{}.txt".format(i + 2))

    line = file.readline()

    while line:
        _, _, newrtt, _, _, _, _, _ = line.split(" ")
        rtt3.append(float(newrtt.split("t")[-1]))
        if rtt3[-1] > 5:
            rtt3s = rtt3s + 1

        line = file.readline()
plt.plot(rtt1,color="green")
plt.plot(rtt2,color="blue")
plt.plot(rtt3,color="red")
plt.show()
print( rtt_5len_max)
print(rtt1s/len(rtt1),rtt2s/len(rtt2),rtt3s/len(rtt3))