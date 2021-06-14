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
        self.best_individual = []
        self.assessed = False

    def reset(self):
        self.n = 0
        self.best_cost = sys.maxsize
        self.best_individual = []
        self.assessed = False
        self.individuals = []
        self.nodes = []
        
    # set list of node
    def setNode(self, nodes):
        self.nodes = nodes

    # create initial population
    def randomCreatePopulation(self, amount):
        self.n = 0
        if amount // 2 == 1:
            amount += 1
        # print("creating initial population...")
        while self.n < amount:
            self.n += 1
            self.createIndividual()
    
    # hamming measure that is number of different position
    def affinity(self, gen1, gen2):
        affin = 0
        for i in range(len(gen1)):
            if gen1[i] == gen2[i]:
                affin += 1
        return affin

    def min_affinity(self, origin):
        min_indiv = None
        min_affinity = len(self.nodes)
        for indiv in self.individuals:
            affin = self.affinity(origin.topo, indiv.topo)
            if affin < min_affinity:
                min_affinity = affin
                min_indiv = indiv
        return min_indiv

    def selection_min_affinity(self, k):
        if not self.assessed:
            print("not assess")
            sys.exit()
        self.individuals.sort(key=self.compare)
        new_population = []
        temp = [x for x in range(len(self.individuals))]
        for i in range(int(self.n/2)):
            tour = random.choices(temp, k=k)
            chose = min(tour)
            new_population.append(self.individuals[chose])
            second_individual = self.min_affinity(self.individuals[chose])
            new_population.append(second_individual)
        self.individuals = new_population
    
    
    def printIndividual(self, index):
        print(self.individuals[index].topo)

    def printPopulation(self):
        for i in range(self.n):
            self.printIndividual(i)

    # return random node from list
    def randomNode(self, adj):
        i = random.randint(0, len(adj)-1)
        return adj[i]

    def createIndividual(self):
        complete = [] # list of complete activity
        adj = [1] # list of activity that can work
        while len(adj) > 0:
            cur_node = self.randomNode(adj)
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
            print(complete)
        else:
            self.individuals.append(Individual(complete))

    # assess population by fitness
    def assess(self, fitness):
        self.best_cost = 10000
        for indiv in self.individuals:
            indiv.fitness = fitness(indiv.topo)
            if indiv.fitness < self.best_cost:
                self.best_cost = indiv.fitness
                self.best_individual = indiv.topo.copy()
        self.assessed = True

    def compare(self, e):
        return e.fitness

    # @param p that is probability selection
    # using tournament selection operator
    def tournament(self, k):
        if not self.assessed:
            print("not assess")
            sys.exit()
        self.individuals.sort(key=self.compare)
        new_population = []
        temp = [x for x in range(len(self.individuals))]
        for i in range(self.n):
            tour = random.choices(temp, k=k)
            chose = min(tour) # min index is min fitness because individual is sorted by finess
            new_population.append(self.individuals[chose])
        self.individuals = new_population

    def cross(self, p):
        for i in range(int(self.n/2)):
            if random.random() > p:
                continue
            first = 2*i #index of first gen
            second = 2*i + 1 # index of second gen
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
            self.individuals.append(Individual(dad))
            self.individuals.append(Individual(mom))

    def twoPointMution(self, p):
        for i in range(self.n):
            temp = random.random()
            if temp < p:
                self.individuals[i].twoPointMution(self.nodes)

    def onePointMution(self, p):
        for i in range(self.n):
            temp = random.random()
            if temp < p:
                self.individuals[i].onePointMution(self.nodes)

    # return topology
    def best_solution(self):
        if not self.assessed:
            print('not assess')
            return None
        return self.best_individual

    # return makespan
    def get_best_cost(self):
        if not self.assessed:
            print('not assess')
            return -1
        return self.best_cost

    def priority_create_population(self, amount):
        self.n = 0
        if amount // 2 == 1:
            amount += 1
        # print("creating initial population...")
        rule = ["SPT", "LPT", "MIS", "MAS", "SR", "LR", "SSR", "LSR"]
        listRule = {"SPT": self.spt, "LPT": self.lpt, "MIS": self.mis, "MAS": self.mas, "SR": self.sr, "LR": self.lr, "SSR": self.ssr, "LSR": self.lsr}
        '''
            SPT: min duration
            LPT: max duration
            MAS: max sussessor
            MIS: min sussessor
            SR: min max resource
            LR: max max resource
            SSR: Max sum resource
            LSR: Min sun rsource
        '''
        while self.n < amount:
            self.n += 1
            if self.n < 8:
                self.createPriorityIndividual(listRule[rule[self.n]])
            else:
                self.createIndividual()
    

    def createPriorityIndividual(self, rule):
        complete = [] # list of complete activity
        adj = [1] # list of activity that can work
        while len(adj) > 0:
            cur_node = rule(adj)
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
    
    # return node has min duration
    def spt(self, adj):
        minValue = self.nodes[adj[0] - 1].duration
        node = adj[0]
        for i in adj:
            if minValue > self.nodes[i - 1].duration:
                node = i
                minValue = self.nodes[i - 1].duration
        return node
    
    # return node has max duration
    def lpt(self, adj):
        maxValue = self.nodes[adj[0] - 1].duration
        node = adj[0]
        for i in adj:
            if maxValue < self.nodes[i - 1].duration:
                node = i
                maxValue = self.nodes[i- 1].duration
        return node

    # return node has max successor
    def mas(self, adj):
        maxValue = len(self.nodes[adj[0] - 1].successor)
        node = adj[0]
        for i in adj:
            if maxValue < len(self.nodes[i - 1].successor):
                node = i
                maxValue = len(self.nodes[i - 1].successor)
        return node

    # return node has min successor
    def mis(self, adj):
        minValue = len(self.nodes[adj[0] - 1].successor)
        node = adj[0]
        for i in adj:
            if minValue < len(self.nodes[i - 1].successor):
                node = i
                minValue = len(self.nodes[i - 1].successor)
        return node

    # return node has min max resource
    def sr(self, adj):
        minValue = max(self.nodes[adj[0] - 1].resource)
        node = adj[0]
        for i in adj:
            if minValue > max(self.nodes[i - 1].resource):
                node = i
                minValue = max(self.nodes[i - 1].resource)
        return node

    # return node has max max resource
    def lr(self, adj):
        maxValue = max(self.nodes[adj[0] - 1].resource)
        node = adj[0]
        for i in adj:
            if maxValue < max(self.nodes[i - 1].resource):
                node = i
                maxValue = max(self.nodes[i - 1].resource)
        return node

    # return node has max sum resource
    def ssr(self, adj):
        maxValue = sum(self.nodes[adj[0] - 1].resource)
        node = adj[0]
        for i in adj:
            if maxValue < sum(self.nodes[i - 1].resource):
                node = i
                maxValue = sum(self.nodes[i - 1].resource)
        return node

    # return node has min sum resource
    def lsr(self, adj):
        minValue = sum(self.nodes[adj[0] - 1].resource)
        node = adj[0]
        for i in adj:
            if minValue > sum(self.nodes[i - 1].resource):
                node = i
                minValue = sum(self.nodes[i - 1].resource)
        return node

    # select random a part of gen and sort by priority rule
    def partialOpimize(self):
        for indiv in self.individuals:
            if random.random() > 1:
                continue
            x = random.randint(1, len(self.nodes) - 3)
            y = random.randint(x + 2, len(self.nodes) - 1)
            if y-x > 6:
                y = x + 6
            nodes = indiv.topo[x:y].copy()  # list node need to sort
            listRule = [self.spt, self.lpt, self.mis, self.mas, self.sr, self.lr, self.ssr, self.lsr]
            adj = []
            # select node that dont have pre in nodes
            for node in nodes:
                pre = False
                for p in self.nodes[node - 1].pre:
                    if p in nodes:
                        pre = True
                if not pre:
                    adj.append(node)
            complete = []
            i = x
            while len(adj) > 0:
                rule = random.randint(0, 7) # rule for sort
                curNode = listRule[rule](adj)
                indiv.topo[i] = curNode
                i += 1
                complete.append(curNode)
                adj.remove(curNode)
                # update node that have pre node done
                for succ in self.nodes[curNode - 1].successor:
                    schedule = True
                    # add node if all predecessor is browsed
                    if succ not in nodes:
                        continue
                    for pre in self.nodes[succ - 1].pre:
                        if pre not in complete and pre in nodes:
                            schedule = False
                    if schedule:
                        adj.append(succ)

    def preLast(self, adj, topo):
        pre_last = len(self.nodes)
        select_node = 0
        for node in adj:
            pre_node = len(self.nodes)
            for i in range(len(topo)):
                if topo[i] in self.nodes[node-1].pre:
                    pre_node = i
            if pre_last >= pre_node:
                pre_last = pre_node
                select_node = node
        return select_node


    def localSearch(self):
        for indiv in self.individuals:
            if random.random() > 0.05:
                continue
            x = random.randint(2, len(self.nodes) - 10)
            y = x + 8
            nodes = indiv.topo[x:y].copy()  # list node need to sort
            adj = []
            # select node that dont have pre in nodes
            for node in nodes:
                pre = False
                for p in self.nodes[node - 1].pre:
                    if p in nodes:
                        pre = True
                if not pre:
                    adj.append(node)
            complete = []
            while len(adj) > 0:
                curNode = self.preLast(adj, indiv.topo)
                complete.append(curNode)
                adj.remove(curNode)
                # update node that have pre node done
                for succ in self.nodes[curNode - 1].successor:
                    schedule = True
                    # add node if all predecessor is browsed
                    if succ not in nodes:
                        continue
                    for pre in self.nodes[succ - 1].pre:
                        if pre not in complete and pre in nodes:
                            schedule = False
                    if schedule:
                        adj.append(succ)
            for i in range(x, y):
                indiv.topo[i] = complete[i-x]
    