import datetime
import time
from threading import Thread
from tkinter import *
from tkinter.messagebox import *

from mine_sweeper.controller.ui_controller import UiController
from mine_sweeper.controller.ai_controller import AiController
from mine_sweeper.controller.game_board import GameBoard
from mine_sweeper.view.colors import colors
from mine_sweeper.model.node import Node


class Board:
    def __init__(self, master: Tk, size: (int, int), game_board: GameBoard, is_ai=False):
        # Initialize the UI
        self.master = master
        self.size = size
        self.game_board = game_board
        self.first_click = True
        # zero indicates unsolved
        # 1 win and -1 lose
        self.game_state = 0
        frame = Frame(self.master)
        self.is_ai = is_ai
        # Make the window responsive
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Grid.rowconfigure(master, 0, weight=1)
        Grid.rowconfigure(frame, 0, minsize=60, weight=1)
        Grid.columnconfigure(master, 0, weight=1)

        # Initialize the core variables
        self.flags = 0  # The number of flags
        self.boxes = []  # A list that contain all of the boxes
        self.clickedNodes = []  # Contains the clicked nodes (helps checking for victory)
        self.clicks = 0  # Number of clicks to check for victory
        self.mines = round(
            (self.size[0] * self.size[1]) * (10 / 64))  # The number of mines, Identified by the game size

        # Initialize the timer
        self.start_time = time
        self.timer = "00:00"
        self.update_timer_id = 0

        # Initialize the timer label
        self.timerLBL = Label(frame, text="Time: " + self.timer, font=("Helvetica", 16))
        self.timerLBL.grid(column=0, row=0, sticky=N + S + E + W, columnspan=int(self.size[1] / 2))

        # Initialize the flag-mines label
        self.minesLBL = Label(frame, font=("Helvetica", 16),
                              text="Mines left: " + str(self.flags) + "/" + str(self.mines))
        self.minesLBL.grid(column=int(self.size[1] / 2), row=0, sticky=N + S + E + W, columnspan=int(self.size[1] / 2))

        # get graph nodes
        # Create boxes upon the game size
        for x in range(self.size[0]):
            Grid.rowconfigure(frame, x + 1, weight=1)
            for y in range(self.size[1]):
                i = len(self.boxes)
                Grid.columnconfigure(frame, y, weight=1)
                self.boxes.append({
                    "button": Button(frame, font='TkDefaultFont 20 bold', text=" ", bg="darkgrey"),
                    "isFlagged": False
                })
                # Lay the boxes on the board
                self.boxes[i]['button'].grid(row=x + 1, column=y, sticky=N + S + E + W)
        if is_ai:
            self.controller = AiController(game_board,
                                           self.open_box,
                                           self.highlight,
                                           self.highlight_sec,
                                           self.add_flag)
        else:
            self.controller = UiController(game_board,
                                           self.boxes,
                                           self.open_box,
                                           self.add_flag)

    def open_box(self, node):
        if self.first_click:
            self.first_click = False
            self.start_time = time.time()
            self.update_timer()

        # TODO belal
        changed_nodes = self.game_board.discover(node)

        if node.node_data.mine:
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    value = self.game_board.get_graph_nodes_as_list()[x][y]
                    self.game_board.discover(value)
                    index = value.pos[0] * self.size[1] + value.pos[1]
                    if value.node_data.mine:
                        if value == node:
                            self.boxes[index]['button'].configure(text="*", fg="red", bg="lightgrey")
                        else:
                            if not self.boxes[index]['isFlagged']:
                                self.boxes[index]['button'].configure(text="*", fg="black")
                    else:
                        if self.boxes[index]['isFlagged']:
                            self.boxes[index]['button'].configure(fg="red")

            ai_thread = Thread(target=self.gameover, args=())
            ai_thread.start()
        elif node.node_data.weight >= 0:
            for changed_node in changed_nodes:
                weight = changed_node.node_data.weight
                if weight == 0:
                    weight = ' '
                index = changed_node.pos[0] * self.size[1] + changed_node.pos[1]
                self.boxes[index]['button'].configure(text=weight, bg="lightgrey", fg=colors[weight])
                if not self.is_ai:
                    self.boxes[index]['button'].unbind('<Button-1>')
                    self.boxes[index]['button'].unbind('<Button-3>')
                if changed_node not in self.clickedNodes:
                    self.clickedNodes.append(changed_node)
                    self.clicks += 1

            # Check for victory
            if self.clicks == (self.size[0] * self.size[1] - self.mines):
                ai_thread = Thread(target=self.victory, args=())
                ai_thread.start()
        return changed_nodes

    def add_flag(self, node):
        index = node.pos[0] * self.size[1] + node.pos[1]
        # If this box not left clicked, mark it as a flag
        if not self.boxes[index]['isFlagged']:
            self.boxes[index]['button'].configure(text="F")
            self.boxes[index]['isFlagged'] = True
            self.boxes[index]['button'].unbind('<Button-1>')
            self.flags += 1
        # If this box is flagged, unflag
        elif self.boxes[index]['isFlagged']:
            self.boxes[index]['button'].configure(text=" ")
            self.boxes[index]['isFlagged'] = False
            if not self.is_ai:
                self.boxes[index]['button'].bind('<Button-1>', self.controller.lclick_wrapper(node.pos[0], node.pos[1]))
            self.flags -= 1

        # Update the flags count
        self.minesLBL.configure(text="Mines left: " + str(self.flags) + "/" + str(self.mines))

    def update_timer(self):
        timer = time.time() - self.start_time
        self.timer = datetime.datetime.fromtimestamp(timer).strftime('%M:%S')
        self.timerLBL.configure(text="Time: " + self.timer)
        self.update_timer_id = self.master.after(1000, self.update_timer)

    # Show the player that he lose!
    def gameover(self):
        self.master.after_cancel(self.update_timer_id)
        self.game_state = -1
        self.controller.wait_till_ai_finish()
        showinfo("Game Over", "You Lose!")
        answer = askquestion("Play again?", "Do you want to play again?")
        if answer == "yes":
            self.__init__(self.master, self.size, self.game_board, self.is_ai)
        else:
            # self.master.destroy()
            sys.exit(0)

    # Show the player that he won!
    def victory(self):
        self.game_state = 1
        self.controller.wait_till_ai_finish()
        self.master.after_cancel(self.update_timer_id)
        showinfo("Victory!", "You Win!")

        try:
            score = open("score.txt", "r")
        except:
            open("score.txt", "w").close()
            score = open("score.txt", "r")

        scores = score.readlines()
        scores.append(self.timer + '\n')
        scores.sort()

        score.close()
        score = open("score.txt", "w")
        score.writelines(scores)
        score.close()
        s = ''.join(scores)
        showinfo("Score", "Your time was: " + self.timer + '\nScores Board:\n' + s)

        answer = askquestion("Play again?", "Do you want to play again?")
        if answer == "yes":
            self.__init__(self.master, self.size, self.game_board, self.is_ai)
        else:
            # self.master.destroy()
            sys.exit(0)

    def highlight(self, node):
        index = node.pos[0] * self.size[1] + node.pos[1]
        self.boxes[index]['button'].configure(bg="yellow")

    def highlight_sec(self, node):
        index = node.pos[0] * self.size[1] + node.pos[1]
        self.boxes[index]['button'].configure(bg="green")
