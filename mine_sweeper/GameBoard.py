from mine_sweeper.singleton import Singleton


@Singleton
class GameBoard:
    def __init__(self):
        # init graph here
        self.__gameState = []
        self.currentState = []
        pass

    def discover(self, node) -> bool:
        pass
