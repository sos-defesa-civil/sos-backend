from datetime import datetime
from app.models.usuario import Usuario, Cidadao, Funcionario_Defesa_Civil
from app.models.registro import Registro
from app.repositories.registro import create_log, get_logs

import pytest


# Fixture para limpar o banco de dados antes de cada teste
@pytest.fixture(scope="function")
def clean_db(db):
    # Limpa as tabelas do banco de dados
    db.query(Registro).delete()
    db.query(Usuario).delete()
    db.commit()
    yield db  # Retorna o banco de dados para o teste
    # Após o teste, você pode realizar outras limpezas ou commits, se necessário
    db.query(Registro).delete()
    db.query(Usuario).delete()
    db.commit()


# Helper para adicionar usuários no banco
def add_test_users(db):
    # Criação de usuários com informações completas
    users = [
        Usuario(
            nome="Usuário Teste 1",
            data_nascimento=datetime(1990, 1, 1),
            cpf="000.000.000-01",
            email="teste1@example.com",
            senha="senha1",
            admin=False,
            cidadao=Cidadao(
                endereco="Rua A, 123",
                telefone="(82) 1234-5678",
                celular="(82) 98765-4321"
            )
        ),
        Usuario(
            nome="Usuário Teste 2",
            data_nascimento=datetime(1985, 5, 15),
            cpf="000.000.000-02",
            email="teste2@example.com",
            senha="senha2",
            admin=True,
            funcionario=Funcionario_Defesa_Civil(
                cargo="Analista de TI",
                nivel_acesso="Alto"
            )
        ),
    ]
    db.add_all(users)
    db.commit()

# Teste para criar um log
def test_create_log(db):
    # Adiciona usuários necessários
    add_test_users(db)

    # Cria um log
    log = create_log(db, user_id=1, log_type="INFO", log_description="Teste de log")
    
    # Verifica se foi criado corretamente
    assert log.id is not None
    assert log.user_id == 1
    assert log.tipo == "INFO"
    assert log.descricao == "Teste de log"

# Teste para recuperar logs
def test_get_logs(db):
    # Adiciona usuários necessários
    add_test_users(db)

    # Cria logs
    create_log(db, user_id=1, log_type="INFO", log_description="Log 1")
    create_log(db, user_id=2, log_type="ERROR", log_description="Log 2")

    # Recupera logs
    logs = get_logs(db)

    # Verifica se os logs foram retornados corretamente
    assert len(logs) == 2
    assert logs[0]["tipo"] == "INFO"
    assert logs[0]["username"] == "Usuário Teste 1"
    assert logs[1]["tipo"] == "ERROR"
    assert logs[1]["username"] == "Usuário Teste 2"

# Teste para o endpoint
def test_get_logs_endpoint(client, db):
    # Adiciona usuários necessários
    add_test_users(db)

    # Cria logs
    create_log(db, user_id=1, log_type="INFO", log_description="Log Endpoint Test")
    create_log(db, user_id=2, log_type="WARNING", log_description="Outro Log Test")

    # Faz a requisição ao endpoint
    response = client.get("/registro")

    # Verifica a resposta
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["tipo"] == "INFO"
    assert data[0]["descricao"] == "Log Endpoint Test"
    assert data[1]["tipo"] == "WARNING"
    assert data[1]["descricao"] == "Outro Log Test"


