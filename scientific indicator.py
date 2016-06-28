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
        self.get_OBV()
        self.get_MA5()
        self.get_MA6()
        self.BIAS6()
        self.PSY12()
        self.SY()
        self.ASY5()
        self.ASY4()
        self.ASY3()
        self.ASY2()
        self.ASY1()


    def stochastic_K(self):
        try:
            temp_data = data[self.index-n+1:]


    def get_OBV(self):
        try:
            temp_data = data[self.index - 1]
            if temp_data.closeP > self.closeP:
                theta = 1
            else:
                theta = -1
            self.OBV = temp_data.get_OBV() + theta * self.VOL
        except:
            self.OBV = 'invalid'

    def get_MA5(self):
        try:
            temp_data = data[self.index - 4:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 5
            self.MA5 = s
        except:
            self.MAS = 'invalid'

    def get_MA6(self):
        try:
            temp_data = data[self.index - 5:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 6
            self.MA6 = s
        except:
            self.MA6 = 'invalid'

    def get_BIAS6(self):
        try:
            self.BIAS6 =  (float(self.closeP) - self.get_MA6())/self.get_MA6()
        except:
            self.BIAS6 = 'invalid'

    def get_PSY12(self):
        try:
            temp_data = data[self.index - n + 1:self.index + 1]
            A = 0
            for i in temp_data:
                if i.closeP > i.openP:
                    A += 1
            self.PSY12 = A / 12.0
        except:
            self.PSY12 = 'invalid'

    def get_SY(self):
        try:
            temp_data = data[self.index - 1]
            self.SY = (math.log(self.closeP) - math.log(temp_data.closeP)) * 100.0
        except:
            self.SY = 'invalid'

    def get_ASY5(self):
        try:
            temp_data = data[self.index - 4:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 5
            self.ASY5 = s
        except:
            self.ASY5 = 'invalid'

    def get_ASY4(self):
        try:
            temp_data = data[self.index - 3:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 4
            self.ASY4 = s
        except:
            self.ASY4 = 'invalid'

    def get_ASY3(self):
        try:
                temp_data = data[self.index - 2:self.index + 1]
                s = 0.0
                for i in temp_data:
                    s += i.get_SY()
                s /= 3
                self.ASY3 = s
        except:
            self.ASY3 = 'invalid'

    def get_ASY2(self):
        try:
            temp_data = data[self.index - 1:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.get_SY()
            s /= 2
            self.ASY2 = s
        except:
            self.ASY2 = 'invalid'

    def get_ASY1(self):
        try:
            temp_data = data[self.index - 1]
            self.ASY1 = temp_data.get_SY()
        except:
            self.ASY1 = 'invalid'


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




