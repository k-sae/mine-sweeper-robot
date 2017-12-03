from mine_sweeper.model.node_data import NodeData


class Node:
    def __init__(self, node_data: NodeData = None):
        self.node_data = node_data
