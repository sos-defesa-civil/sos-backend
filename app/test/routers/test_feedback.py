import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app.models import Base

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
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Feedback Teste"

# Testar leitura de feedback específico
def test_read_feedback(db):
    feedback_id = 1  # ID do feedback criado
    response = client.get(f"/feedback/{feedback_id}")
    assert response.status_code == 200
    assert response.json()["id"] == feedback_id

# Testar atualização de feedback
def test_update_feedback(db):
    feedback_id = 1
    response = client.put(f"/feedback/{feedback_id}", json={
        "titulo": "Feedback Atualizado",
        "descricao": "Descrição atualizada",
        "status": "resolved"
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Feedback Atualizado"

# Testar exclusão de feedback
def test_delete_feedback(db):
    feedback_id = 1
    response = client.delete(f"/feedback/{feedback_id}")
    assert response.status_code == 200
    assert response.json()["id"] == feedback_id
