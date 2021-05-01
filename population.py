from individual import Individual
from activity import Activity
import random
import sys

class Population:
    def __init__(self, nodes=[], individuals=[]):
        self.individuals = individuals # list of individual
        self.nodes = nodes # list of node
        self.n = 0
        self.best_cost = sys.maxsize
        self.best_individual = None
        self.assessed = False

    # create initial population
    def createPopulation(self, amount):
        self.n = 0
        if amount // 2 == 1:
            amount += 1
        print("creating initial population...")
        while self.n < amount:
            self.n += 1
            self.createIndividual()
    
    def printIndividual(self, index):
        print(self.individuals[index].topo)

    def printPopulation(self):
        for i in range(self.n):
            self.printIndividual(i)

    # return node that has max value from set
    def priorityNode(self, adj):
        i = random.randint(0, len(adj)-1)
        return adj[i]

    def createIndividual(self):
        complete = [] # list of complete activity
        adj = [1] # list of activity that can work
        while len(adj) > 0:
            cur_node = self.priorityNode(adj)
            complete.append(cur_node)
            adj.remove(cur_node)
            # update adj
            for x in self.nodes[cur_node - 1].successor:
                schedule = True
                # add node if all predecessor is browsed
                for y in self.nodes[x - 1].pre:
                    if y not in complete:
                        schedule = False
                if schedule:
                    adj.append(x)
        if len(complete) < len(self.nodes):
            print("cannot complete sheduled")
        else:
            self.individuals.append(Individual(complete))

    # assess population by fitness
    def assess(self, fitness):
        for indiv in self.individuals:
            indiv.fitness = fitness(indiv.topo)
            if indiv.fitness < self.best_cost:
                self.best_cost = indiv.fitness
                self.best_individual = indiv
        self.assessed = True

    def compare(self, e):
        return e.fitness

    # @param p that is probability selection
    # using tournament selection operator
    def selection(self, p):
        k = int(self.n*p)
        if not self.assessed:
            print("not assess")
            sys.exit()
        self.individuals.sort(key=self.compare)
        new_population = []
        temp = [x for x in range(self.n)]
        for i in range(self.n):
            tour = random.choices(temp, k=5)
            chose = min(tour)
            new_population.append(self.individuals[chose])
        self.individuals = new_population

    def cross(self, p):
        for i in range(int(self.n/2)):
            if random.random() > p:
                continue
            first = 2*i
            second = 2*i + 1
            start = random.randint(0, self.n - 2)
            end = random.randint(start, self.n - 1)
            dad = self.individuals[first].topo.copy()
            mom = self.individuals[second].topo.copy()
            new_start = start
            for h in dad:
                if new_start > end:
                    break
                if h in mom[start : end + 1]:
                    self.individuals[second].topo[new_start] = h
                    new_start += 1

            new_start = start
            for k in mom:
                if new_start > end:
                    break
                if k in dad[start : end + 1]:
                    self.individuals[first].topo[new_start] = k
                    new_start += 1

    def mution(self, p):
        for i in range(self.n):
            temp = random.random()
            if temp < p:
                self.individuals[i].mution(self.nodes)

    # return topology
    def best_solution(self):
        if not self.assessed:
            print('not assess')
            return None
        return self.best_individual.topo

    # return makespan
    def get_best_cost(self):
        if not self.assessed:
            print('not assess')
            return -1
        return self.best_cost

    # set list of node
    def setNode(self, nodes):
        self.nodes = nodes