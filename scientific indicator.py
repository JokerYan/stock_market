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
class minute:
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
        def get_OBV(self, temp_data = data[self.index - 1]):
            if temp_data.closeP > self.closeP:
                theta = 1
            else:
                theta = -1

data = []
for i in range(len(content)):
    data.append(minute(content[i][0],content[i][2],content[i][3],\
                       content[i][4],content[i][5],content[i][6],\
                       content[i][7],content[i][8],i))

