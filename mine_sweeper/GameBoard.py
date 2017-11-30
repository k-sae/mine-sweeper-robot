from mine_sweeper.singleton import Singleton
from mine_sweeper.Graph import Graph
from mine_sweeper.Node import Node

@Singleton
class GameBoard:
    def __init__(self):
        # need to recive row & col numbers
        self.__gameGraph =Graph(self.getNodesConnection(self.findMinesweeperConnections(5,5),self.initGameList(5,5)))
        self.__gameState = []
        self.currentState = []
        pass

    def discover(self, node) -> bool:
        pass

    def findMinesweeperConnections(self,row, col):
        nodePairs = []
        for r in range(0, row):
            for c in range(0, col):
                current = (r, c)
                if (c + 1 < col):
                    nodePairs.append((current, (r, c + 1)))
                if (c - 1 >= 0):
                    nodePairs.append((current, (r, c - 1)))
                if (r + 1 < row):
                    nodePairs.append((current, (r + 1, c)))
                if (r - 1 >= 0):
                    nodePairs.append((current, (r - 1, c)))
                if (r - 1 >= 0 and c + 1 < col):
                    nodePairs.append((current, (r - 1, c + 1)))
                if (r - 1 >= 0 and c - 1 >= 0):
                    nodePairs.append((current, (r - 1, c - 1)))
                if (r + 1 < row and c + 1 < col):
                    nodePairs.append((current, (r + 1, c + 1)))
                if (r + 1 < row and c - 1 >= 0):
                    nodePairs.append((current, (r + 1, c - 1)))

        return nodePairs

    def getNodesConnection(self,pairs, data):
        graphData = []
        for (r1, c1), (r2, c2) in pairs:
            pair = (data[r1][c1], data[r2][c2])
            graphData.append(pair)
        return graphData


    def initGameList(self,row,col):
        bord = [[] for i in range(0, row)]
        for r in range(0, row):
            for c in range(0, col):
                node = Node()
                node.pos = str(r) + "," + str(c)
                bord[r].append(node)
                return bord



