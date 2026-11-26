from fastapi.testclient import TestClient
from backend.main import app
c=TestClient(app)
def test_health(): assert c.get('/health').status_code==200
def test_colonies(): assert c.get('/api/colonies').status_code==200
def test_status(): assert c.get('/api/system-status').status_code==200
def test_validation(): assert c.get('/api/validation').json()['valid']
def test_missing_colony(): assert c.get('/api/colonies/NOPE').status_code==404
def test_forecast_endpoint(): assert c.post('/api/forecast',json={'colony_id':'COLONY_001'}).status_code==200
