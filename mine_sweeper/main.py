from tkinter import *
from mine_sweeper.view.menu import Menu

if __name__ == "__main__":

    root = Tk()
    root.minsize(640, 640)
    Menu(root)
    root.mainloop()
