from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "online"
    
    assert data["database"] == "connected", "❌ Error: Firebase no conectó"
    assert data["ai"] == "ready", "❌ Error: La IA no inició (Revisa GEMINI_API_KEY en .env)"