import pytest
import app.test.routers.data_teste as data_teste
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine


client = TestClient(app)

usuario_data = data_teste.usuario_token()
response_usuario = client.post("/api/cidadao/", json=usuario_data)

# Get Login token
response = client.post("/api/login/", data={"username": "test@example.com", "password": "password"})
token = response.json()["access_token"]

def test_create_ocorrencia():
    ocorrencia_data = data_teste.ocorrencia_alagamento()
    
    response = client.post("api/ocorrencia/", json=ocorrencia_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["descricao"] == ocorrencia_data["descricao"]
    client.delete(f"api/ocorrencia/{response.json()["id"]}", headers={"Authorization": f"Bearer {token}"})
    # return response.json()["id"]

def test_read_ocorrencia():
    ocorrencia_data = data_teste.ocorrencia_alagamento()
    response = client.post("api/ocorrencia/", json=ocorrencia_data, headers={"Authorization": f"Bearer {token}"})
    id_ocorrencia = response.json()["id"]

    response = client.get(f"api/ocorrencia/{id_ocorrencia}")
    assert response.status_code == 200
    assert "descricao" in response.json()
    client.delete(f"api/ocorrencia/{response.json()["id"]}", headers={"Authorization": f"Bearer {token}"})

def test_update_ocorrencia():
    ocorrencia_update = data_teste.ocorrencia_alagamento()
    response = client.post("api/ocorrencia/", json=ocorrencia_update, headers={"Authorization": f"Bearer {token}"})
    id_ocorrencia = response.json()["id"]

    ocorrencia_update["descricao"] = "Updated"
    response = client.put(f"api/ocorrencia/{id_ocorrencia}", json=ocorrencia_update, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["descricao"] == ocorrencia_update["descricao"]
    client.delete(f"api/ocorrencia/{response.json()["id"]}", headers={"Authorization": f"Bearer {token}"})

def test_delete_ocorrencia():
    ocorrencia_update = data_teste.ocorrencia_alagamento()
    response = client.post("api/ocorrencia/", json=ocorrencia_update, headers={"Authorization": f"Bearer {token}"})
    id_ocorrencia = response.json()["id"]

    # Testa a exclusão
    response = client.delete(f"/api/ocorrencia/{id_ocorrencia}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Verifica se a ocorrência foi removida
    response = client.get(f"/api/ocorrencia/{id_ocorrencia}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404  

    client.delete(f"/api/{response_usuario.json()["id"]}")

    

