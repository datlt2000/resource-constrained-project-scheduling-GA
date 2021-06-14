from const import FILE_PATH
from ga import GA
import glob
base_ga = GA(select_method="minAff", partial_optimize=False, initial_method="priority", local_search=False)
files = glob.glob("./j60rcp/J60[1-5]_*")

for file in files:
    result = 0
    cost = 10000
    solution = None
    base_ga.get_data(file)
    for i in range(5):
        best_cost, best_solution = base_ga.run_GA()
        result += best_cost
        if best_cost < cost:
            cost = best_cost
            solution = best_solution
    line = file.split("\\")[-1] + " " + str(cost) + " " + str(solution) + "\n"
    print(line)
    f = open('./result_j60/j60_minAff.txt', "a")
    f.write(line)
    f.close()
# base_ga.get_data(FILE_PATH)
# best_cost, best_solution = base_ga.run_GA()
# line = str(best_cost) + "\t" + str(best_solution) + "\n"
# print(line)
