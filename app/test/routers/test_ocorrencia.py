import pytest
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
client.post("/api/cidadao/", json=usuario_data)

# Get Login token
response = client.post("/api/login/", data={"username": "test@example.com", "password": "password"})
token = response.json()["access_token"]


def test_create_ocorrencia():
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

id_ocorrencia = test_create_ocorrencia()

def test_read_ocorrencia():
    response = client.get(f"api/ocorrencia/{id_ocorrencia}")
    assert response.status_code == 200
    assert "descricao" in response.json()

def test_update_ocorrencia():
    ocorrencia_update = {
        "tipo": "alagamentos",
        "bairro": "bairro1",
        "descricao": "Updated",
        "data_registro": "2024-10-01T13:00:00",
        "ultima_atualizacao": "2024-10-24T14:00:00",
        "user_id": 1,
        "latitude": 40.73061,
        "longitude": -73.935242
    }

    response = client.put(f"api/ocorrencia/{id_ocorrencia}", json=ocorrencia_update, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["descricao"] == ocorrencia_update["descricao"]

def test_delete_ocorrencia():
    response = client.delete(f"api/ocorrencia/{id_ocorrencia}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

