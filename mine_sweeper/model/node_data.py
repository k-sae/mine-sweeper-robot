class NodeData:
    def __init__(self, mine=False, weight=0, pos=()):
        self.mine = mine
        self.weight = weight
        self.pos = pos

    def __str__(self):
        return "weight:" + str(self.weight) + " mine: " + str(self.mine) + " pos: " + str(self.pos)
