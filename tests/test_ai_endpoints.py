# test_ai_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.api import app

pytestmark = pytest.mark.anyio

client = TestClient(app)


def test_ai_move():
    client.post("/reset")
    res = client.post("/ai_move", json={"player": "X"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "board" in data
    assert "turn" in data


def test_transcribe(tmp_path):
    # 建立一個假的音檔
    fake_audio = tmp_path / "test.wav"
    fake_audio.write_bytes(b"FAKEWAVDATA")

    with open(fake_audio, "rb") as f:
        res = client.post("/transcribe", files={"file": ("test.wav", f, "audio/wav")})

    # 即使是假的檔案，API 也要能正常回應
    assert res.status_code == 200
    data = res.json()
    assert "text" in data


def test_llm_move():
    res = client.post("/llm_move", json={"prompt": "幫我決定下一步棋"})
    assert res.status_code == 200
    data = res.json()

    assert "decision" in data
    decision = data["decision"]

    # 改成檢查 dict
    assert isinstance(decision, dict)
    assert "action" in decision
    assert "pos" in decision
    assert decision["pos"] is not None