from population import Population
from const import *
import sys
from activity import Activity
"""
    class that run GA loop
    @param
            pCross {float}: cross operator probability in (0, 1)
            pMution {float}: mution operator probability in (0, 1)
            pSelection {float}: selection operator probability in (0, 1)
            generation {int}: number of loop in (0, 1000)
"""
class Environment:
    def __init__(self):
        self.method = 1 # select operator
        self.generation = 0
        self.amount_individual = 0
        self.pCross = 0
        self.pMution = 0
        self.pSelection = 0
        self.best_solution = None
        self.best_cost = sys.maxsize
        self.n = 0 # number of node
        self.k = 0 # number of resource
        self.capacity = []  # max capacity of resource
        self.node = [] # list of node

    def get_method(self):
        pass

    # get operator probability and generation
    def get_param(self, p_cross=0.9, p_mution=0.2, p_selection=0.03, generation=100, amount_individual=100):
        while p_cross <= 0 or p_cross >= 1:
            p_cross = float(input("cross probability= "))
        while p_mution <= 0 or p_mution >= 1:
            p_mution = float(input("mution probability= "))
        while p_selection <= 0 or p_selection >= 1:
            p_selection = float(input("selection probability= "))
        while generation <= 0 or generation >= 1000:
            generation = int(input('generation= '))
        while amount_individual <= 0 or amount_individual >= 1000:
            amount_individual = int(input('number of individual= '))
        self.amount_individual = amount_individual
        self.generation = generation
        self.pCross = p_cross
        self.pMution = p_mution
        self.pSelection = p_selection

    # check if param is invalid
    def check_param(self):
        if self.pCross <= 0 or self.pCross >= 1:
            return False
        if self.pMution <= 0 or self.pMution >= 1:
            return False
        if self.pSelection <= 0 or self.pSelection >= 1:
            return False
        if self.generation <= 0 or self.generation >= 1000:
            return False
        if self.amount_individual <= 0 or self.amount_individual >= 1000:
            return False
        return True
    
    # read node from file
    def get_data(self):
        f = open(FILE_PATH, "r")
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
        for i in range(len(self.node)):
            for succ in self.node[i].successor:
                self.node[succ - 1].pre.append(i + 1) # succ-1 and i+1 because index from 0 and node from 1

    # Sort topo list that is activity list begin at index 1
    def fitness(self, topo):
        capacity = self.capacity.copy()
        makespan = 0
        i = 0
        done = 0
        doing = []
        while done < self.n:
            if i < self.n:
                can = True
                resource = self.node[topo[i] - 1].resource
                for j in range(self.k):
                    if resource[j] > capacity[j]:
                        can = False
                if can:
                    for j in range(self.k):
                        capacity[j] -= resource[j]
                    self.node[topo[i] - 1].finish = makespan + self.node[topo[i] - 1].duration
                    doing.append(i)
                    i += 1
                    continue
            min_finish = sys.maxsize
            index = 0
            for k in doing:
                if self.node[topo[k] - 1].finish < min_finish:
                    index = k
                    min_finish = self.node[topo[k] - 1].finish
            doing.remove(index)
            makespan = min_finish
            for j in range(self.k):
                capacity[j] += resource[j]
            done += 1

        return makespan
            
    # GA loop
    def run_GA(self):
        self.get_method()
        self.get_param()
        self.get_data()
        if not self.check_param():
            print('invalid param')
            return None
        
        cur_generation = 0

        # initial population
        population = Population()
        population.setNode(self.node)
        population.createPopulation(self.amount_individual)     # create population
        while True:
            cur_generation += 1     # loop travel every generation
            population.assess(fitness=self.fitness)
            best_solution = population.best_solution()
            cost = population.get_best_cost()
            if cost < self.best_cost:
                self.best_solution = best_solution
                self.best_cost = cost
            print("Generation: ", cur_generation, end="\t")
            print("Best cost: ", self.best_cost, end="\t")
            print("Best current cost: ", cost, end='\n')
            if cur_generation > self.generation:
                break
            population.selection(self.pSelection)
            population.cross(self.pCross)
            population.mution(self.pMution)
            
        print("-------------------------------")
        if self.best_solution is None:
            print("Cannot find solution")
        else:
            print('Solution is:')
            print(self.best_solution)
            print("Makespan is: ", self.best_cost)
        print("------------End-----------")

