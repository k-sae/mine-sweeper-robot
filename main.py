from tkinter import *
from mine_sweeper.view.menu import Menu
from mine_sweeper.controller.game_board import GameBoard
from mine_sweeper.controller.ai_controller import AiController
from mine_sweeper.model.node import Node

'''
    list of params:
    -c              : start in console mode (NO UI IS INITIALIZED) 
    -s (size)       :control the size of the board
'''

if __name__ == "__main__":
    # TODO
    # based on args
    # initialize GameBoard
    # initialize Ai_controller
    # the console version will close immediately before finishing
    # use ai_controller.wait_till_ai_finish()
    # to prevent it from closing
    # hf
    print("welcome\n")
    print("choose width / height\n")
    width=int(input("enter width:\n"))
    height=int(input("enter height:\n"))
    game_board = GameBoard.get_instance()
    game_board.generate_initial_state(height, width)
    controller = AiController(game_board ,GameBoard.get_instance().discover)
    controller.start_ai_solver()
    controller.wait_till_ai_finish()
    root = Tk()
    root.minsize(640, 640)
    Menu(root)
    root.mainloop()
