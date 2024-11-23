import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.models.usuario import Usuario, Cidadao, Funcionario_Defesa_Civil
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, CidadaoCreate, FuncionarioDefesaCivilCreate
from app.repositories.usuario import (
    create_cidadao, create_funcionario, get_usuario, get_usuarios, 
    update_usuario, delete_usuario, create_base_usuario
)
from app.auth.password import verify_password

client = TestClient(app)

# Teste para criar um usuário base

# Teste para criar um Cidadão
def test_create_cidadao(db):
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
    # assert response.json()["endereco"] == "Rua Principal, 123"
    # assert response.json()["num_ocorrencias_registradas"] == 5
    # assert response.json()["telefone"] == "(11) 2345-6789"
    # assert response.json()["celular"] == "(11) 91234-5678"
    # assert response.json()["senha"] != "senha_cidadao"  # Senha deve estar hasheada

# Teste para criar um Funcionário de Defesa Civil
def test_create_funcionario(db):
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
    # assert response.json()["cargo"] == "Coordenador"
    # assert response.json()["nivel_acesso"] == "Alto"
    # assert response.json()["senha"] != "senha_funcionario"  # Senha deve estar hasheada


# Teste para obter um usuário por ID
def test_get_usuario(db):
    usuario = get_usuario(db, 1)
    assert usuario is not None
    assert usuario.id == 1

# Teste para obter todos os usuários
def test_get_usuarios(db):
    usuarios = get_usuarios(db)
    assert len(usuarios) > 0  # Verifica que há pelo menos um usuário

# Teste para atualizar um usuário
def test_update_usuario(db):
    update_data = UsuarioUpdate(
        nome="João Silva Atualizado",
        data_nascimento=datetime(1990, 5, 15),
        cpf="12345678900",
        email="joao_atualizado@example.com",
        senha="nova_senha_segura",
        admin=True
    )
    usuario = update_usuario(db, 1, update_data)

    assert usuario.nome == "João Silva Atualizado"
    assert usuario.email == "joao_atualizado@example.com"
    assert usuario.admin == True

# Teste para deletar um usuário
def test_delete_usuario(db):
    response = client.delete("/api/usuario/1")

    # Verificações do status da resposta
    assert response.status_code == 200

    # Verifique se o usuário foi excluído
    usuario = response.json()
    assert usuario is not None
    assert usuario["id"] == 1

    # Verifique se o usuário realmente foi deletado
    response = client.get("/api/usuario/1")
    assert response.status_code == 404  # Usuário não deve ser encontrado
 # Verifica se o usuário foi realmente deletado

# Teste de login (verifica se a senha está hasheada e corresponde ao login)
def test_login(db):
    senha = "senha_segura"
    usuario_data = {
        "nome": "Login Teste",
        "data_nascimento": datetime(1990, 5, 15).isoformat(),
        "cpf": "12312312300",
        "email": "login@example.com",
        "senha": "senha",
        "admin": False
    }

    # Criando o usuário
    client.post("/api/cidadao/", json=usuario_data)

    

    # Recuperar o usuário criado
    response = client.post("/api/login/", data={"username": "login@example.com", "password": "senha"})
    # Verificações do status da resposta
    assert response.status_code == 200
    # token = response.json()["access_token"]  # Verifica se a senha bate com o hash

