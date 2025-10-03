# ai.py
# AI 模組：隨機下棋 + 語音辨識 (Whisper) + LLM 決策
import random
from transformers import pipeline

# ---------- 1. 隨機 AI ----------
def ai_move(board, player):
    """
    隨機 AI，下棋或移動棋子
    """
    if len(board.pieces[player]) < board.max_pieces:
        options = [i for i in range(9) if board.board[i] == ' ']
        if not options:
            return None, None, "AI 無合法位置"
        target = random.choice(options)
        return None, board.idx_to_pos(target), ""  # 放子
    else:
        my_pieces = board.pieces[player]
        random.shuffle(my_pieces)
        for src in my_pieces:
            options = [i for i in range(9) if board.board[i] == ' ']
            if not options:
                continue
            dest = random.choice(options)
            return board.idx_to_pos(src), board.idx_to_pos(dest), ""
        return None, None, "AI 無法移動"


# ---------- 2. 語音轉文字 (Whisper) ----------
# 初始化 Whisper pipeline（小模型，速度快，精度夠 demo）
asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

def transcribe_audio(file_path):
    """
    語音轉文字：用 Hugging Face Whisper
    原理：
      - 把音訊 (wav/mp3) 轉成特徵向量
      - 丟進 Whisper 模型
      - 解碼成文字
    """
    try:
        result = asr(file_path)
        return result.get("text", "")
    except Exception as e:
        return f"轉錄失敗: {e}"


# ---------- 3. LLM 決策 ----------
# 初始化一個簡單 LLM（先用 gpt2，輕量，跑得動）
llm = pipeline("text-generation", model="gpt2")

def ai_decision_with_llm(prompt):
    """
    呼叫 LLM 解析自然語言並轉成棋步
    原理：
      - 你給 LLM 一段 prompt（自然語言描述情境）
      - LLM 產生回覆（文字）
      - 從文字裡解析出 pos/action
    """
    output = llm(prompt, max_length=50, num_return_sequences=1)
    if not output:
        return {"action": "place", "pos": "a1", "from_pos": None, "raw": ""}
    text = output[0].get("generated_text", "")
    if "pos=" in text:
        pos = text.split("pos=")[1].split()[0]
        return {"action": "place", "pos": pos, "from_pos": None, "raw": text}
    else:
        return {"action": "place", "pos": "a1", "from_pos": None, "raw": text}