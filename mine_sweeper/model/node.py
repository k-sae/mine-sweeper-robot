from mine_sweeper.model.node_data import NodeData


class Node:
    def __init__(self, node_data: NodeData = None, pos=()):
        self.node_data = node_data
        self.pos = pos

    def __str__(self):
        if self.node_data is None:
            return "none" + "pos: " + str(self.pos)
        else:
            return str(self.node_data) + "pos: " + str(self.pos)
