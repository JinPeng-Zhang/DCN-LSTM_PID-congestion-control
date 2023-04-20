
file = open("fct_fat_flow_hp95ai50.txt")
file2 = open("fct_fat_flow_hp95ai50_d.txt","w")
line = file.readline()

while line:
    _,_,_,_,size,_,_,_ = line.split(" ")
    if float(size) != 500000:
        file2.write(line)
    line = file.readline()