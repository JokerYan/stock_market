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


# permutation
def permutation(list1):
    if len(list1) == permutation_size:
        count_one = 0
        for i in range(len(list1)):
            if list1[i] == '1':
                count_one += 1
        if count_one >= 2:
            f.write(list1 + '\n')
        return
    permutation(list1 + '0')
    permutation(list1 + '1')
    return

try:
    f = open('permutation.txt', 'r')
except IOError:
    f = open('permutation.txt', 'w')
    permutation_size = len(training_set[0])
    permutation('')
    f.close()
    f = open('permutation.txt', 'r')

prediction_accuracy = []
buy_total = []
sell_total = []
do_nothing_total = []
buy_success = []
sell_success = []
do_nothing_success = []
buy_fail = []
sell_fail = []
do_nothing_fail = []

count = 0
highest_prediciton = [0,0]
for line in f:
    count += 1
    # if count > 500:
    #     break
    print count
    training_set_temp = []
    for i in range(len(training_set)):
        training_set_temp.append([])
        for j in range(len(line)):
            if line[j] == '1':
                training_set_temp[i].append(training_set[i][j])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(training_set_temp,target_set)

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
    extra_data_temp = []
    for i in range(len(extra_data)):
        extra_data_temp.append([])
        for j in range(len(line)):
            if line[j] == '1':
                extra_data_temp[-1].append(extra_data[i][j])
    for n in range(0, s):
        test_input = []
        # n = 10
        test_input = extra_data_temp[n]
        test_output = extra_data[n][-1][:-1]
        prediction = clf.predict(test_input)[0]
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
    # prediction_accuracy.append(float(c) / s  * 100)
    # buy_total.append(float(_buy) / s * 100)
    # sell_total.append(float(_sell) / s  * 100)
    # do_nothing_total.append(float(_do_nothing) / s  * 100)
    # buy_success.append((float(buy) / c  * 100))
    # sell_success.append((float(sell) / c  * 100))
    # do_nothing_success.append((float(do_nothing) / c  * 100))
    # buy_fail.append((float(buy_) / (s - c)  * 100))
    # sell_fail.append(float(sell_) / (s - c)  * 100)
    # do_nothing_fail.append(float(do_nothing_) / (s - c)  * 100)
    current_prediction_result = [count-1,float(c) / s  * 100,float(_buy) / s * 100,float(_sell) / s * 100,float(_do_nothing) / s * 100, \
                                 (float(buy) / c * 100),(float(sell) / c * 100),(float(do_nothing) / c  * 100), \
                                 (float(buy_) / (s - c) * 100),float(sell_) / (s - c)  * 100,float(do_nothing_) / (s - c)* 100]
    if current_prediction_result[1] > highest_prediciton[1]:
        highest_prediction = current_prediction_result
    print highest_prediction[1]
print highest_prediction
