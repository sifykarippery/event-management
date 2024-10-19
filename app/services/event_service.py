from sqlalchemy.orm import Session
from app.models import event as models
from app.schemas import event as schemas



def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(**event.dict(), organizer_id=user_id)  # Set organizer_id to current user
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_all_events(db: Session):
    return db.query(models.Event).all()

def join_event(db: Session, event_id: int, user_id: int):
    event = db.query(models.Event).get(event_id)
    user = db.query(models.User).get(user_id)
    if user not in event.joiners:
        event.joiners.append(user)
        db.commit()
    return event

def leave_event(db: Session, event_id: int, user_id: int):
    event = db.query(models.Event).get(event_id)
    user = db.query(models.User).get(user_id)
    if user in event.joiners:
        event.joiners.remove(user)
        db.commit()
    return event
def get_event(db: Session, event_id: int):
    """Fetch a single event by its ID."""
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def create_user(db: Session, user_data: dict):
    # Ensure the dict is properly handled
    db_user = models.User(**user_data)  # Unpack the dictionary
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def login_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if not user:
        user = create_user(db, schemas.UserCreate(username=username))
    return user
