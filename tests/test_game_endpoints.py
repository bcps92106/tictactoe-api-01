from fastapi.testclient import TestClient
from app.api.app import app
import pytest

client = TestClient(app)

def create_game():
    response = client.post("/games", json={"mode": "manual"})
    assert response.status_code == 201
    return response.json()["game_id"]

def test_place_moves():
    # X places at a1, O places at b2
    game_id = create_game()
    # X moves first
    resp1 = client.post(f"/games/{game_id}/move", json={"player": "X", "position": "a1"})
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["board"]["a1"] == "X"
    assert data1["next_player"] == "O"
    # O moves
    resp2 = client.post(f"/games/{game_id}/move", json={"player": "O", "position": "b2"})
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["board"]["b2"] == "O"
    assert data2["next_player"] == "X"

def test_wrong_turn():
    # O tries to move first
    game_id = create_game()
    resp = client.post(f"/games/{game_id}/move", json={"player": "O", "position": "a1"})
    assert resp.status_code == 400 or resp.status_code == 422
    data = resp.json()
    assert "turn" in data.get("detail", "").lower() or "turn" in str(data.get("detail", "")).lower()

def test_duplicate_move():
    # X moves, then X or O tries to move on the same spot
    game_id = create_game()
    resp1 = client.post(f"/games/{game_id}/move", json={"player": "X", "position": "a1"})
    assert resp1.status_code == 200
    resp2 = client.post(f"/games/{game_id}/move", json={"player": "O", "position": "a1"})
    assert resp2.status_code == 400 or resp2.status_code == 422
    data = resp2.json()
    assert "occupied" in data.get("detail", "").lower() or "already" in data.get("detail", "").lower()

def test_winner_detected():
    # X wins by filling a row
    game_id = create_game()
    moves = [
        ("X", "a1"), ("O", "a2"),
        ("X", "b1"), ("O", "b2"),
        ("X", "c1"),
    ]
    for player, pos in moves:
        resp = client.post(f"/games/{game_id}/move", json={"player": player, "position": pos})
        assert resp.status_code == 200
    # Last move should result in X winning
    resp = client.get(f"/games/{game_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["winner"] == "X"
    assert data["is_over"] is True

@pytest.mark.skip(reason="目前規則每方僅 4 子，無法填滿 9 格造成和局")
def test_draw():
    # Fill the board for a draw (no winner)
    game_id = create_game()
    moves = [
        ("X", "a1"), ("O", "a2"),
        ("X", "a3"), ("O", "b1"),
        ("X", "b3"), ("O", "b2"),
        ("X", "c2"), ("O", "c1"),
        ("X", "c3"),
    ]
    for player, pos in moves:
        resp = client.post(f"/games/{game_id}/move", json={"player": player, "position": pos})
        assert resp.status_code == 200
    resp = client.get(f"/games/{game_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["winner"] is None
    assert data["is_over"] is True