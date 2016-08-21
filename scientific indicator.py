import math
output_file_name = 'scientific indicator.csv'
info_file_name = 'bundle information.csv'
f = open('US1.MSFT_130101_160531.txt','r')
O = open(output_file_name,'w')
I = open(info_file_name,'w')
content = []
for line in f:
    content.append(line)
f.close()
content = content[1:]
for i in range(len(content)):
    content[i] = content[i].split(',')
n = 5
t = 1
boundary = 0.1
max_profitable = 0
min_profitable = 0
print len(content)/t
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

    def create_indicator(self):
        self.get_OBV()
        self.get_MA5()
        self.get_MA6() #not included
        self.get_BIAS6()
        self.get_PSY12()
        self.get_SY() #not included
        self.get_ASY5()
        self.get_ASY4()
        self.get_ASY3()
        self.get_ASY2()
        self.get_ASY1()
        self.get_stochastic_K()
        self.get_stochastic_D()
        self.get_stochastic_slow_D()
        self.get_momentum()
        self.get_ROC()
        self.get_LW_R()
        self.get_AO_oscillator()
        self.get_disparity5()
        self.get_disparity10()
        self.get_OSCP()
        self.get_Mt() #not included
        self.get_SMt() #not included
        self.get_Dt() #not included
        self.get_CCI()
        self.get_RSI()
        self.get_future_profitable()

    def get_future_profitable(self):
        try:
            temp_data = data[self.index:self.index+6]
            if self.index+6 > len(data)-1:
                raise IndexError
            temp_highP = self.highP
            temp_lowP = self.lowP
            for i in temp_data:
                if i.highP > temp_highP:
                    temp_highP = i.highP
                if i.lowP < temp_lowP:
                    temp_lowP = i.lowP
            self.future_profitable = (temp_highP - self.highP) - (self.lowP - temp_lowP)
        except IndexError:
            self.future_profitable = 'invalid'

    def get_decision(self):
        global max_profitable
        global min_profitable
        if self.future_profitable == "invalid":
            self.decision = "invalid"
        elif self.future_profitable > max_profitable * boundary:
        # elif self.future_profitable > 0:
            self.decision = "BUY"
        elif self.future_profitable < min_profitable * boundary:
        # elif self.future_profitable < 0:
            self.decision = "SELL"
        else:
            self.decision = "do_nothing"

    def output_data(self):
        global O
        O.write(str(self.index)+','+str(self.OBV)+","+str(self.MA5)+","+str(self.BIAS6)\
                +","+str(self.PSY12)+","+str(self.ASY5)+","+str(self.ASY4)+","+str(self.ASY3)\
                + "," + str(self.ASY2)+","+str(self.ASY1)+","+str(self.stochastic_K)+","+str(self.stochastic_D) \
                + "," + str(self.stochastic_slow_D)+","+str(self.momentum)+","+str(self.ROC)+","+str(self.LW_R) \
                + "," + str(self.AO_oscillator)+","+str(self.disparity5)+","+str(self.disparity10)+","+str(self.OSCP) \
                +","+str(self.CCI)+","+str(self.RSI)+','+str(self.future_profitable)+','+str(self.decision)+'\n')
        # O.write(str(self.index)+';'+str(self.openP)+';'+str(self.highP)+';'+str(self.lowP)+';'+str(self.VOL)+'\n')

    def output_info(self):
        I.write(str(self.name)+','+str(self.index)+','+str(self.openP)+','+str(self.highP) \
                + ',' + str(self.lowP)+','+str(self.closeP)+','+str(self.VOL)+'\n')

    def get_stochastic_K(self):
        try:
            temp_data = data[self.index-n+1:self.index+1]
            N_lowP = 10000
            N_highP = 0
            for i in range(len(temp_data)):
                if temp_data[i].lowP < N_lowP:
                    N_lowP = temp_data[i].lowP
                if temp_data[i].highP > N_highP:
                    N_highP = temp_data[i].highP
            self.stochastic_K = (temp_data[-1].closeP - N_lowP)/(N_highP - N_lowP)*100
        except:
            self.stochastic_K = 'invalid'

    def get_stochastic_D(self):
        try:
            if self.index-n+1<0:
                raise IndexError
            temp_data = data[self.index-n+1:self.index+1]
            sum = 0
            for i in range(len(temp_data)):
                sum += temp_data[i].stochastic_K
            self.stochastic_D = sum/n
        except:
            self.stochastic_D = 'invalid'

    def get_stochastic_slow_D(self):
        try:
            if self.index-n+1<0:
                raise IndexError
            temp_data = data[self.index-n+1:self.index+1]
            sum = 0
            for i in range(len(temp_data)):
                sum += temp_data[i].stochastic_D
            self.stochastic_slow_D = sum/n
        except:
            self.stochastic_slow_D = 'invalid'

    def get_momentum(self):
        try:
            if self.index-n+1<0:
                raise IndexError
            self.momentum = self.closeP - data[self.index-n+1].closeP
        except:
            self.momentum = 'invalid'

    def get_ROC(self):
        try:
            self.ROC = self.closeP/data[self.index-n].closeP
        except:
            self.ROC = 'invalid'

    def get_LW_R(self):
        try:
            temp_data = data[self.index-n+1:self.index+1]
            N_lowP = 10000
            N_highP = 0
            for i in range(len(temp_data)):
                if temp_data[i].lowP < N_lowP:
                    N_lowP = temp_data[i].lowP
                if temp_data[i].highP > N_highP:
                    N_highP = temp_data[i].highP
            self.LW_R =(N_highP - temp_data[-1].closeP)/(N_highP - N_lowP)*100
        except:
            self.LW_R = 'invalid'

    def get_AO_oscillator(self):
        try:
            self.AO_oscillator = (self.highP - data[self.index-1].closeP)/(self.highP - self.lowP)
        except ZeroDivisionError:
            self.AO_oscillator = 10

    def get_disparity5(self):
        try:
            self.disparity5 = self.closeP/self.MA5*100
        except:
            self.disparity5 = 'invalid'

    def get_disparity10(self):
        try:
            temp_data = data[self.index - 9:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 10
            self.disparity10 = self.closeP/s
        except:
            self.disparity10 = 'invalid'

    def get_OSCP(self):
        try:
            temp_data = data[self.index - 9:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 10
            self.OSCP = (self.MA5 - s)/self.MA5
        except:
            self.OSCP = 'invalid'

    def get_Mt(self):
        try:
            self.Mt = (self.highP + self.lowP + self.closeP)/3
        except:
            self.Mt = 'invalid'

    def get_SMt(self):
        try:
            temp_data = data[self.index-n+1:self.index+1]
            sum = 0
            for i in range(len(temp_data)):
                sum += temp_data[i].Mt
            self.SMt = sum/n
        except:
            self.SMt = 'invalid'

    def get_Dt(self):
        try:
            temp_data = data[self.index-n+1:self.index+1]
            sum = 0
            for i in range(len(temp_data)):
                sum += temp_data[i].Mt- temp_data[i].SMt
            self.Dt = sum/n
        except:
            self.Dt = 'invalid'

    def get_CCI(self):
        try:
            self.CCI = (self.Mt - self.SMt) / (0.015 * self.Dt)
        except:
            self.CCI = 'invalid'

    def get_RSI(self):
        try:
            temp_data = data[self.index - n:self.index+1]
            up_sum = 0.
            down_sum = 0
            for i in range(len(temp_data)-1):
                if temp_data[i].closeP < temp_data[i+1].closeP:
                    up_sum += float(temp_data[i+1].closeP - temp_data[i].closeP)
                else:
                    down_sum += float(temp_data[i].closeP - temp_data[i+1].closeP)
            self.RSI = 100-100/(1+(up_sum/n)/(down_sum))
        except IndexError:
            self.RSI = 'invalid'
        except ZeroDivisionError:
            self.RSI = 1000

    def get_OBV(self):
        # try:
            if self.index == 0:
                self.OBV = 0
            else:
                temp_data = data[self.index - 1]
                if temp_data.closeP > self.closeP:
                    theta = 1
                else:
                    theta = -1
                self.OBV = temp_data.OBV + theta * self.VOL
        # except IndexError:
        #     self.OBV = 'invalid'
        #     raise IndexError



    def get_MA5(self):
        try:
            if self.index-4<0:
                raise IndexError
            temp_data = data[self.index - 4:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 5
            self.MA5 = s
        except:
            self.MA5 = 'invalid'

    def get_MA6(self):
        try:
            temp_data = data[self.index - 5:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.closeP
            s /= 6
            self.MA6 = s
        except IndexError:
            self.MA6 = 'invalid'

    def get_BIAS6(self):
        try:
            self.BIAS6 =(float(self.closeP) - self.MA6)/self.MA6
        except IndexError:
            self.BIAS6 = 'invalid'
        except ZeroDivisionError:
            if float(self.closeP) - self.MA6>0:
                self.BIAS6 = 0.1
            else:
                self.BIAS6 = -0.1

    def get_PSY12(self):
        try:
            if self.index - n + 1<0:
                raise IndexError
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
            if self.index-4<0:
                raise IndexError
            temp_data = data[self.index - 4:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.SY
            s /= 5
            self.ASY5 = s
        except:
            self.ASY5 = 'invalid'

    def get_ASY4(self):
        try:
            if self.index-3<0:
                raise IndexError
            temp_data = data[self.index - 3:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.SY
            s /= 4
            self.ASY4 = s
        except:
            self.ASY4 = 'invalid'

    def get_ASY3(self):
        try:
            if self.index-2<0:
                raise IndexError
            temp_data = data[self.index - 2:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.SY
            s /= 3
            self.ASY3 = s
        except:
            self.ASY3 = 'invalid'

    def get_ASY2(self):
        try:
            if self.index-1<0:
                raise IndexError
            temp_data = data[self.index - 1:self.index + 1]
            s = 0.0
            for i in temp_data:
                s += i.SY
            s /= 2
            self.ASY2 = s
        except:
            self.ASY2 = 'invalid'

    def get_ASY1(self):
        try:
            if self.index-1<0:
                raise IndexError
            temp_data = data[self.index - 1]
            self.ASY1 = temp_data.SY
        except:
            self.ASY1 = 'invalid'


all_data = []
reverse_data = []
data = []
for i in range(len(content)):
    all_data.append(bundle(content[i][0],content[i][2],content[i][3],\
                       content[i][4],content[i][5],content[i][6],\
                       content[i][7],content[i][8],i))
count = 0
for i in range(len(all_data)-1,t-1,-1*t):
    temp_highP = 0
    temp_lowP = 10000
    temp_VOL = 0
    for j in range(t):
        if temp_highP < all_data[i-t].highP:
            temp_highP = all_data[i-t].highP
        if temp_lowP > all_data[i-t].lowP:
            temp_lowP = all_data[i-t].lowP
        temp_VOL += int(all_data[i-t].VOL)
    reverse_data.append(bundle(all_data[i].name,all_data[i-t+1].date,all_data[i-t+1].time,all_data[i-t+1].openP,\
                            temp_highP,temp_lowP,all_data[i].closeP,str(temp_VOL)+' ',0))
for i in range(len(reverse_data)-1,-1,-1):
    data.append(reverse_data[i])
    data[-1].index = len(data)-1
for i in range(len(data)):
    data[i].create_indicator()
profitable_list = []
for i in range(len(data)):
    t = data[i].future_profitable
    if t != "invalid":
        profitable_list.append(t)
max_profitable = max(profitable_list)
min_profitable = min(profitable_list)
for i in range(len(data)):
    data[i].get_decision()
O.write('index' + ',' + 'OBV' + "," + 'MA5' + "," + 'BIAS6' \
        + "," + "PSY12" + "," +'ASY5' + "," + 'ASY4' + "," + "ASY3" \
        + "," + "ASY2" + "," + 'ASY1' + "," + 'stochastic_K' + "," +'stochastic_D' \
        + "," + 'stochastic_slow_D' + "," + 'momentum' + "," + 'ROC' + "," + 'LW_R' \
        + "," + 'AO_oscillator' + "," + 'disparity5' + "," + 'disparity10' + "," + 'OSCP' \
        + "," + 'CCI' + "," + 'RSI' + ',' + 'future_profitable' \
        + ',' + 'decision' + '\n')
I.write('name' + ',' + 'index' + ',' 'openP' + ',' + 'highP' \
        + ',' + 'lowP' + ',' + 'closeP' + ',' + 'VOL'+'\n')
for i in range(len(data)):
    data[i].output_data()
    data[i].output_info()
O.close()
I.close()

