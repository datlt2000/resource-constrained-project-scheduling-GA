from population import Population
import sys
from activity import Activity
"""
    class that run GA loop
    GA has 4 operation:
        selection - using tournament selection
        cross - select a part of gen and sort it in the order of the other gen
        mution - select a node, travel to the right as far as possible but pre is true
        finess - makespan
    @param
        pCross {float}: cross operator probability in (0, 1)
        pMution {float}: mution operator probability in (0, 1)
        number_selection {int}: selection operator probability in (1, 10)
        generation {int}: number of loop in (0, 1000)
"""
class GA:
    def __init__(self, generation=1000, size=50, pCross=1, pMution=0.5, number_selection=5, partial_optimize=False,
        select_method="tournament", cross_method="2point", mution_method="1point", initial_method="random", local_search=False):
        self.generation = generation
        self.amount_individual = size
        self.pCross = pCross
        self.pMution = pMution
        self.number_selection = number_selection
        self.selection = select_method
        self.cross = cross_method
        self.mution = mution_method
        self.initial = initial_method
        self.partialOptimize = partial_optimize
        self.localSearch = local_search
        self.reset()

    def reset(self):
        self.best_solution = None
        self.best_cost = sys.maxsize
        self.n = 0 # number of node
        self.k = 0 # number of resource
        self.capacity = []  # max capacity of resource
        self.node = [] # list of node
        self.population = Population()

    # check if param is invalid
    def check_param(self):
        if self.pCross < 0 or self.pCross > 1:
            return False
        if self.pMution < 0 or self.pMution > 1:
            return False
        if self.number_selection <= 0 or self.number_selection > 10:
            return False
        if self.generation <= 0 or self.generation >= 10000:
            return False
        if self.amount_individual <= 0 or self.amount_individual >= 1000:
            return False
        return True
    
    # read node from file
    def get_data(self, file_path):
        self.reset()
        f = open(file_path, "r")
        try:
            data = f.readlines()
        except:
            print("cannot read file")
            return False
        finally:
            f.close()
        line1 = [int(x) for x in data[0].split() if x.isdigit()]
        self.n = line1[0]
        self.k = line1[1]
        self.capacity = [int(x) for x in data[1].split() if x.isdigit()]
        for i in range(self.n):
            line = data[i + 2]
            arr = [int(x) for x in line.split() if x.isdigit()]
            self.node.append(Activity(label=i+1, k=self.k, duration=arr[0], 
                resource=arr[1:(1+self.k)], s=arr[self.k+1], successor=arr[(self.k+2):]))
        
        # determine pre of node
        for i in range(self.n):
            for succ in self.node[i].successor:
                self.node[succ - 1].pre.append(i + 1) # succ-1 and i+1 because index from 0 and node from 1

    # caculate makespan of activity list
    def makespan(self, topo):
        capacity = self.capacity.copy()
        makespan = 0
        i = 0 # index of activity will do at next time
        done = 0 # number of complete activity
        doing = [] # list of activity that doing
        while done < self.n:
            if i < self.n:
                can = True # true if enough resource for activity

                # allocate resource for activity
                resource = self.node[topo[i] - 1].resource
                for j in range(self.k):
                    if resource[j] > capacity[j]:
                        can = False

                # check if pre activity done
                for j in self.node[topo[i] - 1].pre:
                    if j in doing:
                        can = False

                if can: # if true append activity to doing activity
                    for j in range(self.k):
                        capacity[j] -= resource[j]
                    self.node[topo[i] - 1].finish = makespan + self.node[topo[i] - 1].duration
                    doing.append(topo[i])
                    # print(self.node[topo[i] - 1].finish)
                    i += 1
                    continue
            min_finish = sys.maxsize
            index = 0 # lable of finish activity
            # select early done activity in doing
            for k in doing:
                if self.node[k - 1].finish < min_finish:
                    index = k
                    min_finish = self.node[k - 1].finish
            doing.remove(index)
            makespan = min_finish
            resource = self.node[index - 1].resource
            for j in range(self.k):
                capacity[j] += resource[j]
            done += 1

        return makespan
        
    def test(self):
        topo = [1, 3, 4, 2, 13, 18, 10, 8, 15, 11, 9, 19, 16, 12, 14, 
            26, 29, 5, 17, 7, 20, 27, 22, 23, 21, 6, 28, 24, 25, 30, 31, 32]
        print(self.fitness(topo))
        sys.exit()

    def setMethod(self):
        listSelect = {"tournament": self.population.tournament, "minAff": self.population.selection_min_affinity}
        list_initial = {"random": self.population.randomCreatePopulation, "priority": self.population.priority_create_population}
        self.cross_method = self.population.cross
        self.mution_method = self.population.onePointMution
        self.selection_method = listSelect[self.selection]
        self.initial_method = list_initial[self.initial]

    # GA loop
    def run_GA(self):
        # self.test()
        if not self.check_param():
            print('invalid param')
            return None
        self.setMethod()

        cur_generation = 0
        self.population.reset()
        self.best_solution = None
        self.best_cost = sys.maxsize

        # initial population
        self.population.setNode(self.node)
        self.initial_method(self.amount_individual)     # create population
        while True:
            cur_generation += 1     # loop travel every generation
            self.population.assess(fitness=self.makespan)
            solution = self.population.best_solution()
            cost = self.population.get_best_cost()
            if cost < self.best_cost:
                self.best_solution = solution
                self.best_cost = cost
            # print("best cost: ", self.best_cost, end=" ")
            # print("best current cost: ", cost)
            if cur_generation > self.generation:
                break
            self.selection_method(self.number_selection)
            self.cross_method(self.pCross)
            if self.partialOptimize:
                self.population.partialOpimize()
            if self.localSearch:
                self.population.localSearch()
            self.mution_method(self.pMution)
            
        # print("-------------------------------")
        if self.best_solution is None:
            print("Cannot find solution")
        else:
            # print('Solution is:')
            # print(self.best_solution)
            # print("Makespan is: ", self.best_cost)
            return self.best_cost, self.best_solution

        # print("------------End-----------")
