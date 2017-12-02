from mine_sweeper.singleton import Singleton
from mine_sweeper.Graph import Graph
from mine_sweeper.Node import Node
from random import randint


@Singleton
class GameBoard:
    def __init__(self):
        # need to recive row & col numbers
        self.row = 6
        self.col = 6
        self.__gameGraph = Graph(self._getNodesConnection(self._findMinesweeperConnections(),self._initGameList()))
        self.__gameState = []
        self.currentState = []
        pass

    def discover(self, node) -> bool:
        pass

    def _findMinesweeperConnections(self):
        row=self.row
        col=self.col
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

    def _getNodesConnection(self,pairs, data):
        graphData = []
        for (r1, c1), (r2, c2) in pairs:
            pair = (data[r1][c1], data[r2][c2])
            graphData.append(pair)
        return graphData


    def _initGameList(self):
        bord = [[] for i in range(0, self.row)]
        for r in range(0, self.row):
            for c in range(0, self.col):
                node = Node()
                bord[r].append(node)
        return bord


# recive first clicked node
    def setMines(self , node :Node):
        persent = 10/64
        minesNum = round(self.row*self.col*persent)
        keys =[]
        for key in self.__gameGraph._graph:
            keys.append(key)
        while (minesNum>0):
            rand = randint(0,len(keys)-1)
            if((not self.__gameGraph.is_connected(node,keys[rand]) )and (not keys[rand].mine)):
                keys[rand].mine=True
                for node  in self.__gameGraph._graph[keys[rand]]:
                    node.weight+=1
                    minesNum-=1


    def getGraphNodesAsList(self):
        list = [[] for dump in range(0,self.row)]
        for r in range(0,self.row):
            for c in range(0,self.col):
                list[r].append(self.__gameGraph._graph.keys()[(self.row*self.col)+self.col])
