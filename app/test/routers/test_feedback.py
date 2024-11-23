import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from datetime import datetime

client = TestClient(app)

# Configuração do banco de dados para os testes
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Testar criação de feedback
def test_create_feedback(db):
    response = client.post("/feedback/", json={
        "titulo": "Feedback Teste",
        "descricao": "Descrição do feedback de teste",
        "status": "pending",
        "data_registro": datetime.now().isoformat(),
        "user_id": 1,
        "oc_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Feedback Teste"
    assert data["descricao"] == "Descrição do feedback de teste"
    assert data["status"] == "pending"
    assert data["user_id"] == 1
    assert data["oc_id"] == 1

# Testar leitura de feedback específico
def test_read_feedback(db):
    # Supondo que o feedback com id 1 já foi criado
    feedback_id = 1  # ID do feedback criado
    response = client.get(f"/feedback/{feedback_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feedback_id
    assert "titulo" in data
    assert "descricao" in data
    assert "status" in data

# Testar atualização de feedback
def test_update_feedback(db):
    feedback_id = 1  # ID do feedback que será atualizado
    response = client.put(f"/feedback/{feedback_id}", json={
        "titulo": "Feedback Atualizado",
        "descricao": "Descrição atualizada",
        "status": "resolved",
        "data_registro": datetime.now().isoformat(),
        "user_id": 1,
        "oc_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Feedback Atualizado"
    assert data["descricao"] == "Descrição atualizada"
    assert data["status"] == "resolved"

# Testar exclusão de feedback
def test_delete_feedback(db):
    feedback_id = 1  # ID do feedback que será deletado
    response = client.delete(f"/feedback/{feedback_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feedback_id

    # Verifica se o feedback foi realmente deletado
    response = client.get(f"/feedback/{feedback_id}")
    assert response.status_code == 404  # O feedback não deve mais existir

