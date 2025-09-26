# board.py

class TicTacToe:
    def __init__(self):
        # 初始化棋盤：9 格預設為空白
        self.board = [' ' for _ in range(9)]
        # 記錄玩家與 AI 各自的棋子位置（最多 4 個）
        self.pieces = {'X': [], 'O': []}
        self.max_pieces = 4

    def display(self):
        # 顯示棋盤畫面
        print("\n棋盤狀態：")
        for i in range(0, 9, 3):
            print(' | '.join(self.board[i:i+3]))
        print()

    def place_piece(self, pos, player):
        # 嘗試放下一枚棋子
        idx = self.pos_to_idx(pos)
        if self.board[idx] == ' ':
            # 檢查是否已達最大數量
            if len(self.pieces[player]) >= self.max_pieces:
                return False, "你已經放滿 4 子，請使用 move_piece()"
            # 放棋子
            self.board[idx] = player
            self.pieces[player].append(idx)
            return True, self.get_board_state()
        else:
            return False, "該位置已有棋子"

    def move_piece(self, to_pos, player):
        # 嘗試移動「最舊的棋子」
        if len(self.pieces[player]) < self.max_pieces:
            return False, "還沒到需要移動的階段"

        to_idx = self.pos_to_idx(to_pos)
        if self.board[to_idx] != ' ':
            return False, "目標位置不是空格"

        # 取出最舊的棋子
        from_idx = self.pieces[player].pop(0)
        self.board[from_idx] = ' '
        self.board[to_idx] = player
        self.pieces[player].append(to_idx)
        return True, self.get_board_state()

    def pos_to_idx(self, pos):
        # 棋盤位置文字 → 索引編號（0～8）
        mapping = {
            "a1": 0, "b1": 1, "c1": 2,
            "a2": 3, "b2": 4, "c2": 5,
            "a3": 6, "b3": 7, "c3": 8,
        }
        return mapping.get(pos.lower(), -1)

    def is_winner(self, player):
        # 判斷玩家是否獲勝（三連線）
        b = self.board
        lines = [
            [0,1,2], [3,4,5], [6,7,8],    # 橫
            [0,3,6], [1,4,7], [2,5,8],    # 直
            [0,4,8], [2,4,6],             # 斜
        ]
        return any(all(b[i] == player for i in line) for line in lines)

    def is_full(self):
        # 判斷棋盤是否滿了
        return all(s != ' ' for s in self.board)

    def available_positions(self):
        # 回傳所有空格的索引位置
        return [i for i, s in enumerate(self.board) if s == ' ']

    def idx_to_pos(self, idx):
        # 索引編號 → 棋盤位置文字（0→a1，8→c3）
        reverse_map = {
            0: "a1", 1: "b1", 2: "c1",
            3: "a2", 4: "b2", 5: "c2",
            6: "a3", 7: "b3", 8: "c3"
        }
        return reverse_map.get(idx, "?")

    def get_board_state(self):
        # 回傳字典，每個位置對應其棋子狀態（'X'、'O' 或 None）
        state = {}
        for idx in range(9):
            pos = self.idx_to_pos(idx)
            val = self.board[idx]
            state[pos] = val if val in ['X', 'O'] else None
        return state