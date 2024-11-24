import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)

def test_read_registros():
    response = client.get("api/registro/")
    
    assert response.status_code == 200