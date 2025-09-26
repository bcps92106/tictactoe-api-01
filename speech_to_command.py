# speech_to_command.py

def interpret_command(text, player='X'):
    """
    將語音（或文字）輸入轉換成指令。
    回傳格式：
      - ("place", "b2")
      - ("move", "a1", "c2")
      - (None, None) 表示無法理解
    """
    text = text.lower().replace("到", "->").replace("移動", "move").replace("放", "place").strip()

    # 先判斷移動指令
    if "->" in text:
        parts = text.split("->")
        if len(parts) == 2:
            src = parts[0].strip()[-2:]  # 例如「從a1->b2」→ 取 a1
            dst = parts[1].strip()[-2:]
            return ("move", src, dst)

    # 嘗試匹配放置指令
    for pos in ["a1", "b1", "c1", "a2", "b2", "c2", "a3", "b3", "c3"]:
        if pos in text:
            return ("place", pos)

    # 也可處理一些常見方位詞（選配進階）
    mapping = {
        "左上": "a1", "中上": "b1", "右上": "c1",
        "左中": "a2", "中間": "b2", "右中": "c2",
        "左下": "a3", "中下": "b3", "右下": "c3"
    }
    for k, v in mapping.items():
        if k in text:
            return ("place", v)

    return (None, None)