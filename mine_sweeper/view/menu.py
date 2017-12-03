from tkinter import *

from PIL import ImageTk, Image

from mine_sweeper.controller.ai_controller import *
from mine_sweeper.controller.ui_controller import *
from mine_sweeper.view.board import Board


class Menu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.frame = Frame(self.master)

        self.image = Image.open('resources/13950123000568_PhotoI.jpg')
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self.frame, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        self.widthLbl = Label(self.background, text='Width: ')
        self.widthLbl.pack()
        self.widthEntry = Entry(self.background)
        self.widthEntry.pack()

        self.heightLbl = Label(self.background, text='Height: ')
        self.heightLbl.pack()
        self.heightEntry = Entry(self.background)
        self.heightEntry.pack()

        self.AIBtn = Button(self.background, text='AI Controller', command=lambda: self.invokeBoard(AiController))
        self.AIBtn.pack()
        self.MouseBtn = Button(self.background, text='Mouse Controller', command=lambda: self.invokeBoard(UiController))
        self.MouseBtn.pack()

        self.frame.pack(fill=BOTH, expand=YES)

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

    def invokeBoard(self, controller):
        try:
            width = int(self.widthEntry.get())
            height = int(self.heightEntry.get())
        except:
            width = 8
            height = 8

        self.frame.destroy()
        game_board = GameBoard.get_instance()
        game_board.generateInitialState(height,width)
        Board(self.master, (width, height), game_board, controller)
