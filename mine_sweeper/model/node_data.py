class NodeData:
    def __init__(self, mine=False, weight=0):
        self.mine = mine
        self.weight = weight

    def __str__(self):
        return "weight:" + str(self.weight) + " mine: " + str(self.mine)