import random
class Individual:
    def __init__(self, topo=[]):
        self.topo = topo
        self.fitness = 0

    def twoPointMution(self, nodes):
        start = random.randint(1, len(self.topo) - 3)
        end = start + 1
        succ = nodes[self.topo[start] - 1].successor.copy()
        while end < len(self.topo) - 1:
            if self.topo[end] in succ:
                break
            succ.extend(nodes[self.topo[end] - 1].successor)
            end += 1
        temp = random.randint(start, end - 1)
        self.topo[start], self.topo[temp] = self.topo[temp], self.topo[start]
    
    def onePointMution(self, nodes):
        start = random.randint(1, len(self.topo) - 3)
        end = start + 1
        succ = nodes[self.topo[start] - 1].successor.copy()
        while end < len(self.topo) - 1:
            if self.topo[end] in succ:
                break
            end += 1
        temp = random.randint(start, end - 1)
        a = self.topo[start]
        for i in range(start, temp):
            self.topo[i] = self.topo[i+1]
        self.topo[temp] = a

    def cross(self, p, gen):
        pass
