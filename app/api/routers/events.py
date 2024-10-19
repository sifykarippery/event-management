from fastapi import FastAPI, APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect,Body
from sqlalchemy.orm import Session
from app.models import event as models
from app.schemas import event as schemas
from app.services import event_service
from app.db import engine, SessionLocal
from typing import List
from app.services.websocket_manager import manager
import json
from passlib.context import CryptContext

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Receive data from client
            # Optionally handle incoming messages if necessary
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post("/events/", response_model=schemas.Event)
async def create_event(
    event_request: schemas.EventRequest,  # Accept the combined request body
    db: Session = Depends(get_db)          # Database dependency
):
    # Extract the event data and user_id from the request body
    event_data = event_request.event        # Get event details
    user_id = event_request.user_id         # Get user ID

    # Create the event and set the organizer to the current user
    event_record = event_service.create_event(db, event_data, user_id)  # Pass user_id to associate as organizer

    event_info = {
        "event_id": event_record.id,
        "title": event_record.title,
        "location": event_record.location,
        "duration": event_record.duration,
        "organizer": event_record.organizer.username,
        "joiners": [user.username for user in event_record.joiners]
    }

    await manager.broadcast(json.dumps(event_info))  # Broadcast event creation to all clients
    return event_record
# List events
@router.get("/events/", response_model=List[schemas.Event])
def list_events(db: Session = Depends(get_db)):
    return event_service.get_all_events(db)

@router.post("/events/{event_id}/join")
async def join_event(event_id: int, request: schemas.JoinEventRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    event_service.join_event(db, event_id, user_id)

    # Fetch the event after user has joined
    event = event_service.get_event(db, event_id)

    # Prepare event data for broadcasting
    event_data = {
        "event_id": event.id,
        "joiners": [user.username for user in event.joiners]
    }

    # Broadcast the updated event data to WebSocket clients
    await manager.broadcast(json.dumps(event_data))

    return {"message": "User joined the event"}

# Leave event
@router.post("/events/{event_id}/leave")
async def leave_event(event_id: int, request: schemas.JoinEventRequest, db: Session = Depends(get_db)):
    user_id = request.user_id  # Get user_id from the request body
    event_service.leave_event(db, event_id, user_id)

    # Fetch the event after user leaves
    event = event_service.get_event(db, event_id)

    # Prepare event data for broadcasting
    event_data = {
        "event_id": event.id,
        "joiners": [user.username for user in event.joiners]
    }

    # Broadcast the updated event data to WebSocket clients
    await manager.broadcast(json.dumps(event_data))

    return {"message": "User left the event"}

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password before storing
    hashed_password = hash_password(user.password)  # Assume hash_password is a utility function

    # Check if the user already exists
    existing_user = event_service.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Pass the user data as a dictionary, including the hashed password
    return event_service.create_user(db, {**user.dict(), "password": hashed_password})
@router.post("/login", response_model=schemas.User)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Fetch the user from the database
    db_user = event_service.get_user_by_username(db, user.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Verify the password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return db_user