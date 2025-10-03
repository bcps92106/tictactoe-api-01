import whisper
import sounddevice as sd
import numpy as np
import json
import asyncio
import edge_tts
from openai import OpenAI
import tempfile
import os
import soundfile as sf
import random

from board import Board
game = Board()

# 初始化 - 從環境變數讀取 API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
whisper_model = whisper.load_model("base")  # 可改成 "small"/"medium" 提升準確率

def print_board():
    print("\n棋盤狀態：")
    for r in ["a", "b", "c"]:
        row = [game.state[f"{r}{c}"] if game.state[f"{r}{c}"] else " " for c in range(1, 4)]
        print(" | ".join(row))
        print("-" * 5)

def check_winner():
    return game.check_winner()

def reset_game():
    global game
    game = Board()
    print("🔄 新的一局開始！")
    print_board()

# 🎤 錄音 + Whisper
def record_and_recognize(duration=3, samplerate=16000):
    print("🎤 請開始說話...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    print("🛑 錄音結束，正在辨識...")

    audio = np.squeeze(audio)
    result = whisper_model.transcribe(audio, fp16=False, language="zh")
    text = result["text"].strip()
    print(f"📝 Whisper 辨識結果: {text}")
    return text

# ✨ 語音修正
def clean_command(text):
    prompt = f"""
    你是一個語音辨識修正器。
    Whisper 有時會把「下在 a1」聽成「下載 a1」，或把棋盤位置聽錯。
    請幫我把輸入修正成正確的棋步指令（a1~c3），例如：
    - 「下載 A1」→「下在 a1」
    - 「放在右上角」→「下在 a1」
    - 「移動左下到右中」→「把 c1 移動到 b2」
    如果真的聽不懂，就原封不動回傳。
    
    使用者輸入: {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "你是語音指令修正器"},
                  {"role": "user", "content": prompt}],
        temperature=0
    )
    result = response.choices[0].message.content.strip()
    # 去除重複的詞或句子
    parts = result.split()
    seen = set()
    filtered = []
    for p in parts:
        if p not in seen:
            filtered.append(p)
            seen.add(p)
    result = " ".join(filtered)
    return result

# 🤖 GPT 指令解析
def interpret_with_gpt(text):
    prompt = f"""
    請判斷這句話的棋步，棋盤是 a1~c3。
    只能回傳 JSON，不能多字：
    - {{"action": "place", "pos": "b2"}}
    - {{"action": "move", "from": "a1", "to": "c3"}}
    - {{"action": "none"}}
    使用者輸入: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "你是棋步指令解析器，只能輸出 JSON，不允許其他字。"},
                  {"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()
    print("🔍 GPT 原始回傳:", content)

    import re
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        content = match.group(0)

    try:
        data = json.loads(content)
    except Exception:
        print("❌ JSON parse 失敗:", content)
        return {"action": "none"}

    if data["action"] == "place":
        pos = data["pos"]

        if game.state[pos] is not None:
            say("該位置已經有子了，請重新選擇")
            return None

        if list(game.state.values()).count("O") >= 4:
            say("你已經下滿四子，只能移動自己的子")
            return None

        game.state[pos] = "O"
        print_board()

        say(f"你下在 {pos}")

        winner = check_winner()
        if winner:
            handle_winner(winner)
            return None  # 已在 handle_winner/say 播報，外層不要再說一次

        empty_cells = [k for k, v in game.state.items() if v is None]

        pos_choice = random.choice(empty_cells)
        if list(game.state.values()).count("X") >= 4:
            # 移除最舊的電腦子 (假設有紀錄順序，這裡沒實作，暫不移除)
            pass
        game.state[pos_choice] = "X"
        print(f"🤖 電腦落子在 {pos_choice}")
        print_board()
        say(f"我下在 {pos_choice}")

        winner = check_winner()
        if winner:
            handle_winner(winner)
            return None  # 已播報勝負

        return None  # 已在函式內說明玩家與電腦落子，外層不再重複播報

    elif data["action"] == "move":
        from_pos, to_pos = data["from"], data["to"]
        game.state[to_pos] = game.state[from_pos]
        game.state[from_pos] = None
        print_board()

        say(f"你把 {from_pos} 移動到 {to_pos}")

        winner = check_winner()
        if winner:
            handle_winner(winner)
            return None  # 已播報

        empty_cells = [k for k, v in game.state.items() if v is None]

        pos_choice = random.choice(empty_cells)
        if list(game.state.values()).count("X") >= 4:
            # 移除最舊的電腦子 (假設有紀錄順序，這裡沒實作，暫不移除)
            pass
        game.state[pos_choice] = "X"
        print(f"🤖 電腦落子在 {pos_choice}")
        print_board()
        say(f"我下在 {pos_choice}")

        winner = check_winner()
        if winner:
            handle_winner(winner)
            return None  # 已播報

        return None  # 已在函式內說明玩家與電腦落子，外層不再重複播報
    else:
        return "抱歉，我聽不懂你的指令"

def handle_winner(winner):
    if winner == "O":
        say("恭喜你贏了！")
        print("🎉 玩家獲勝！")
    else:
        say("我贏了！")
        print("🤖 電腦獲勝！")
    reset_game()

# 🔊 TTS 輸出
async def speak(text):
    communicate = edge_tts.Communicate(text, "zh-TW-HsiaoChenNeural")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        await communicate.save(tmp.name)
        filename = tmp.name

    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()
    os.remove(filename)

def say(text):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(speak(text))
    else:
        loop.create_task(speak(text))
    print(f"🔊 電腦回覆: {text}")

# 🌀 測試 Loop
print("🎮 遊戲開始！")
print("規則：雙方各最多 4 子，第五手起會移除自己最舊的一子。")
print("棋盤格子名稱：a1 ~ c3（a=最上排, c=最下排, 1=最左, 3=最右）")
print_board()

if __name__ == "__main__":
    while True:
        mode = input("請選擇輸入方式（v=語音 / t=文字 / q=離開）: ").strip().lower()
        if mode == "q":
            print("🎮 遊戲結束")
            break
        elif mode == "v":
            text = record_and_recognize(duration=6)  # 錄音加長
            text = clean_command(text)  # 自動修正
            print(f"✨ 修正後指令: {text}")
        elif mode == "t":
            text = input("請輸入你的指令（例如: 放在 b2, 把 a1 移到 c3）: ")
        else:
            print("❌ 無效的選項，請重新選擇")
            continue

        reply = interpret_with_gpt(text)
        # 只有在需要額外播報（如錯誤訊息）時才回傳字串；一般情況函式內已播報
        if isinstance(reply, str) and reply.strip():
            say(reply)