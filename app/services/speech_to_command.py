# speech_to_command.py

import re

def interpret_command(text, player='X'):
    """
    將語音（或文字）輸入轉換成棋步指令。
    回傳格式統一為 (action, from_pos, to_pos):
      - ("place", None, "b2")
      - ("move", "a1", "c2")
      - (None, None, None) 表示無法理解
    """
    text = text.lower().strip()

    # 嘗試匹配座標，例如 a1, b2, c3
    positions = re.findall(r"[abc][123]", text)

    # 判斷移動指令：格式 like "a1->b2" 或 "從a1到b2"
    if "->" in text or "到" in text or "move" in text:
        if len(positions) >= 2:
            return ("move", positions[0], positions[1])

    # 判斷放置指令：有單一位置
    if len(positions) == 1:
        return ("place", None, positions[0])

    # 中文方位詞
    mapping = {
        "左上": "a1", "中上": "b1", "右上": "c1",
        "左中": "a2", "中間": "b2", "右中": "c2",
        "左下": "a3", "中下": "b3", "右下": "c3"
    }
    for k, v in mapping.items():
        if k in text:
            return ("place", None, v)

    return (None, None, None)