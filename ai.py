# ai.py
import random

def ai_move(board, player):
    # 如果還沒放滿 4 子，隨機放新子
    if len(board.pieces[player]) < board.max_pieces:
        options = [i for i in range(9) if board.board[i] == ' ']
        if not options:
            return None, None, "AI 無合法位置"
        target = random.choice(options)
        return None, board.idx_to_pos(target), ""  # 回傳放的位置（無移動）
    else:
        # 放滿了 → 隨機移動現有棋子
        my_pieces = board.pieces[player]
        random.shuffle(my_pieces)  # 打亂順序
        for src in my_pieces:
            options = [i for i in range(9) if board.board[i] == ' ']
            if not options:
                continue
            dest = random.choice(options)
            return board.idx_to_pos(src), board.idx_to_pos(dest), ""
        return None, None, "AI 無法移動"
    