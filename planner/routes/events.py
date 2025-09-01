from fastapi import APIRouter, HTTPException, status, Body, Depends, Request
from beanie import PydanticObjectId
from sqlmodel import select
from database.connection import Database #get_session
from models.events import Event, EventUpdate
from auth.authenticate import authenticate
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

""" # For sql
@event_router.get("/", response_model=List[Event])
async def get_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events
"""

@event_router.get("/", response_model=List[Event])
async def get_all_events() -> List[Event]:
    return await event_database.get_all()

"""
@event_router.get("/{id}", response_model=Event)
async def get_event(id: int, session=Depends(get_session)) -> Event:
    event = session.query(Event).filter(Event.id == id).first()
    if event:
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found"
    )
"""

@event_router.get("/{id}", response_model=Event)
async def get_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

"""
@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {
        "message": "Event created successfully"
    }
"""

@event_router.post("/new")
async def create_event(new_event: Event, user: str = Depends(authenticate)) -> dict:
    new_event.creator = user
    await event_database.save(new_event)
    return {
        "message": "Event created successfully"
    }

"""
@event_router.put('/update/{id}', response_model=Event)
async def update_event(id:int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    event_data = new_data.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(event, key, value)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
"""

@event_router.put('/update/{id}', response_model=Event)
async def update_event(id: PydanticObjectId, new_data: EventUpdate, user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    updated_event = await event_database.update(id, new_data)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return updated_event

"""
@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event not found"
    )
"""

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not allowed"
        )

    event = await event_database.delete(id)
    
    return {"message": "Event deleted successfully"}