from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from board import Board   # ✅ 改成從 board.py import
import random

TEST_MODE = False

app = FastAPI()
board = Board()

class GameIn(BaseModel):
    player: str
    action: str  # "place" or "move"
    pos: str = None
    from_pos: str = None

@app.get("/")
def root():
    return {"message": "TicTacToe API is running"}

@app.post("/game")
def game(game_in: GameIn):
    try:
        player = game_in.player.upper()
        if game_in.action == "place":
            if not TEST_MODE and player != board.turn:
                raise HTTPException(status_code=400, detail="不是你的回合")
            success, msg = board.place_piece(game_in.pos, player)
        elif game_in.action == "move":
            if not TEST_MODE and player != board.turn:
                raise HTTPException(status_code=400, detail="不是你的回合")
            if not game_in.from_pos or not game_in.pos:
                raise HTTPException(status_code=400, detail="move 動作需要提供 from_pos 和 pos")
            success, msg = board.move_piece(game_in.pos, player, game_in.from_pos)
        else:
            raise HTTPException(status_code=400, detail="無效的動作，必須是 place 或 move")

        # 確保 winner 狀態即時更新
        board.is_winner("X")
        board.is_winner("O")

        result = {
            "success": success,
            "message": msg,
            "board": board.render(),
            "board_str": board.render_string(),
            "winner": board.winner,
            "turn": board.turn,
        }

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="伺服器內部錯誤，請稍後再試")

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