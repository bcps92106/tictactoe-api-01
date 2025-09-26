from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections import deque
import random

class Board:
    def __init__(self):
        # 3x3 棋盤（空白代表無棋）
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
        # 記錄每位玩家下子的順序（最舊→最新）
        self.moves = {"O": deque(), "X": deque()}
        self.max_pieces = 4
        self.winner = None
        self.turn = "X"  # 玩家先手

    # --- 工具函式 ---
    def _pos_to_xy(self, pos: str):
        mapping = {"a": 0, "b": 1, "c": 2}
        if not isinstance(pos, str) or len(pos) != 2:
            raise ValueError("無效的位置，必須是 a1 ~ c3")
        x = mapping.get(pos[0].lower())
        try:
            y = int(pos[1]) - 1
        except Exception:
            y = None
        if x is None or y not in {0, 1, 2}:
            raise ValueError("無效的位置，必須是 a1 ~ c3")
        return x, y

    def _xy_to_pos(self, x: int, y: int) -> str:
        return "abc"[x] + str(y + 1)

    # --- 規則：place / move ---
    def place(self, player: str, pos: str):
        player = player.upper()
        if self.winner:
            return False, "遊戲已結束"
        if player not in ("X", "O"):
            raise ValueError("player 必須是 'X' 或 'O'")
        if player != self.turn:
            return False, f"現在是 {self.turn} 的回合"
        if len(self.moves[player]) >= self.max_pieces:
            return False, "你已有 4 顆棋子，請改用 move（移動最舊的棋子）"
        x, y = self._pos_to_xy(pos)
        if self.grid[y][x] != " ":
            return False, "這個位置已經有棋子"
        self.grid[y][x] = player
        self.moves[player].append(pos)
        self._check_winner()
        if not self.winner:
            self.turn = "O" if player == "X" else "X"
        return True, f"{player} 放到 {pos}"

    def move(self, player: str, new_pos: str):
        player = player.upper()
        if self.winner:
            return False, "遊戲已結束"
        if player not in ("X", "O"):
            raise ValueError("player 必須是 'X' 或 'O'")
        if player != self.turn:
            return False, f"現在是 {self.turn} 的回合"
        # 未達 4 子不得移動
        if len(self.moves[player]) < self.max_pieces:
            return False, "還沒到需要移動的階段（該玩家未滿 4 子）"
        tx, ty = self._pos_to_xy(new_pos)
        if self.grid[ty][tx] != " ":
            return False, "這個位置已經有棋子"
        # 取出最舊的棋子→清空→放到新位置
        old_pos = self.moves[player].popleft()
        ox, oy = self._pos_to_xy(old_pos)
        self.grid[oy][ox] = " "
        self.grid[ty][tx] = player
        self.moves[player].append(new_pos)
        self._check_winner()
        if not self.winner:
            self.turn = "O" if player == "X" else "X"
        return True, f"{player} 把 {old_pos} 移到 {new_pos}"

    # --- AI 行動（固定 O） ---
    def ai_move(self):
        player = "O"
        if self.winner:
            return False, "遊戲已結束"
        if self.turn != player:
            return False, f"現在不是 {player} 的回合"

        # 可落子位置
        empty_positions = [
            self._xy_to_pos(x, y)
            for y in range(3)
            for x in range(3)
            if self.grid[y][x] == " "
        ]
        if not empty_positions:
            return False, "沒有可用位置"

        if len(self.moves[player]) < self.max_pieces:
            pos = random.choice(empty_positions)
            return self.place(player, pos)
        else:
            pos = random.choice(empty_positions)
            return self.move(player, pos)

    # --- 勝負判斷 ---
    def _check_winner(self):
        lines = []
        # 橫排
        lines.extend(self.grid)
        # 直排
        lines.extend([[self.grid[r][c] for r in range(3)] for c in range(3)])
        # 對角
        lines.append([self.grid[i][i] for i in range(3)])
        lines.append([self.grid[i][2 - i] for i in range(3)])
        for line in lines:
            if line[0] != " " and line.count(line[0]) == 3:
                self.winner = line[0]
                return

    # --- 輸出狀態 ---
    def render(self):
        state = {}
        for y in range(3):
            for x in range(3):
                pos = self._xy_to_pos(x, y)
                v = self.grid[y][x]
                state[pos] = None if v == " " else v
        return state

    def render_string(self):
        rows = []
        for y in range(3):
            row = " | ".join(self.grid[y])
            rows.append(row)
            if y < 2:
                rows.append("-" * 9)
        return "\n".join(rows)

# --- FastAPI ---
app = FastAPI()
board = Board()

class GameIn(BaseModel):
    player: str
    pos: str
    action: str  # "place" or "move"

@app.get("/")
def root():
    return {"message": "TicTacToe API is running"}

@app.post("/game")
def game(game_in: GameIn):
    try:
        player = game_in.player.upper()
        if game_in.action == "place":
            success, msg = board.place(player, game_in.pos)
        elif game_in.action == "move":
            success, msg = board.move(player, game_in.pos)
        else:
            raise HTTPException(status_code=400, detail="無效的動作，必須是 place 或 move")

        result = {
            "success": success,
            "message": msg,
            "board": board.render(),
            "board_str": board.render_string(),
            "winner": board.winner,
            "turn": board.turn,
        }

        # 若輪到 AI（O）且遊戲未結束，AI 自動下
        if success and not board.winner and board.turn == "O":
            ai_success, ai_msg = board.ai_move()
            result["ai"] = {
                "success": ai_success,
                "message": ai_msg,
                "board": board.render(),
                "board_str": board.render_string(),
                "winner": board.winner,
                "turn": board.turn,
            }
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伺服器錯誤: {e}")


# --- Reset API ---
@app.post("/reset")
def reset():
    global board
    board = Board()
    return {
        "success": True,
        "message": "遊戲已重置",
        "board": board.render(),
        "board_str": board.render_string(),
        "winner": board.winner,
        "turn": board.turn,
    }