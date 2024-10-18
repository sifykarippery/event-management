
from pydantic import BaseModel
from typing import List
from datetime import datetime


class Event(BaseModel):
    id: int = None
    title: str
    organizer: str
    date_time: datetime
    duration: int
    location: str
    joiners: List[str] = []


class JoinRequest(BaseModel):
    user: str


class CancelRequest(BaseModel):
    event_id: int
