import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, SessionLocal
from app.main import app
from app.models import event as models
from app.schemas import event as schemas
from app.services import event_service
from app.db import engine, SessionLocal
from typing import List
from app.services.websocket_manager import manager
import json
from passlib.context import CryptContext

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


models.Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# Test user registration
def test_register_user(test_client):
    response = test_client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

# Test user login
def test_login_user(test_client):
    response = test_client.post(
        "/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

# Test event creation
def test_create_event(test_client):
    response = test_client.post(
        "/events/",
        json={
            "event": {
                "title": "Test Event",
                "location": "Test Location",
                "duration": 120
            },
            "user_id": 1  # Assuming the user with id 1 exists
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Event"

# Test list events
def test_list_events(test_client):
    response = test_client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test joining an event
def test_join_event(test_client):
    response = test_client.post(
        "/events/1/join",
        json={"user_id": 1}  
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User joined the event"

# Test leaving an event
def test_leave_event(test_client):
    response = test_client.post(
        "/events/1/leave",
        json={"user_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User left the event"

