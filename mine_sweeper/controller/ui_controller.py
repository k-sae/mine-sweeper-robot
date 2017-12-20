from mine_sweeper.controller.game_board import GameBoard


class UiController:
    def __init__(self, game_board: GameBoard, boxes
                 , discover_call_back
                 , add_flag_call_call_back):

        self.game_board = game_board
        self.boxes = boxes
        self.discover_call_back = discover_call_back
        self.add_flag_call_call_back = add_flag_call_call_back

        self.bind_boxes()

    def bind_boxes(self):
        for x in range(self.game_board.row):
            for y in range(self.game_board.col):
                i = x * self.game_board.col + y
                self.boxes[i]['button'].bind('<Button-1>', self.lclick_wrapper(x, y))
                self.boxes[i]['button'].bind('<Button-3>', self.rclick_wrapper(x, y))

    def lclick_wrapper(self, x: int, y: int):
        node = self.game_board.get_graph_nodes_as_list()[x][y]
        return lambda Button: self.discover_call_back(node)

    def rclick_wrapper(self, x: int, y: int):
        node = self.game_board.get_graph_nodes_as_list()[x][y]
        return lambda Button: self.add_flag_call_call_back(node)

    def wait_till_ai_finish(self):
        pass
