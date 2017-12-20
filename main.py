import getopt
from tkinter import *
from mine_sweeper.view.menu import Menu
from mine_sweeper.controller.ai_controller import AiController
from mine_sweeper.view.board import Board
from mine_sweeper.controller.game_board import GameBoard


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
    if len(sys.argv) > 1:
        try:
            # shorter command: python main.py -cs 8,8
            # short command: python main.py -c -s 8,8
            # long command: python main.py --console --size=8,8
            opts, args = getopt.getopt(sys.argv[1:], "cs:s:", ["console", "size="])
        except getopt.GetoptError as err:
            print('INVALID ARGUMENT\n')
            print(str(err))
            sys.exit(2)
        is_console = False
        size = (8, 8)
        for opt, arg in opts:
            if opt in ("-c", "--console"):
                is_console = True
            elif opt in ("-s", "--size"):
                try:
                    size = eval(arg)
                    if size[0] < 4:
                        size = (4, size[1])
                    if size[1] < 4:
                        size = (size[0], 4)
                except:
                    pass

        if is_console:
            game_board = GameBoard.get_instance()
            game_board.generate_initial_state(size[1], size[0])
            print(size)
            controller = AiController(game_board, GameBoard.get_instance().discover)
            controller.start_ai_solver()
            controller.wait_till_ai_finish()
            # 1 win, -1 lose
            print(game_board.game_state)
    else:
        root = Tk()
        root.minsize(640, 640)
        Menu(root)
        root.mainloop()
