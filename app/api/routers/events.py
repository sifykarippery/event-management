from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.models.event import Event, JoinRequest, CancelRequest
from app.services.websocket_manager import manager
from typing import List

router = APIRouter()

# In-memory event storage (can be replaced with a database later)
events: List[Event] = []
event_id_counter = 1


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post("/events/")
async def create_event(event: Event):
    global event_id_counter
    event.id = event_id_counter
    event_id_counter += 1
    events.append(event)
    # Broadcast the new event to all WebSocket clients
    await manager.broadcast(f"Event Created: {event.title}")
    return event


@router.get("/events/")
async def get_events():
    return events


@router.put("/events/{event_id}/join")
async def join_event(event_id: int, join_request: JoinRequest):
    for event in events:
        if event.id == event_id:
            if join_request.user not in event.joiners:
                event.joiners.append(join_request.user)
                return {"message": f"{join_request.user} joined the event."}
            return {"message": f"{join_request.user} is already in the joiners list."}
    raise HTTPException(status_code=404, detail="Event not found.")

@router.put("/events/{event_id}/unjoin")
async def unjoin_event(event_id: int, join_request: JoinRequest):
    for event in events:
        if event.id == event_id and join_request.user in event.joiners:
            event.joiners.remove(join_request.user)
            await manager.broadcast(f"{join_request.user} left the event: {event.title}")
            return {"message": f"{join_request.user} left the event."}
    raise HTTPException(status_code=404, detail="User not found in joiners.")

@router.delete("/events/cancel")
async def cancel_event(cancel_request: CancelRequest):
    global events
    event_to_cancel = next((event for event in events if event.id == cancel_request.event_id), None)
    if event_to_cancel:
        events = [event for event in events if event.id != cancel_request.event_id]
        await manager.broadcast(f"Event Cancelled: {event_to_cancel.title}")
        return {"message": f"Event {event_to_cancel.title} has been cancelled."}
    raise HTTPException(status_code=404, detail="Event not found.")