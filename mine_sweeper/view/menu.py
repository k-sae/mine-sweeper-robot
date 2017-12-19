from tkinter import *


from mine_sweeper.controller.ai_controller import *
from mine_sweeper.controller.ui_controller import *
from mine_sweeper.view.board import Board


class Menu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.frame = Frame(self.master)

        self.widthLbl = Label(self.frame, text='Width: ')
        self.widthLbl.grid(row=0, column=0)
        self.widthEntry = Entry(self.frame)
        self.widthEntry.grid(row=0, column=1)

        self.heightLbl = Label(self.frame, text='Height: ')
        self.heightLbl.grid(row=1, column=0)
        self.heightEntry = Entry(self.frame)
        self.heightEntry.grid(row=1, column=1)

        self.AIBtn = Button(self.frame, text='AI Controller', command=lambda: self.invoke_board(True))
        self.AIBtn.grid(row=2, column=0)
        self.MouseBtn = Button(self.frame, text='Mouse Controller', command=lambda: self.invoke_board(False))
        self.MouseBtn.grid(row=2, column=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.frame.pack(pady=250)

    def invoke_board(self, is_ai):
        try:
            width = int(self.widthEntry.get())
            height = int(self.heightEntry.get())
        except:
            width = 8
            height = 8

        if width < 4:
            width = 4

        if height < 4:
            height = 4

        self.frame.destroy()
        game_board = GameBoard.get_instance()
        game_board.generate_initial_state(height, width)
        Board(self.master, (width, height), game_board, is_ai)
