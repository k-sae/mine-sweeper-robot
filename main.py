import getopt
from tkinter import *
from mine_sweeper.view.menu import Menu
from mine_sweeper.controller.ai_controller import AiController
from mine_sweeper.view.board import Board
from mine_sweeper.controller.game_board import GameBoard
7

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
    #controller.start_ai_solver()
    #controller.wait_till_ai_finish()
    root = Tk()
    root.minsize(640, 640)
    if len(sys.argv) > 1:
        try:
            # short command: python main.py -c ai -s 8,8
            # long command: python main.py --controller=ai --size=8,8
            opts, args = getopt.getopt(sys.argv[1:], "c:s:", ["controller=", "size="])
        except getopt.GetoptError:
            print('INVALID ARGUMENT')
            sys.exit(2)
        is_ai = False
        size = (8, 8)
        for opt, arg in opts:
            if opt in ("-c", "--controller"):
                if arg.lower() == 'ai':
                    is_ai = True
            elif opt in ("-s", "--size"):
                try:
                    size = eval(arg)
                    if size[0] < 4:
                        size = (4, size[1])
                    if size[1] < 4:
                        size = (size[0], 4)
                except:
                    pass

        game_board = GameBoard.get_instance()
        game_board.generate_initial_state(size[1], size[0])
        Board(root, size, game_board, is_ai)

    else:
        Menu(root)

    root.mainloop()
