from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Testa a rota raiz para verificar se a aplicação está ativa
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is up and running"}

# Testa uma rota de status/saúde, se existir, para checar a integridade do app
def test_health_check():
    response = client.get("/health")  # Substitua pela rota de health check real
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Teste de autenticação (caso aplicável)
def test_authentication():
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
