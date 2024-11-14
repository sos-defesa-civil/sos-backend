import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.usuario import Usuario
from app.database import SessionLocal, engine
from app.schemas.usuario import CidadaoCreate, FuncionarioDefesaCivilCreate, UsuarioUpdate
from datetime import datetime

client = TestClient(app)

# Criação do banco de dados de teste e sessão de teste
@pytest.fixture(scope="module")
def setup_db():
    # Cria o banco de dados de teste
    db = SessionLocal()
    # Certifique-se de que as tabelas sejam criadas
    Usuario.metadata.create_all(bind=engine)
    yield db
    db.close()
    # Limpeza do banco de dados após os testes
    Usuario.metadata.drop_all(bind=engine)

# Teste de criação de Cidadão
def test_create_cidadao(setup_db):
    cidadao_data = {
        "nome": "João Silva",
        "data_nascimento": "1990-05-10T00:00:00",
        "cpf": "12345678901",
        "email": "joao@teste.com",
        "senha": "senha123",
        "endereco": "Rua A, 123",
        "telefone": "1234567890",
        "celular": "9876543210"
    }

    response = client.post("/cidadao/", json=cidadao_data)
    assert response.status_code == 200
    assert response.json()["nome"] == cidadao_data["nome"]
    assert response.json()["email"] == cidadao_data["email"]

# Teste de criação de Funcionário Defesa Civil
def test_create_funcionario(setup_db):
    funcionario_data = {
        "nome": "Carlos Souza",
        "data_nascimento": "1985-08-20T00:00:00",
        "cpf": "98765432100",
        "email": "carlos@defesacivil.com",
        "senha": "senha456",
        "cargo": "Analista",
        "nivel_acesso": "Alto"
    }

    response = client.post("/funcionario/", json=funcionario_data)
    assert response.status_code == 200
    assert response.json()["nome"] == funcionario_data["nome"]
    assert response.json()["email"] == funcionario_data["email"]

# Teste de leitura de usuário
def test_read_user(setup_db):
    usuario = Usuario(nome="Mariana Lima", email="mariana@teste.com", senha="senha789", cpf="12312312312", data_nascimento=datetime.utcnow())
    setup_db.add(usuario)
    setup_db.commit()

    response = client.get(f"/usuario/{usuario.id}")
    assert response.status_code == 200
    assert response.json()["nome"] == usuario.nome
    assert response.json()["email"] == usuario.email

# Teste de atualização de usuário
def test_update_user(setup_db):
    usuario = Usuario(nome="Felipe Oliveira", email="felipe@teste.com", senha="senha123", cpf="32132132132", data_nascimento=datetime.utcnow())
    setup_db.add(usuario)
    setup_db.commit()

    updated_data = {"nome": "Felipe Oliveira Atualizado", "email": "felipe.atualizado@teste.com"}
    response = client.put(f"/{usuario.id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["nome"] == updated_data["nome"]
    assert response.json()["email"] == updated_data["email"]

# Teste de login de usuário
def test_login_user(setup_db):
    usuario_data = {
        "nome": "Lucas Silva",
        "data_nascimento": "1995-12-05T00:00:00",
        "cpf": "55555555555",
        "email": "lucas@teste.com",
        "senha": "senha321"
    }
    usuario = Usuario(**usuario_data)
    setup_db.add(usuario)
    setup_db.commit()

    login_data = {
        "username": "lucas@teste.com",
        "password": "senha321"
    }

    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# Teste de exclusão de usuário
def test_delete_user(setup_db):
    usuario = Usuario(nome="Tatiane Silva", email="tatiane@teste.com", senha="senha987", cpf="66666666666", data_nascimento=datetime.utcnow())
    setup_db.add(usuario)
    setup_db.commit()

    response = client.delete(f"/{usuario.id}")
    assert response.status_code == 200
    assert response.json()["nome"] == usuario.nome

    # Tentando ler o usuário excluído
    response = client.get(f"/usuario/{usuario.id}")
    assert response.status_code == 404  # Usuário não deve ser encontrado após exclusão
