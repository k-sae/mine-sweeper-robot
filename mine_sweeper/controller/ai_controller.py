from threading import *

from mine_sweeper.controller.game_board import GameBoard
from mine_sweeper.model.node import Node
from mine_sweeper.view.board import Board
import time


class AiController:
    def __init__(self, board: Board):
        self.board = board
        # list holds the weighted nodes in order to traverse them later
        self.nodes_to_traverse = []
        self.mine_vault = []
        self.high_priority_nodes = []
        self.discover_node((int(board.size[0] / 2), int(board.size[1] / 2)))
        t = Thread(target=self.start_ui_solver, args=())
        t.start()

    def start_ui_solver(self):
        while self.board.game_state == 0:
            self.start_discovering()
            # time.sleep(0.5)

    def discover_node(self, pos):
        nodes = self.board.left_click(pos)
        for node in nodes:
            if node.node_data.weight > 0:
                self.nodes_to_traverse.append(node)

    def start_discovering(self):
        for node in self.nodes_to_traverse:
            un_discovered = []
            for neighbour in self.board.game_board.game_graph.m_graph[node]:
                if neighbour.node_data is None:
                    un_discovered.append(neighbour)
            self.start_weighting(un_discovered, node)
        self.trigger_the_high_priority_nodes()

    def trigger_the_high_priority_nodes(self):
        if len(self.high_priority_nodes) == 0:
            self.discover_rand_node()
        else:
            for node in self.high_priority_nodes:
                if node not in self.mine_vault:
                    self.discover_node(node.pos)
        self.high_priority_nodes.clear()

    def start_weighting(self, nodes: [], parent: Node):
        if len(nodes) == parent.node_data.weight:
            self.add_to_the_vault(nodes)
            for node in nodes:
                for neighbour in self.board.game_board.game_graph.m_graph[node]:
                    # self.board.highlight_sec(neighbour.pos)
                    if neighbour.node_data is not None:
                        self.back_track_nodes(neighbour)

    def back_track_nodes(self, node):
        if self.get_un_risky_weight(node) == 0:
            self.board.highlight(node.pos)
            if node in self.nodes_to_traverse:
                self.nodes_to_traverse.remove(node)
            for neighbour in self.board.game_board.game_graph.m_graph[node]:
                if neighbour.node_data is None and neighbour not in self.mine_vault:
                    self.high_priority_nodes.append(neighbour)

    def get_un_risky_weight(self, node: Node):
        count = node.node_data.weight
        for neighbour in self.board.game_board.game_graph.m_graph[node]:
            if neighbour.node_data is None and neighbour in self.mine_vault:
                count -= 1
        return count

    def add_to_the_vault(self, nodes):
        for node in nodes:
            if node not in self.mine_vault:
                self.mine_vault.append(node)
                self.board.add_flag(node.pos[0], node.pos[1])

    # TODO
    def discover_rand_node(self):
        print("choosing a random node")
        for nodes in self.board.game_board.get_graph_nodes_as_list():
            for node in nodes:
                if node.node_data is None and node not in self.mine_vault:
                    self.discover_node(node.pos)
                    return
