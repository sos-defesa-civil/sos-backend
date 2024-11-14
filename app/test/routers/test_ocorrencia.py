import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.ocorrencia import OcorrenciaCreate
from app.database import SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_ocorrencia(setup_db):
    ocorrencia_data = {
        "titulo": "Ocorrência Teste",
        "descricao": "Descrição da ocorrência de teste",
        "bairro": "Centro",
        "tipo": "Incidente",
        "data_inicio": "2024-11-14T10:00:00",
        "data_fim": "2024-11-14T12:00:00"
    }
    
    response = client.post("/ocorrencia/", json=ocorrencia_data)
    assert response.status_code == 200
    assert response.json()["titulo"] == ocorrencia_data["titulo"]

def test_read_ocorrencia(setup_db):
    response = client.get("/ocorrencia/1")
    assert response.status_code == 200
    assert "titulo" in response.json()

def test_update_ocorrencia(setup_db):
    ocorrencia_update = {
        "titulo": "Ocorrência Atualizada",
        "descricao": "Descrição atualizada da ocorrência",
        "bairro": "Centro",
        "tipo": "Incidente",
        "data_inicio": "2024-11-14T10:00:00",
        "data_fim": "2024-11-14T12:00:00"
    }
    
    response = client.put("/ocorrencia/1", json=ocorrencia_update)
    assert response.status_code == 200
    assert response.json()["titulo"] == ocorrencia_update["titulo"]

def test_delete_ocorrencia(setup_db):
    response = client.delete("/ocorrencia/1")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

