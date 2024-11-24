import pytest
import app.test.routers.data_teste as data_teste
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from datetime import datetime

client = TestClient(app)

## Criação de usuário de teste
usuario_data = data_teste.usuario_token()
response = client.post("/api/cidadao/", json=usuario_data)
user_id = response.json()["id"]

# Get Login token
response = client.post("/api/login/", data={"username": "test@example.com", "password": "password"})
token = response.json()["access_token"]

def create_ocorrencia():
    ocorrencia_data = data_teste.ocorrencia_alagamento()
    
    response = client.post("api/ocorrencia/", json=ocorrencia_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["descricao"] == ocorrencia_data["descricao"]

    return response.json()["id"]

oc_id = create_ocorrencia()

feedback_data = {
    "titulo": "Feedback Teste",
    "descricao": "Descrição do feedback de teste",
    "status": "pending",
    "data_registro": datetime.now().isoformat(),
    "user_id": user_id,
    "oc_id": oc_id
}

def test_create_feedback():
    response = client.post("api/feedback/", json=feedback_data, headers={"Authorization": f"Bearer {token}"})
    feedback_id = response.json()["id"]
    
    assert response.status_code == 200
    client.delete(f"api/feedback/{feedback_id}", headers={"Authorization": f"Bearer {token}"})

def test_read_feedback():
    response = client.post("api/feedback/", json=feedback_data, headers={"Authorization": f"Bearer {token}"})
    feedback_id = response.json()["id"]

    response = client.get(f'api/feedback/{feedback_id}')
    
    assert response.status_code == 200
    assert response.json()['id'] == feedback_id
    client.delete(f"api/feedback/{feedback_id}", headers={"Authorization": f"Bearer {token}"})

def test_update_feedback():
    response = client.post("api/feedback/", json=feedback_data, headers={"Authorization": f"Bearer {token}"})
    feedback_id = response.json()["id"]
    
    updated_data = feedback_data
    updated_data['status'] = 'resolved'
    updated_data['id'] = feedback_id

    response = client.put(f'/api/feedback/{feedback_id}', json=updated_data, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
    client.delete(f"api/feedback/{feedback_id}", headers={"Authorization": f"Bearer {token}"})

def test_delete_feedback():
    response = client.post("api/feedback/", json=feedback_data, headers={"Authorization": f"Bearer {token}"})
    feedback_id = response.json()["id"]

    response = client.delete(f"api/feedback/{feedback_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    client.delete(f"api/feedback/{feedback_id}", headers={"Authorization": f"Bearer {token}"})
    client.delete(f"/api/{user_id}")
    client.delete(f"/api/ocorrencia/{oc_id}", headers={"Authorization": f"Bearer {token}"})