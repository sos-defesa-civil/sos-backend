import pytest
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.cruds.registro import create_log, get_logs
from app.schemas.registro import RegistroResponse
from app.database import Base, engine
from datetime import datetime


# Criação de um banco de dados de teste
@pytest.fixture(scope="module")
def db():
    # Criando as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    db_session = Session(bind=engine)
    yield db_session
    # Limpeza após os testes
    db_session.close()
    Base.metadata.drop_all(bind=engine)


# Teste para criar um log
def test_create_log(db: Session):
    # Criação de um usuário de teste
    usuario = Usuario(nome="Test User", email="test@example.com", cpf="12312312300", senha="hashed_password", admin=False)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Criação de um log de teste
    log_type = "LOGIN"
    log_description = "User logged in"
    new_log = create_log(db, usuario.id, log_type, log_description)

    # Verifica se o log foi criado corretamente
    assert new_log is not None
    assert new_log.tipo == log_type
    assert new_log.descricao == log_description
    assert new_log.user_id == usuario.id


# Teste para recuperar logs
def test_get_logs(db: Session):
    # Criando usuário e log de teste
    usuario = Usuario(nome="Test User", email="test2@example.com", cpf="12312312301", senha="hashed_password", admin=False)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Criação de log de tipo 'SIGNUP'
    log_type = "LOGIN"
    log_description = "User logged in"
    create_log(db, usuario.id, log_type, log_description)

    # Consultando os logs
    logs = get_logs(db)

    # Verifica se o número de logs é maior que 0
    assert len(logs) > 0

    # Verifica se o log retornado tem os dados corretos
    assert logs[0]["username"] == usuario.nome
    assert logs[0]["tipo"] == log_type
    assert logs[0]["descricao"] == log_description

    assert logs[0]["tipo"] == "LOGIN"

