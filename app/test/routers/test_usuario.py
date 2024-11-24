import pytest
import app.test.routers.data_teste as data_teste
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Teste para criar um Cidadão
def test_create_cidadao():
    cidadao_data = data_teste.usuario_cidadao()

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

    response = client.delete(f"/api/{response.json()["id"]}")

# Teste para criar um Funcionário de Defesa Civil
def test_create_funcionario():
    funcionario_data = data_teste.usuario_funcionario()

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
    
    response = client.delete(f"/api/{response.json()["id"]}")

def create_funcionario():
    funcionario_data = data_teste.usuario_funcionario2()

    response = client.post("/api/funcionario/", json=funcionario_data)
    
    return response.json()["id"]

id = create_funcionario()

# Teste para obter um usuário por ID
def test_get_usuario():
    response = client.get(f"/api/usuario/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id

# Teste de login (verifica se a senha está hasheada e corresponde ao login)
def test_login(): 
    # Recuperar o usuário criado
    response = client.post("/api/login/", data={"username": "js@example.com", "password": "senha_funcionario"})
    # Verificações do status da resposta
    assert response.status_code == 200

# Teste para obter todos os usuários
def test_get_usuarios():
    response = client.get("/api/")
    
    assert response.status_code == 200
    response_data = response.json() 
    assert isinstance(response_data, list) 
    assert len(response_data) > 0 # Verifica que há pelo menos um usuário

# Teste para atualizar um usuário
def test_update_usuario():
    update_data = data_teste.usuario_update()
    response = client.put(f"/api/{id}", json=update_data)

    assert response.status_code == 200

    assert response.json()["nome"] == "João Silva Atualizado"
    assert response.json()["email"] == "joao_atualizado@example.com"
    assert response.json()["admin"] == True

# Teste para deletar um usuário
def test_delete_usuario():
    response = client.delete(f"/api/{id}")

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