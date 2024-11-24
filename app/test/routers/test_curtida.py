import pytest
from datetime import datetime
#from app.repositories.curtida import create_curtida, delete_curtida
#from app.models.curtida import Curtida
#from app.schemas.curtida import CurtidaCreate
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    db = SessionLocal()
    yield db
    db.close()

usuario_data = {
        "nome": "Test User",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678901",
        "email": "test@example.com",
        "senha": "password",
        "admin": False,
        "endereco": "123 Test St",
        "num_ocorrencias_registradas": 0,
        "telefone": "1234567890",
        "celular": "0987654321"
    }
# Create Usuario
response = client.post("/api/cidadao/", json=usuario_data)
id = response.json()["id"]

# Get Login token
response = client.post("/api/login/", data={"username": "test@example.com", "password": "password"})
token = response.json()["access_token"]

def create_ocorrencia():
    ocorrencia_data = {
    "tipo": "alagamentos",
    "bairro": "bairro1",
    "descricao": "Incident description tipo 3",
    "data_registro": "2024-10-01T13:00:00",
    "ultima_atualizacao": "2024-10-24T14:00:00",
    "user_id": 1,
    "latitude": 40.73061,
    "longitude": -73.935242
    }
    
    response = client.post("api/ocorrencia/", json=ocorrencia_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["descricao"] == ocorrencia_data["descricao"]

    return response.json()["id"]

id_ocorrencia = create_ocorrencia()

def test_create_curtida():
    curtida_data = {
                    'user_id': id,
                    'oc_id': id_ocorrencia,
                    'data_registro': '2024-10-24T14:00:00'}

    response = client.post(f"api/ocorrencia/{id_ocorrencia}/curtidas/", json=curtida_data)

    assert response.status_code == 200
    return response.json()['id']

id_curtida = test_create_curtida()

def test_delete_curtida():
    response = client.delete(f"api/ocorrencia/{id_ocorrencia}/curtidas/{id_curtida}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

# def test_delete_curtida(db):
#     # Adiciona uma curtida para testar a exclusão
#     curtida_data = CurtidaCreate(id=1, user_id=1, oc_id=1, data_registro=datetime.now())
#     curtida = create_curtida(db, curtida=curtida_data)
    
#     # Chama a função de exclusão
#     deleted_curtida = delete_curtida(db, curtida_id=curtida.id)
    
#     # Verifica se a curtida foi excluída corretamente
#     assert deleted_curtida is not None
#     assert deleted_curtida.id == curtida.id
#     assert db.query(Curtida).filter(Curtida.id == curtida.id).first() is None
