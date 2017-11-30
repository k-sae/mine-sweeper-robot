from tkinter import *
from mine_sweeper.view.Board import Board
from mine_sweeper.GameBoard import GameBoard


if __name__ == "__main__":

    game_board = GameBoard.get_instance()
    root = Tk()
    root.minsize(640, 640)
    Board(root, (8, 8), game_board)
    root.mainloop()
