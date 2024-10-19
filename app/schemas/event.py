
from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    date_time: datetime
    duration: int
    location: str

class EventCreate(EventBase):
    pass

class EventRequest(BaseModel):
    event: EventCreate  # Embed the event details
    user_id: int

class Event(EventBase):
    id: int
    organizer: User
    joiners: List[User] = []

    class Config:
        from_attributes = True
class JoinEventRequest(BaseModel):
    user_id: int