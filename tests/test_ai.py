# test_ai.py
from app.core.board import Board
from app.core.ai import ai_move

def test_ai_move():
    board = Board()
    from_pos, to_pos, msg = ai_move(board, "X")
    print("AI move:", from_pos, "->", to_pos, msg)

    assert to_pos is not None

    # 真的執行動作
    if from_pos is None:
        success, _ = board.place_piece(to_pos, "X")
    else:
        success, _ = board.move_piece(to_pos, "X", from_pos)

    assert success
    assert board.get_board_state()[to_pos] == "X"