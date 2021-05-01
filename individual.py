import random
class Individual:
    def __init__(self, topo=[]):
        self.topo = topo
        self.fitness = 0

    def mution(self, nodes):
        start = random.randint(0, len(self.topo) - 1)
        end = start + 1
        succ = nodes[start].successor.copy()
        while end < len(self.topo):
            if self.topo[end] in succ:
                break
            succ.extend(nodes[end].successor)
            end += 1
        temp = random.randint(start, end - 1)
        self.topo[start], self.topo[temp] = self.topo[temp], self.topo[start]

    def cross(self, p, gen):
        pass
