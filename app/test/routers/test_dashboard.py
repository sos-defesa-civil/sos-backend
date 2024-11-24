# import pytest
# from datetime import datetime, timedelta
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.database import Base
# from app.models.ocorrencia import Ocorrencia
# from app.models.curtida import Curtida
# from app.models.session_data import SessionData
# from app.repositories.dashboard import (
#     get_session_data,
#     get_ocorrencia_data,
#     get_curtida_data,
#     count_ocorrencias_by_tipo,
#     count_ocorrencias_by_tipo_per_month,
# )

# # Configuração do banco de dados de testes em memória
# @pytest.fixture
# def db_session():
#     engine = create_engine("sqlite:///:memory:")
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Função auxiliar para criar dados fictícios
# def create_mock_data(db_session):
#     # Criando duas ocorrências para garantir dados suficientes
#     mock_ocorrencia_1 = Ocorrencia(
#         user_id=1,
#         tipo="Incêndio",
#         bairro="Centro",
#         descricao="Incêndio próximo à praça",
#         data_registro=datetime.now() - timedelta(days=1),
#         ultima_atualizacao=datetime.now(),
#         latitude=-9.6640,
#         longitude=-35.7385
#     )
#     mock_ocorrencia_2 = Ocorrencia(
#         user_id=2,
#         tipo="Inundação",
#         bairro="Praia",
#         descricao="Inundação na área da praia",
#         data_registro=datetime.now() - timedelta(days=2),
#         ultima_atualizacao=datetime.now(),
#         latitude=-9.6645,
#         longitude=-35.7390
#     )
#     mock_ocorrencia_3 = Ocorrencia(
#         user_id=3,
#         tipo="Incêndio",
#         bairro="Jatiúca",
#         descricao="Incêndio em área residencial",
#         data_registro=datetime.now() - timedelta(days=3),
#         ultima_atualizacao=datetime.now(),
#         latitude=-9.6530,
#         longitude=-35.7270
#     )

#     mock_curtida_1 = Curtida(
#         user_id=1,
#         ocorrencia_id=1,
#         data_registro = datetime.now()
#     )
    

# # Teste para o Card de Sessões
# def test_get_session_data(db_session):
#     create_mock_data(db_session)
#     result = get_session_data(db_session)
#     assert result.total == 3  # Agora temos 3 ocorrências
#     assert result.today > 0
#     assert isinstance(result.yesterdayPercent, float)
#     assert isinstance(result.lastWeekPercent, float)

# # Teste para o Card de Ocorrências
# def test_get_ocorrencia_data(db_session):
#     create_mock_data(db_session)
#     result = get_ocorrencia_data(db_session)
#     assert result.total == 3  # Agora temos 3 ocorrências
#     assert result.today == 1  # Uma ocorrência foi registrada hoje
#     assert isinstance(result.yesterdayPercent, float)
#     assert isinstance(result.lastWeekPercent, float)

# # Teste para o Card de Curtidas
# def test_get_curtida_data(db_session):
#     create_mock_data(db_session)
#     result = get_curtida_data(db_session)
#     assert result.total == 1  # Uma curtida foi registrada
#     assert result.today == 1  # Curtida registrada hoje
#     assert isinstance(result.yesterdayPercent, float)
#     assert isinstance(result.lastWeekPercent, float)

# # Teste para o gráfico de pizza (PieChart)
# def test_count_ocorrencias_by_tipo(db_session):
#     create_mock_data(db_session)
#     result = count_ocorrencias_by_tipo(db_session)
#     assert len(result.data) == 2  # Agora temos dois tipos: "Incêndio" e "Inundação"
#     assert any(item.tipo == "Incêndio" and item.count == 2 for item in result.data)
#     assert any(item.tipo == "Inundação" and item.count == 1 for item in result.data)

# # Teste para o gráfico mensal (Monthly Chart)
# def test_count_ocorrencias_by_tipo_per_month(db_session):
#     create_mock_data(db_session)
#     result = count_ocorrencias_by_tipo_per_month(db_session)
#     assert len(result.data) > 0  # Deve haver dados agrupados por tipo e mês
#     assert all(item.year == datetime.now().year for item in result.data)
