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
        used_data[i][j] = float(used_data[i][j])
from sklearn.neighbors import KNeighborsRegressor
training_set = []
target_set = []
for i in range(len(used_data)):
    training_set.append(used_data[i][:-1])
    target_set.append(used_data[i][-1])
clf = KNeighborsRegressor(n_neighbors=2)
clf = clf.fit(training_set,target_set)

#test
test_input = []
n = 0
extra_data[n][-1] = extra_data[n][-1][:-1]
test_input = extra_data[n][1:-1]
test_output = extra_data[n][-1]
print clf.predict(test_input)
print 'target:',test_output


