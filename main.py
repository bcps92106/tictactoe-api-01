from board import TicTacToe
from ai import ai_move
from speech_to_command import interpret_command

def main():
    game = TicTacToe()
    player = 'X'
    ai = 'O'

    while True:
        game.display()

        # 玩家輸入階段
        if len(game.pieces[player]) < game.max_pieces:
            # 使用語音文字模擬輸入
            text = input("請輸入語音內容（例如：放在右上）：").strip()
            result = interpret_command(text)

            if result[0] != "place":
                print("⚠️ 請使用『放在 XX』的句子，目前只能放新子")
                continue

            move = result[1]
            success, msg = game.place_piece(move, player)

        else:
            # 玩家需要移動棋子
            text = input("請輸入語音內容（例如：把 a1 移動到 c3）：").strip()
            result = interpret_command(text)

            if result[0] != "move":
                print("⚠️ 請使用『把 X 移動到 Y』的語句，目前只能移動")
                continue

            src, dst = result[1], result[2]
            success, msg = game.move_piece(src, dst, player)

        if not success:
            print("❌", msg)
            continue

        if game.is_winner(player):
            game.display()
            print("🎉 你贏了！")
            break

        # AI 回合
        src, dst, msg = ai_move(game, ai)
        if dst is None:
            print("AI 無法下棋，平手！")
            break
        if src:
            game.move_piece(src, dst, ai)
            print(f"🤖 AI 將 O 從 {src} 移動到 {dst}")
        else:
            game.place_piece(dst, ai)
            print(f"🤖 AI 在 {dst} 放下一顆 O")

        if game.is_winner(ai):
            game.display()
            print("💀 AI 贏了")
            break

        if game.is_full():
            print("棋盤滿了，平手結束")
            break

if __name__ == "__main__":
    main()
    