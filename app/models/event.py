from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db import Base

# Association table for the many-to-many relationship between events and joiners
event_joiners = Table(
    'event_joiners',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # One-to-many relationship: a user can organize many events
    organized_events = relationship("Event", back_populates="organizer")

    # Many-to-many relationship: a user can join many events
    joined_events = relationship("Event", secondary=event_joiners, back_populates="joiners")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    organizer_id = Column(Integer, ForeignKey('users.id'))
    date_time = Column(DateTime)
    duration = Column(Integer)  # Duration in minutes
    location = Column(String)

    # Relationship to the organizer (one-to-many, a user can organize multiple events)
    organizer = relationship("User", back_populates="organized_events")

    # Many-to-many relationship: multiple users can join an event
    joiners = relationship("User", secondary=event_joiners, back_populates="joined_events")
