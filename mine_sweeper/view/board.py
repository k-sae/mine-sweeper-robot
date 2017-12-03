import datetime
import time
from tkinter import *
from tkinter.messagebox import *

from mine_sweeper.controller.game_board import GameBoard


class Board:
    def __init__(self, master, size, game_board: GameBoard, controller):
        # Initialize the UI
        self.master = master
        self.master.title("Minesweeper")
        self.size = size
        self.game_board = game_board
        game_board.set_mines(game_board.get_graph_nodes_as_list()[0][0])
        self.controller = controller(self.game_board)
        frame = Frame(master)
        # Make the window responsive
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Grid.rowconfigure(master, 0, weight=1)
        Grid.rowconfigure(frame, 0, minsize=60, weight=1)
        Grid.columnconfigure(master, 0, weight=1)

        # Initialize the core variables
        self.flags = 0  # The number of flags
        self.boxes = []  # A list that contain all of the boxes
        self.mines = int((self.size[0] * self.size[1]) * 0.16)  # The number of mines, Identified by the game size

        # Initialize the timer label
        self.timerLBL = Label(frame, font=("Helvetica", 16))
        self.timerLBL.grid(column=0, row=0, sticky=N + S + E + W, columnspan=int(self.size[1] / 2))

        # Initialize the timer and update it every second
        self.start_time = time.time()
        self.update_timer()

        # Initialize the flag-mines label
        self.minesLBL = Label(frame, font=("Helvetica", 16),
                              text="Mines left: " + str(self.flags) + "/" + str(self.mines))
        self.minesLBL.grid(column=int(self.size[1] / 2), row=0, sticky=N + S + E + W, columnspan=int(self.size[1] / 2))

        # get graph nodes
        print(game_board.get_graph_nodes_as_list())
        # Create boxes upon the game size
        for x in range(self.size[0]):
            Grid.columnconfigure(frame, x, weight=1)
            for y in range(self.size[1]):
                i = len(self.boxes)
                Grid.rowconfigure(frame, y + 1, weight=1)
                self.boxes.append(Button(frame, font=('TkDefaultFont', 20), text=" ", bg="darkgrey"))
                # Lay the boxes on the board
                self.boxes[i].grid(row=x + 1, column=y, sticky=N + S + E + W)
                self.boxes[i].bind('<Button-1>', self.lclickwrapper(x, y))

    def lclickwrapper(self, x, y):
        # WARNING redundant line
        # too many useless loops
        nodes = self.game_board.get_graph_nodes_as_list()

        return lambda Button: self.update_text(nodes[x][y])

    def update_text(self, value):
        print(self.game_board.discover(value))

    def update_timer(self):
        timer = time.time() - self.start_time
        timerstr = datetime.datetime.fromtimestamp(timer).strftime('%M:%S')
        self.timerLBL.configure(text="Time: " + timerstr)
        self.master.after(1000, self.update_timer)

    # Show the player that he lose!
    def gameover(self):
        showinfo("Game Over", "You Lose!")
        answer = askquestion("Play again?", "Do you want to play again?")
        if answer == "yes":
            self.__init__(self.master, self.size)
        else:
            self.master.destroy()

    # Show the player that he won!
    def victory(self):
        showinfo("Victory!", "You Win!")
        answer = askquestion("Play again?", "Do you want to play again?")
        if answer == "yes":
            self.__init__(self.master, self.size)
        else:
            self.master.destroy()
