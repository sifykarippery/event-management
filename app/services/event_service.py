# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from ..models import Event, User
# from ..schemas import EventCreate

# def create_event(db: Session, event: EventCreate):
#     db_event = Event(**event.dict())
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#     return db_event

# def get_events(db: Session):
#     return db.query(Event).all()

# def join_event(db: Session, event_id: int, user_id: int):
#     event = db.query(Event).filter(Event.id == event_id).first()
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found")

#     user = db.query(User).filter(User.id == user_id).first()
#     if user not in event.joiners:
#         event.joiners.append(user)
#         db.commit()
#         db.refresh(event)
#     return event
from typing import List, Optional
from app.models.event import Event

events = []
event_counter = 1

def get_all_events() -> List[Event]:
    return events

def create_event(event_data) -> Event:
    global event_counter
    event = Event(id=event_counter, **event_data.dict())
    event_counter += 1
    events.append(event)
    return event

def find_event(event_id: int) -> Optional[Event]:
    return next((e for e in events if e.id == event_id), None)

def join_event(event_id: int, username: str) -> Event:
    event = find_event(event_id)
    if event and username not in event.joiners:
        event.joiners.append(username)
    return event

def cancel_event(event_id: int) -> Event:
    event = find_event(event_id)
    if event:
        event.is_cancelled = True
    return event