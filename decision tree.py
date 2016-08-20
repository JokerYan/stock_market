file_name = 'scientific indicator.csv'
f = open(file_name,'r')
data = []
extra_data = []
used_data = []
extra_data_2 = []
total_volume = 5877
for line in f:
    if len(data)>= total_volume*5/6:
        extra_data.append(line.split(','))
        extra_data[-1][-1] = extra_data[-1][-1][:-1]
    elif len(data) >= total_volume*4/6:
        extra_data_2.append(line.split(','))
        extra_data_2[-1][-1] = extra_data_2[-1][-1][:-1]
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
    training_set.append(used_data[i][:-1])
    target_set.append(used_data[i][-1])


# permutation
def permutation(list1):
    if len(list1) == permutation_size :
        count_one = 0
        for i in range(len(list1)):
            if list1[i] == '1':
                count_one += 1
        if count_one >= 1:
            f.write(list1 + '\n')
        return
    permutation(list1 + '0')
    permutation(list1 + '1')
    return

def scoring (list1):
    return (list1[5]*list1[1]/(list1[2]*100) +list1[6]*list1[1]/(list1[3]*100))/2


try:
    permutation_size = len(training_set[0]) / 3
    f = open('permutation.txt', 'r')
except IOError:
    f = open('permutation.txt', 'w')
    permutation_size = len(training_set[0]) / 3
    permutation('')
    f.close()
all_highest_predictions = []
all_voting_accuracy = []
all_voting_accuracy_2 = []
all_voting_volume_2 = []
for sequence in range(0,3):
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

    p = open('prediction_results_'+str(sequence)+'.txt','w')
    classifiers = []
    highest_prediction = [0,0,0,0,0,0,0,0]
    all_prediction_results = []
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
                    training_set_temp[i].append(training_set[i][j + sequence * permutation_size / 3])
        classifiers.append(tree.DecisionTreeClassifier())
        classifiers[-1] = classifiers[-1].fit(training_set_temp,target_set)

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
        for i in range(len(extra_data_2)):
            extra_data_temp.append([])
            for j in range(len(line)):
                if line[j] == '1':
                    extra_data_temp[-1].append(extra_data_2[i][j])
        for n in range(0, s):
            test_input = []
            # n = 10
            test_input = extra_data_temp[n]
            test_output = extra_data_2[n][-1]
            prediction = classifiers[-1].predict(test_input)[0]
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
        try:
            current_prediction_result = [count-1,float(c) / s  * 100,float(_buy) / s * 100,float(_sell) / s * 100,float(_do_nothing) / s * 100, \
                                     (float(buy) / c * 100),(float(sell) / c * 100),(float(do_nothing) / c  * 100), \
                                     (float(buy_) / (s - c) * 100),float(sell_) / (s - c)  * 100,float(do_nothing_) / (s - c)* 100]
        except ZeroDivisionError:
            current_prediction_result = [count-1,float(c) / s  * 100,float(_buy) / s * 100,float(_sell) / s * 100,float(_do_nothing) / s * 100, \
                                     0,0,0, \
                                     (float(buy_) / (s - c) * 100),float(sell_) / (s - c)  * 100,float(do_nothing_) / (s - c)* 100]
        for i in range(len(current_prediction_result)-1):
            p.write(str(current_prediction_result[i])+',')
            # p.write("{0:10}".format(str(current_prediction_result[i]))+',')
        current_prediction_result .append(scoring(current_prediction_result))
        all_prediction_results.append(current_prediction_result)
        p.write(str(current_prediction_result[-1])+'\n')
    #     if current_prediction_result[-1] > highest_prediction[-1]:
    #         highest_prediction = current_prediction_result
    #     print highest_prediction[-1]
    # all_highest_predictions.append(highest_prediction)
    # print highest_prediction
    f.close()

    #voting
    f = open('permutation.txt','r')
    permutation_txt = f.read().splitlines()
    voting_results = []
    voting_accuracy = 0
    voting_results_2 = []
    voting_accuracy_2 = 0
    volume_2 = 0
    for i in range(len(extra_data_2)):
        test_set_2 = []
        buy_voting = 0
        sell_voting = 0
        do_nothing_voting = 0
        for j in range(len(permutation_txt)):
            test_set_2.append([])
            for m in range(len(permutation_txt[j])):
                if permutation_txt[j][m] == '1':
                    test_set_2[-1].append(extra_data_2[i][m + sequence * permutation_size / 3])
        for j in range(len(classifiers)):
            new_prediction = classifiers[j].predict(test_set_2[j])[0]
            if new_prediction == 'BUY':
                buy_voting += all_prediction_results[j][5] * all_prediction_results[j][1] / (all_prediction_results[j][2] *100)/2
            elif new_prediction == 'SELL':
                sell_voting += all_prediction_results[j][6] * all_prediction_results[j][1] / (all_prediction_results[j][3] *100)/2
            elif new_prediction == 'do_nothing':
                try:
                    do_nothing_voting += all_prediction_results[j][7] * all_prediction_results[j][1] / (all_prediction_results[j][4] *100)/2
                except ZeroDivisionError:
                    pass
        if buy_voting > sell_voting and buy_voting > do_nothing_voting:
            voting_results.append('BUY')
        elif sell_voting > buy_voting and sell_voting > do_nothing_voting:
            voting_results.append('SELL')
        else:
            voting_results.append('do_nothing')
        if voting_results[-1] == extra_data_2[i][-1]:
            voting_accuracy += 1
        if voting_results[-1] == 'BUY' or voting_results[-1] == 'SELL':
            volume_2 += 1
            if voting_results[-1] == extra_data_2[i][-1]:
                voting_accuracy_2 += 1
    try:
        all_voting_accuracy.append(voting_accuracy/ float(len(extra_data_2)) * 100)
        all_voting_accuracy_2.append(voting_accuracy_2/float(volume_2)*100)
        all_voting_volume_2.append(volume_2)
    except ZeroDivisionError:
        pass


    p.close()
    f.close()
print all_voting_accuracy,all_voting_accuracy_2,all_voting_volume_2
