import requests

BASE = "http://127.0.0.1:8000"

def test_reset():
    r = requests.post(f"{BASE}/reset")
    print("reset:", r.json())

def test_ai_move():
    r = requests.post(f"{BASE}/ai_move", json={"player": "X"})
    print("ai_move:", r.json())

def test_llm_move():
    r = requests.post(f"{BASE}/llm_move", json={"prompt": "幫我決定下一步棋"})
    print("llm_move:", r.json())

if __name__ == "__main__":
    test_reset()
    test_ai_move()
    test_llm_move()