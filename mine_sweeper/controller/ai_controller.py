from mine_sweeper.controller.game_board import GameBoard
from mine_sweeper.model.node import Node
from mine_sweeper.view.board import Board


class AiController:
    def __init__(self, board: Board):
        self.board = board
        # list holds the weighted nodes in order to traverse them later
        self.nodes_to_traverse = []
        self.nodes_to_discover = {}
        self.discover_node(int(board.size[0] / 2), int(board.size[1] / 2))
        self.start_discovering()

    def discover_node(self, x: int, y: int):
        nodes = self.board.left_click((x, y))
        for node in nodes:
            if node.node_data.weight > 0:
                self.nodes_to_traverse.append(node)

    def start_discovering(self):
        self.nodes_to_discover.clear()
        for node in self.nodes_to_traverse:
            un_discovered = []
            for neighbour in self.board.game_board.game_graph.m_graph[node]:
                if neighbour.node_data is None:
                    un_discovered.append(neighbour)

    def start_weighting(self, nodes: [], parent_weight):
        for node in nodes:
            if node in self.nodes_to_discover.keys():
                self.nodes_to_discover[node] += parent_weight / len(nodes)
            else:
                self.nodes_to_discover[node] = parent_weight / len(nodes)

    def get_the_least_weighted_node(self):
        # TODO change this
        least_item = 100
        node = None
        for key, value in self.nodes_to_discover:
            if value < least_item:
                node = key
                least_item = value