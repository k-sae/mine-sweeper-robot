from mine_sweeper.controller.game_board import GameBoard


class UiController:
    def __init__(self, game_board: GameBoard):
        self.game_board = game_board