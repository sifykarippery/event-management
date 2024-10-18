from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/events", json={
        "title": "Test Event",
        "organizer": "John",
        "date_time": "2024-10-14T18:00:00",
        "duration": 120,
        "location": "Test Location"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Event"

def test_join_event():
    response = client.post("/events/1/join", json={"username": "Jane"})
    assert response.status_code == 200
    assert "Jane" in response.json()["joiners"]