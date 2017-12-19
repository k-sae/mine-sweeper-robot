from tkinter import *
from mine_sweeper.view.menu import Menu

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
    root = Tk()
    root.minsize(640, 640)
    Menu(root)
    root.mainloop()
