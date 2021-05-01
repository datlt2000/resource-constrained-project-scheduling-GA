class Activity:
    def __init__(self, label, duration=0, k=0, resource=[], s=0, successor=[]):
        self.duration = duration
        self.label = label
        self.k = k  # number of resource
        self.resource = resource # list of resource size
        self.s = s # number of successor
        self.successor = successor # label of successor
        self.finish = 0
        self.pre = []
