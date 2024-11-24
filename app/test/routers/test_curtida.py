import pytest
import app.test.routers.data_teste as data_teste
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal

client = TestClient(app)

usuario_data = data_teste.usuario_token_curtida()
response = client.post("/api/cidadao/", json=usuario_data)
id = response.json()["id"]

# Get Login token
response = client.post("/api/login/", data={"username": "test_curtida@example.com", "password": "password"})
token = response.json()["access_token"]

def create_ocorrencia():
    ocorrencia_data = data_teste.ocorrencia_alagamento()
    
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
    client.delete(f"/api/{id}")
    client.delete(f"/api/ocorrencia/{id_ocorrencia}", headers={"Authorization": f"Bearer {token}"})
