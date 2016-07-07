file_name = 'scientific indicator.csv'
f = open(file_name,'r')
data = []
extra_data = []
used_data = []
for line in f:
    if len(data)>= 500:
        extra_data.append(line.split(','))
    else:
        data.append(line.split(','))
        data[-1][-1] = data[-1][-1][:-1]
data = data[1:]
f.close()
for i in range(len(data)):
    valid = True
    for j in range(len(data[i])):
        if data[i][j] == 'invalid':
            valid = False
            break
    if valid:
            used_data.append(data[i][1:])
for i in range(len(used_data)):
    for j in range(len(used_data[i])):
        if j != len(used_data[i]) - 1:
            used_data[i][j] = float(used_data[i][j])
from sklearn import tree
training_set = []
target_set = []
for i in range(len(used_data)):
    training_set.append(used_data[i][:-2])
    target_set.append(used_data[i][-1])
clf = tree.DecisionTreeClassifier()
clf = clf.fit(training_set,target_set)

#test
s = 100
c = 0
buy = 0
sell = 0
do_nothing = 0
_buy = 0
_sell = 0
_do_nothing = 0
buy_ = 0
sell_ = 0
do_nothing_ = 0
for n in range(0, s):
    test_input = []
    # n = 10
    extra_data[n][-1] = extra_data[n][-1][:-1]
    test_input = extra_data[n][1:-2]
    test_output = extra_data[n][-1]
    prediction = clf.predict(test_input)
    # print 'target:',test_output
    if test_output == "BUY":
        _buy += 1
    elif test_output == "SELL":
        _sell += 1
    elif test_output == "do_nothing":
        _do_nothing += 1
    if prediction == test_output:
        c += 1
        if prediction == "BUY":
            buy += 1
        elif prediction == "SELL":
            sell += 1
        elif prediction == "do_nothing":
            do_nothing += 1
    else:
        if test_output == "BUY":
            buy_ += 1
        elif test_output == "SELL":
            sell_ += 1
        elif test_output == "do_nothing":
            do_nothing_ += 1
print "prediction accuracy =", str(float(c) / s  * 100) + "%"
print "out of all cases,"
print "buy is", str(float(_buy) / s * 100) + "%"
print "sell is", str(float(_sell) / s  * 100) + "%"
print "do_nothing is", str(float(_do_nothing) / s  * 100) + "%"
print "out of successfully predicted cases,"
print "buy is", str(float(buy) / c  * 100) + "%"
print "sell is", str(float(sell) / c  * 100) + "%"
print "do_nothing is", str(float(do_nothing) / c  * 100) + "%"
print "out of unsuccessfully predicted cases,"
print "buy is", str(float(buy_) / (s - c)  * 100) + "%"
print "sell is", str(float(sell_) / (s - c)  * 100) + "%"
print "do_nothing is", str(float(do_nothing_) / (s - c)  * 100) + "%"



