class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = {
            "a1": None, "a2": None, "a3": None,
            "b1": None, "b2": None, "b3": None,
            "c1": None, "c2": None, "c3": None,
        }
        self.turn = "X"
        self.winner = None

    def get_board_state(self):
        return self.state

    def is_valid_pos(self, pos):
        return pos in self.state

    def place(self, player, pos):
        if self.winner:
            return {"success": False, "message": "Game already ended."}
        if player != self.turn:
            return {"success": False, "message": "Not your turn."}
        if not self.is_valid_pos(pos):
            return {"success": False, "message": "Invalid position."}
        if self.state[pos] is not None:
            return {"success": False, "message": "Position already taken."}
        self.state[pos] = player
        self.check_winner()
        self.turn = "O" if self.turn == "X" else "X"
        return {"success": True, "board": self.get_board_state()}

    def move(self, player, from_pos, to_pos):
        if self.winner:
            return {"success": False, "message": "Game already ended."}
        if player != self.turn:
            return {"success": False, "message": "Not your turn."}
        if not self.is_valid_pos(from_pos) or not self.is_valid_pos(to_pos):
            return {"success": False, "message": "Invalid position."}
        if self.state[from_pos] != player:
            return {"success": False, "message": "You don't have a piece at from_pos."}
        if self.state[to_pos] is not None:
            return {"success": False, "message": "to_pos already taken."}
        self.state[from_pos] = None
        self.state[to_pos] = player
        self.check_winner()
        self.turn = "O" if self.turn == "X" else "X"
        return {"success": True, "board": self.get_board_state()}

    def check_winner(self):
        lines = [
            ["a1", "a2", "a3"],
            ["b1", "b2", "b3"],
            ["c1", "c2", "c3"],
            ["a1", "b1", "c1"],
            ["a2", "b2", "c2"],
            ["a3", "b3", "c3"],
            ["a1", "b2", "c3"],
            ["a3", "b2", "c1"],
        ]
        for line in lines:
            if self.state[line[0]] and self.state[line[0]] == self.state[line[1]] == self.state[line[2]]:
                self.winner = self.state[line[0]]
                break