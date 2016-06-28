import math

f = open('0US1.MSFT_160101_160531.txt','r')
content = []
for line in f:
    content.append(line)
f.close()
content = content[1:]
for i in range(len(content)):
    content[i] = content[i].split(';')
n = 5
t = 60
class bundle:
    def __init__(self,name,date,time,openP,highP,lowP,closeP,VOL,index):
        self.name = str(name)
        self.date = str(date)
        self.time = str(time)
        self.openP = float(openP)
        self.highP = float(highP)
        self.lowP = float(lowP)
        self.closeP = float(closeP)
        self.VOL = int(VOL[:-1])
        self.sequence = int(self.date+self.time)
        self.index = int(index)


        def stochastic_K(self):
            temp_data = data[self.index-n+1:]


        def get_OBV(self):
            temp_data = data[self.index - 1]
            if temp_data.closeP > self.closeP:
                theta = 1
            else:
                theta = -1
            self.OBV = temp_data.get_OBV() + theta * VOL
            return self.OBV
        def get_MA5(self):
            temp_data = data[self.index - 4:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 5
            return s
        def get_MA6(self):
            temp_data = data[self.index - 5:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 6
            return s
        def get_BIAS6(self):
            return (float(self.closeP) - self.get_MA6())/self.get_MA6()
        def get_PSY12(self):
            temp_data = data[self.index - n + 1:self.index + 1]
            A = 0
            for i in temp_data:
                if i.closeP > i.openP:
                    A += 1
            return A / 12.0
        def get_SY:
            temp_data = data[self.index - 1]
            return (math.log(self.closeP) - math.log(temp_data.closeP)) * 100.0
        def get_ASY5:
            temp_data = data[self.index - 4:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 5
            return s
        def get_ASY4:
            temp_data = data[self.index - 3:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 4
            return s
        def get_ASY3:
            temp_data = data[self.index - 2:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 3
            return s
        def get_ASY2:
            temp_data = data[self.index - 1:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 2
            return s
        def get_ASY1:
            temp_data = data[self.index - 1]
            return temp_data.get_SY()


all_data = []
temp_data = []
data = []
for i in range(len(content)):
    all_data.append(bundle(content[i][0],content[i][2],content[i][3],\
                       content[i][4],content[i][5],content[i][6],\
                       content[i][7],content[i][8],i))
count = 0
for i in range(len(all_data)-1,t-1,-1*t):
    temp_highP = 0
    temp_lowP = 0
    temp_VOL = 0
    for j in range(t):
        if temp_highP < all_data[i-t].highP:
            temp_highP = all_data[i-t].highP
        if temp_lowP > all_data[i-t].lowP:
            temp_lowP = all_data[i-t].lowP
        temp_VOL += int(all_data[i-t].VOL)
    temp_data.append(bundle(all_data[i].name,all_data[i-t+1].date,all_data[i-t+1].time,all_data[i-t+1].openP,\
                            temp_highP,temp_lowP,all_data[i].closeP,str(temp_VOL)+' ',0))
for i in range(len(temp_data)-1,-1,-1):
    data.append(temp_data[i])
    data[-1].index = len(data)-1
print data[:10],data[-10:]




