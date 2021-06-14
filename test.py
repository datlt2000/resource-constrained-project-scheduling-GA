optimal_file = open("./result_final/j30_optimal.txt", "r")
test_file = open("./result_final/j30_minAff.txt")
optimal_data = optimal_file.readlines()
test_data = test_file.readlines()
optimal_file.close()
test_file.close()
optimal = []
test = []
for line in optimal_data:
    optimal.append(line.split(" ")[2])
for line in test_data:
    test.append(line.split(" ")[1])
print(len(test))
dev = 0
reachOptimal = 0
for i in range(len(test)):
    temp = float(test[i])-float(optimal[i])
    if temp == 0:
        reachOptimal+=1
    dev += temp/float(optimal[i])
dev_avg = dev/len(test)*100
print(dev_avg)
print(reachOptimal)