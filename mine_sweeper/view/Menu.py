from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from mine_sweeper.view.Board import Board
from mine_sweeper.GameBoard import GameBoard
from mine_sweeper.controller.AiController import *
from mine_sweeper.controller.MouseController import *


class Menu:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        '''root.geometry('640x640')
            #resizing background to be responsive
            def resize_image(event):
                new_width = event.width
                new_height = event.height
                image = copy_of_image.resize((new_width, new_height))
                photo = ImageTk.PhotoImage(image)
                label.config(image=photo)
                label.image = photo  # avoid garbage collection


            image = Image.open('resources/13950123000568_PhotoI.jpg')
            copy_of_image = image.copy()
            photo = ImageTk.PhotoImage(image)
            label = ttk.Label(root, image=photo)
            label.bind('<Configure>', resize_image)
            label.pack(fill=BOTH, expand=YES)
            Board(root,(8, 8),game_board)'''

        self.widthLbl = Label(self.frame, text='Width: ')
        self.widthLbl.pack()
        self.widthEntry = Entry(self.frame)
        self.widthEntry.pack()

        self.heightLbl = Label(self.frame, text='Height: ')
        self.heightLbl.pack()
        self.heightEntry = Entry(self.frame)
        self.heightEntry.pack()

        self.AIBtn = Button(self.frame, text='AI Controller', command=lambda: self.invokeBoard(AiController))
        self.AIBtn.pack()
        self.MouseBtn = Button(self.frame, text='Mouse Controller', command=lambda: self.invokeBoard(MouseController))
        self.MouseBtn.pack()

        self.frame.pack()

    def invokeBoard(self, controller):
        try:
            width = int(self.widthEntry.get())
            height = int(self.heightEntry.get())
        except:
            width = 8
            height = 8

        self.frame.destroy()
        game_board = GameBoard.get_instance()
        Board(self.master, (width, height), game_board, controller)
