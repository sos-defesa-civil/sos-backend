import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, SessionLocal
from app.schemas.usuario import UsuarioCreate
from app.schemas.ocorrencia import OcorrenciaCreate
from app.schemas.feedback import FeedbackCreate
from app.schemas.midia import MidiaCreate
from app.schemas.curtida import CurtidaCreate
from datetime import datetime

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

# Testa a criação de usuário
# def test_create_usuario(db):
#     usuario_data = {
#         "nome": "Test User",
#         "data_nascimento": "2000-01-01",
#         "cpf": "12345678901",
#         "email": "test@example.com",
#         "senha": "password",
#         "admin": False,
#         "endereco": "123 Test St",
#         "num_ocorrencias_registradas": 0,
#         "telefone": "1234567890",
#         "celular": "0987654321"
#     }
#     response = client.post("/api/cidadao/", json=usuario_data)
#     assert response.status_code == 200
#     assert response.json()["nome"] == usuario_data["nome"]

# # Testa a recuperação de usuário
# def test_read_usuario(db):
    
#     response = client.get("/api/usuario/1")  # Assumindo que existe usuário com ID 1
#     assert response.status_code == 200
#     assert "nome" in response.json()

# # Testa a atualização de usuário
# def test_update_usuario(db):
#     usuario_update_data = {
#         "nome": "Updated User",
#         "data_nascimento": datetime(2000, 1, 1).isoformat(),
#         "cpf": "12345678901",
#         "email": "test@example.com",
#         "senha": "newpassword",
#         "admin": False
#     }
#     response = client.put("/api/1", json=usuario_update_data)  # Assumindo que existe usuário com ID 1
#     assert response.status_code == 200
#     assert response.json()["nome"] == usuario_update_data["nome"]

# # Testa a criação de ocorrência
# def test_create_ocorrencia(db):
#     ocorrencia_data = {
#         "tipo": "tipo1",
#         "bairro": "Test Bairro",
#         "descricao": "Test Description",
#         "data_registro": "2024-01-01T00:00:00",
#         "ultima_atualizacao": "2024-01-01T00:00:00",
#         "user_id": 1,
#         "latitude": 0.0,
#         "longitude": 0.0
#     }
#     response = client.post("/api/ocorrencia/", json=ocorrencia_data)
#     assert response.status_code == 200
#     assert response.json()["descricao"] == ocorrencia_data["descricao"]

# # Testa a criação de feedback
# def test_create_feedback(db):
#     feedback_data = {
#         "titulo": "Test Title",
#         "descricao": "Test Description",
#         "status": "open",
#         "data_registro": "2024-01-01T00:00:00",
#         "user_id": 1,
#         "oc_id": 1
#     }
#     response = client.post("/api/feedback/", json=feedback_data)
#     assert response.status_code == 200
#     assert response.json()["titulo"] == feedback_data["titulo"]

# # Testa a criação de mídia
# def test_create_midia(db):
#     with open("app/test/mapa.png", "rb") as image:
#         response = client.post("/api/midia/?ocorrencia_id=1&tipo=image", files={"midias": image})
#         assert response.status_code == 200
#         assert response.json()[0]["tipo"] == "image"

# # Testa a criação de curtida
# def test_create_curtida(db):
#     curtida_data = {
#         "id": 1,
#         "user_id": 1,
#         "oc_id": 1,
#         "data_registro": "2024-01-01T00:00:00"
#     }
#     response = client.post("/api/ocorrencia/1/curtidas/", json=curtida_data)
#     assert response.status_code == 200
