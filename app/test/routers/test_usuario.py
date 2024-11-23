import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Teste para criar um Cidadão
def test_create_cidadao():
    cidadao_data = {
        "nome": "Ana Souza",
        "data_nascimento": datetime(1985, 3, 20).isoformat(),
        "cpf": "98765432100",
        "email": "ana@example.com",
        "senha": "senha_cidadao",
        "admin": False,
        "endereco": "Rua Principal, 123",
        "num_ocorrencias_registradas": 0,
        "telefone": "(11) 2345-6789",
        "celular": "(11) 91234-5678"
    }

    response = client.post("/api/cidadao/", json=cidadao_data)

    # Verificações do status da resposta
    assert response.status_code == 200

    # Verifique os campos retornados na resposta
    assert response.json()["id"] is not None
    assert response.json()["nome"] == "Ana Souza"
    assert response.json()["cpf"] == "98765432100"
    assert response.json()["email"] == "ana@example.com"
    assert response.json()["endereco"] == "Rua Principal, 123"
    assert response.json()["num_ocorrencias_registradas"] == 0
    assert response.json()["telefone"] == "(11) 2345-6789"
    assert response.json()["celular"] == "(11) 91234-5678"

# Teste para criar um Funcionário de Defesa Civil
def test_create_funcionario():
    funcionario_data = {
        "nome": "Carlos Pereira",
        "data_nascimento": datetime(1970, 8, 10).isoformat(),
        "cpf": "11122233344",
        "email": "carlos@example.com",
        "senha": "senha_funcionario",
        "admin": True,
        "cargo": "Coordenador",
        "nivel_acesso": "Alto"
    }

    response = client.post("/api/funcionario/", json=funcionario_data)

    # Verificações do status da resposta
    assert response.status_code == 200

    # Verifique os campos retornados na resposta
    assert response.json()["id"] is not None
    assert response.json()["nome"] == "Carlos Pereira"
    assert response.json()["cpf"] == "11122233344"
    assert response.json()["email"] == "carlos@example.com"
    assert response.json()["cargo"] == "Coordenador"
    assert response.json()["nivel_acesso"] == "Alto"
    
    return response.json()["id"]

id = test_create_funcionario()

# Teste para obter um usuário por ID
def test_get_usuario():
    response = client.get(f"/api/usuario/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id

# Teste para obter todos os usuários
def test_get_usuarios():
    response = client.get("/api/usuario/")
    
    assert response.status_code == 200
    response_data = response.json() 
    assert isinstance(response_data, list) 
    assert len(response_data) > 0 # Verifica que há pelo menos um usuário

# Teste para atualizar um usuário
def test_update_usuario():
    update_data = {
        "nome": "João Silva Atualizado",
        "data_nascimento": "1990-05-15",
        "cpf": "12345678900",
        "email": "joao_atualizado@example.com",
        "senha": "nova_senha_segura",
        "admin": True
    }
    response = client.put(f"/api/usuario/{id}", json=update_data)

    assert response.status_code == 200

    assert response.json()["nome"] == "João Silva Atualizado"
    assert response.json()["email"] == "joao_atualizado@example.com"
    assert response.json()["admin"] == True

# Teste para deletar um usuário
def test_delete_usuario():
    response = client.delete(f"/api/usuario/{id}")

    # Verificações do status da resposta
    assert response.status_code == 200

    # Verifique se o usuário foi excluído
    usuario = response.json()
    assert usuario is not None
    assert usuario["id"] == id

    # Verifique se o usuário realmente foi deletado
    response = client.get(f"/api/usuario/{id}")
    assert response.status_code == 404  # Usuário não deve ser encontrado
 # Verifica se o usuário foi realmente deletado

# Teste de login (verifica se a senha está hasheada e corresponde ao login)
def test_login(): 
    # Recuperar o usuário criado
    response = client.post("/api/login/", data={"username": "ana@example.com", "password": "senha_cidadao"})
    # Verificações do status da resposta
    assert response.status_code == 200

