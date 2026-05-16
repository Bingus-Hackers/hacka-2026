from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["agent"] == "assistente-juridico"


def test_chat_basico():
    r = client.post("/api/chat", json={"message": "Olá, o que você faz?"})
    assert r.status_code == 200
    assert "reply" in r.json()
