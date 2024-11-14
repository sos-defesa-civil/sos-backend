import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.registro import Registro
from app.database import SessionLocal, engine
from datetime import datetime
from app.schemas.registro import RegistroResponse

client = TestClient(app)

# Criação do banco de dados de teste e sessão de teste
@pytest.fixture(scope="module")
def setup_db():
    # Cria o banco de dados de teste
    db = SessionLocal()
    # Certifique-se de que as tabelas sejam criadas
    Registro.metadata.create_all(bind=engine)
    yield db
    db.close()
    # Limpeza do banco de dados após os testes
    Registro.metadata.drop_all(bind=engine)

# Teste de criação de registro
def test_create_registro(setup_db):
    registro_data = {
        "user_id": 1,
        "tipo": "Incidente",
        "descricao": "Descrição do incidente de teste"
    }

    # Fazendo a requisição POST para criar o registro
    response = client.post("/registro", json=registro_data)
    assert response.status_code == 200
    assert "id" in response.json()  # Verificando se o ID foi retornado
    assert response.json()["user_id"] == registro_data["user_id"]
    assert response.json()["tipo"] == registro_data["tipo"]
    assert response.json()["descricao"] == registro_data["descricao"]

# Teste de leitura de registros
def test_get_registros(setup_db):
    # Insira registros de exemplo diretamente no banco de dados de teste
    new_registro = Registro(user_id=1, tipo="Incidente", descricao="Testando leitura de registros")
    setup_db.add(new_registro)
    setup_db.commit()

    # Fazendo a requisição GET para recuperar os registros
    response = client.get("/registro")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Verifique se algum registro foi retornado

    # Verificando o conteúdo de um registro retornado
    registro = response.json()[0]
    assert "id" in registro
    assert "user_id" in registro
    assert "tipo" in registro
    assert "descricao" in registro
    assert "data" in registro

# Teste de erro ao tentar criar registro com dados inválidos
def test_create_registro_invalid(setup_db):
    invalid_registro_data = {
        "user_id": None,  # Dado inválido
        "tipo": "Incidente",
        "descricao": "Tentando criar registro com dados inválidos"
    }
    response = client.post("/registro", json=invalid_registro_data)
    assert response.status_code == 422  # Espera erro de validação (Unprocessable Entity)
    assert response.json()["detail"][0]["msg"] == "none is not allowed"

# Teste para garantir que um registro não existe após ser removido
def test_delete_registro(setup_db):
    new_registro = Registro(user_id=2, tipo="Alerta", descricao="Registro para exclusão")
    setup_db.add(new_registro)
    setup_db.commit()

    # Excluindo o registro manualmente
    registro_id = new_registro.id
    setup_db.delete(new_registro)
    setup_db.commit()

    # Tentando recuperar o registro excluído
    response = client.get(f"/registro/{registro_id}")
    assert response.status_code == 404  # Registro não deve ser encontrado
