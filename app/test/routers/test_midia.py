import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.midia import MidiaBase
from app.database import SessionLocal

client = TestClient(app)

def test_create_midia():
    files = [("midias", ("app/test/mapa.png", open("app/test/mapa.png", "rb"), "image/jpeg"))]
    response = client.post("api/midia/?ocorrencia_id=1&tipo=image", files=files)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_midia():
    response = client.get("api/midia/1")
    assert response.status_code == 200
    assert "tipo" in response.json()

def test_delete_midia():
    response = client.delete("api/midia/1")
    assert response.status_code == 200

