import pytest
from fastapi.testclient import TestClient
from app import app, TEST_MODE
TEST_MODE = True

client = TestClient(app)

def test_dummy():
    assert 1 == 1

def test_reset():
    response = client.post("/reset")
    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True

def test_place_and_conflict():
    client.post("/reset")
    # X places at a1
    response1 = client.post("/game", json={"player": "X", "action": "place", "pos": "a1"})
    data1 = response1.json()
    assert response1.status_code == 200
    assert data1["success"] is True
    # O tries to place again at a1, should fail
    response2 = client.post("/game", json={"player": "O", "action": "place", "pos": "a1"})
    data2 = response2.json()
    assert response2.status_code == 200
    assert data2["success"] is False

def test_move_rules():
    client.post("/reset")
    # Place 4 pieces alternatively
    moves = [
        {"player": "X", "action": "place", "pos": "a1"},
        {"player": "O", "action": "place", "pos": "a2"},
        {"player": "X", "action": "place", "pos": "b1"},
        {"player": "O", "action": "place", "pos": "b2"},
    ]
    for move in moves:
        response = client.post("/game", json=move)
        assert response.status_code == 200
        assert response.json()["success"] is True

    # X moves from a1 to c1
    move_action = {"player": "X", "action": "move", "from_pos": "a1", "pos": "c1"}
    response = client.post("/game", json=move_action)
    assert response.status_code == 200
    assert "success" in response.json()

def test_win_condition():
    client.post("/reset")
    client.post("/game", json={"player": "X", "action": "place", "pos": "a1"})
    client.post("/game", json={"player": "O", "action": "place", "pos": "b1"})
    client.post("/game", json={"player": "X", "action": "place", "pos": "a2"})
    client.post("/game", json={"player": "O", "action": "place", "pos": "b2"})
    response = client.post("/game", json={"player": "X", "action": "place", "pos": "a3"})
    data = response.json()
    assert response.status_code == 200
    assert data["winner"] == "X"