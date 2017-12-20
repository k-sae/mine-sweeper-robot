from threading import *
import operator
from mine_sweeper.controller.game_board import GameBoard
from mine_sweeper.model.node import Node

"""
    in this docs iam describing the role of each function 
    its arranged with chronological order
    start_ai_solver :
                    this start discovering game nodes starting with the middle of the board
    
    discover_node :
                    discover the node and get the interesting nodes surrounded by it 
                    by getting the return of 'discover_call_back' and add it to 'nodes_to_traverse'
                    if the node is not in the 'mine_vault
                    
    start_discovering :
                    loop through 'nodes_to_traverse' and send each node to 
                    'start_weighting'
                    
    start_weighting :
                    its role to find a node with weight equals to its neighbours this means its hundred percent a mine
                    if his node is found send it to 'back_track_nodes'
                                   
    back_track_nodes :
                    traverse the neighbours of the node to see if there is a save nodes 
                    the safe nodes are added to 'high_priority_nodes'
    
    trigger_the_high_priority_nodes:
                    it make sure that the node doesnt exist in the 'mine_vault' before passing it to 
                    'discover_node'
"""


class AiController:
    def __init__(self, game_board: GameBoard, discover_call_back,
                 discovered_nodes_highlight_call_back=None
                 , ignored_nodes_highlight_call_back=None
                 , add_flag_call_call_back=None):
        """

        :param game_board: just the game board :)
        :param discover_call_back: f(pos) -> [nodes] call back that returns the discovered nodes
        :param discovered_nodes_highlight_call_back:
        :param ignored_nodes_highlight_call_back:
        :param add_flag_call_call_back:
        """
        self.game_board = game_board
        self.discover_call_back = discover_call_back
        self.discovered_nodes_highlight_call_back = discovered_nodes_highlight_call_back
        self.ignored_nodes_highlight_call_back = ignored_nodes_highlight_call_back
        self.add_flag_call_call_back = add_flag_call_call_back

        # list holds the weighted nodes in order to traverse them later
        self.nodes_to_traverse = []
        self.nodes_weighted ={}
        # a list contain all the nodes that is hundred percent sure they are mines
        self.mine_vault = []

        # holds the nodes that are less likely to be mines
        self.high_priority_nodes = []
        self.ai_thread = Thread(target=self.start_ai_solver, args=())
        self.ai_thread.start()

    def start_ai_solver(self):
        #discover  node  in the   middel board
        self.discover_node((int(self.game_board.row / 2), int(self.game_board.col / 2)))
        while self.game_board.game_state == 0:
            self.start_discovering()
            # time.sleep(0.5)

    def discover_node(self, pos):
        #get all nodes   connect  with this  node
        nodes = self.discover_call_back(pos)
        for node in nodes:
            if node.node_data.weight > 0 and node not in self.nodes_to_traverse:
                self.nodes_to_traverse.append(node)

    def start_discovering(self):
        for node in self.nodes_to_traverse:
            un_discovered = []
            for neighbour in self.game_board.game_graph.m_graph[node]:
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
                    self.check_and_remove_weight_node(node)
                    self.discover_node(node.pos)
        self.high_priority_nodes.clear()

    def start_weighting(self, nodes: [], parent: Node):
        if len(nodes) <= parent.node_data.weight:
            self.add_to_the_vault(nodes)
            self.nodes_to_traverse.remove(parent)
            if self.ignored_nodes_highlight_call_back is not None:
                self.ignored_nodes_highlight_call_back(parent.pos)

            for node in nodes:
                self.check_and_remove_weight_node(node)
                for neighbour in self.game_board.game_graph.m_graph[node]:
                    # self.board.highlight_sec(neighbour.pos)
                    if neighbour.node_data is not None:
                        #send  node   descoverd before
                        self.back_track_nodes(neighbour)
        else:
            self.estimate(nodes,parent)
    def back_track_nodes(self, node):
        if self.get_un_risky_weight(node) == 0:
            # highlight as traversed
            if self.discovered_nodes_highlight_call_back is not None:
                self.discovered_nodes_highlight_call_back(node.pos)

            if node in self.nodes_to_traverse:
                self.nodes_to_traverse.remove(node)
                # highlight unneeded
                if self.ignored_nodes_highlight_call_back is not None:
                    self.ignored_nodes_highlight_call_back(node.pos)

            for neighbour in self.game_board.game_graph.m_graph[node]:
                if neighbour.node_data is None and neighbour not in self.mine_vault:
                    self.high_priority_nodes.append(neighbour)

        else:
            for neighbour in self.game_board.game_graph.m_graph[node]:
                if neighbour in self.nodes_weighted.keys():
                   new_weight = self.nodes_weighted[neighbour] [0] -1
                   neighbours  = self.nodes_weighted[neighbour][1]
                   self.nodes_weighted[neighbour] =(new_weight,neighbours)
    def get_un_risky_weight(self, node: Node):
        count = node.node_data.weight
        for neighbour in self.game_board.game_graph.m_graph[node]:
            if neighbour.node_data is None and neighbour in self.mine_vault:
                count -= 1
        return count

    def add_to_the_vault(self, nodes):
        for node in nodes:
            if node not in self.mine_vault:
                self.mine_vault.append(node)
                if self.add_flag_call_call_back is not None:
                    self.add_flag_call_call_back(node.pos)

    # TODO
    def discover_rand_node(self):
        #print("choosing a random node")
        print(str(self.nodes_weighted))
        if len(self.nodes_weighted )>0:
            #node = sorted(self.nodes_weighted.items(), key=operator.itemgetter(0))[0]
            node = self.choose_node()
            self.check_and_remove_weight_node(node)
            self.discover_node(node.pos)

        else:
            for nodes in self.game_board.get_graph_nodes_as_list():
                for node in nodes:
                    if node.node_data is None and node not in self.mine_vault:
                        self.check_and_remove_weight_node(node)
                        self.discover_node(node.pos)
                        return

    def wait_till_ai_finish(self):
        self.ai_thread.join()
    def estimate (self , nodes , parent):
        node_weight=self.get_un_risky_weight(parent)
        for node in nodes:
            if node not in self.nodes_weighted.keys():
                self.nodes_weighted[node] = (parent.node_data.weight,[parent])
            else:
                if  parent not in  (self.nodes_weighted[node][1]):
                  total_weight = self.nodes_weighted[node][0] + parent.node_data.weight
                  list_parent = self.nodes_weighted[node][1]
                  list_parent.append(parent)
                  self.nodes_weighted[node]= ( total_weight,list_parent)

    def check_and_remove_weight_node(self,node):
        if node in self.nodes_weighted.keys():
            self.nodes_weighted.pop(node)
    def choose_node (self,arrange=1):
        #send arrange =1 if want pick min else send -1
         m_node = None
         m_weight = 0
         for node in self.nodes_weighted.keys():
             if(m_node == None or m_weight*arrange > self.nodes_weighted[node][0]*arrange):
                 m_node = node
                 m_weight = self.nodes_weighted[node][0]

         return  m_node