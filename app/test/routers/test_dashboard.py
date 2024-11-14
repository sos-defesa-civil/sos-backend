from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock
from app.cruds.dashboard import get_session_data, get_ocorrencia_data, get_curtida_data, count_ocorrencias_by_tipo, count_ocorrencias_by_tipo_per_month

client = TestClient(app)

def test_ocorrencias_card():
    # Mock da função que consulta os dados do banco
    mock_get_ocorrencia_data = MagicMock()
    mock_get_ocorrencia_data.return_value = {
        "total": 100,
        "today": 10,
        "yesterdayPercent": 5,
        "lastWeekPercent": -3
    }
    
    # Substitui a função original por nossa versão mockada
    app.dependency_overrides[get_ocorrencia_data] = mock_get_ocorrencia_data
    
    response = client.get("/dashboard/ocorrencias-card")
    
    # Verifica se a resposta está conforme esperado
    assert response.status_code == 200
    assert response.json() == {
        "total": 100,
        "today": 10,
        "yesterdayPercent": 5,
        "lastWeekPercent": -3
    }

def test_sessoes_card():
    mock_get_session_data = MagicMock()
    mock_get_session_data.return_value = {
        "total": 500,
        "today": 50,
        "yesterdayPercent": 10,
        "lastWeekPercent": 2
    }
    
    app.dependency_overrides[get_session_data] = mock_get_session_data
    
    response = client.get("/dashboard/sessions-card")
    
    assert response.status_code == 200
    assert response.json() == {
        "total": 500,
        "today": 50,
        "yesterdayPercent": 10,
        "lastWeekPercent": 2
    }

def test_curtidas_card():
    mock_get_curtida_data = MagicMock()
    mock_get_curtida_data.return_value = {
        "total": 300,
        "today": 30,
        "yesterdayPercent": -2,
        "lastWeekPercent": 7
    }
    
    app.dependency_overrides[get_curtida_data] = mock_get_curtida_data
    
    response = client.get("/dashboard/curtidas-card")
    
    assert response.status_code == 200
    assert response.json() == {
        "total": 300,
        "today": 30,
        "yesterdayPercent": -2,
        "lastWeekPercent": 7
    }

def test_pie_chart():
    mock_count_ocorrencias_by_tipo = MagicMock()
    mock_count_ocorrencias_by_tipo.return_value = {
        "data": [
            {"tipo": "Incêndio", "count": 50},
            {"tipo": "Alagamento", "count": 30}
        ]
    }
    
    app.dependency_overrides[count_ocorrencias_by_tipo] = mock_count_ocorrencias_by_tipo
    
    response = client.get("/dashboard/pie-chart")
    
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {"tipo": "Incêndio", "count": 50},
            {"tipo": "Alagamento", "count": 30}
        ]
    }

def test_monthly_chart():
    mock_count_ocorrencias_by_tipo_per_month = MagicMock()
    mock_count_ocorrencias_by_tipo_per_month.return_value = {
        "data": [
            {"tipo": "Incêndio", "year": 2024, "month": 1, "count": 20},
            {"tipo": "Alagamento", "year": 2024, "month": 2, "count": 15}
        ]
    }
    
    app.dependency_overrides[count_ocorrencias_by_tipo_per_month] = mock_count_ocorrencias_by_tipo_per_month
    
    response = client.get("/dashboard/monthly-chart")
    
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {"tipo": "Incêndio", "year": 2024, "month": 1, "count": 20},
            {"tipo": "Alagamento", "year": 2024, "month": 2, "count": 15}
        ]
    }
