import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.midia import MidiaBase
from app.database import SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_midia(setup_db):
    files = [("file", ("test_image.jpg", open("test_image.jpg", "rb"), "image/jpeg"))]
    response = client.post("/midia/", files=files, data={"ocorrencia_id": 1, "tipo": "image"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_midia(setup_db):
    response = client.get("/midia/1")
    assert response.status_code == 200
    assert "tipo" in response.json()

def test_delete_midia(setup_db):
    response = client.delete("/midia/1")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

