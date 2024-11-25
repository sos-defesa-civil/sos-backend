# import pytest
# from datetime import datetime
# from fastapi.testclient import TestClient
# from app.main import app
# from app.database import Base, engine, SessionLocal
# import app.test.routers.data_teste as data_teste

# # Fixture para o cliente de teste
# @pytest.fixture(scope="function")
# def client():
#     return TestClient(app)

# # Fixture para resetar o banco antes de cada teste
# @pytest.fixture(scope="function", autouse=True)
# def reset_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

# @pytest.fixture(scope="function")
# def usuario_token(client):
#     usuario_data = data_teste.usuario_token()
#     response = client.post("/api/cidadao/", json=usuario_data)
#     assert response.status_code == 200
#     return response.json()

# # Fixture para obter o token de autenticação de um usuário
# @pytest.fixture(scope="function")
# def auth_token(client, usuario_token):
    

#     login_data = {"username": usuario_token["email"], "password": usuario_token["senha"]}
#     response = client.post("/api/login/", data=login_data)
#     assert response.status_code == 200
#     return response.json()["access_token"]