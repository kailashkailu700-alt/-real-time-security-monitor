from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SecurityEvent, Device
from app.schemas import EventIn, EventOut

router = APIRouter(prefix="/api/events", tags=["Security Events"])


@router.post("", response_model=EventOut, status_code=201)
def create_event(payload: EventIn, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    event = SecurityEvent(
        device_id=payload.device_id,
        event_type=payload.event_type,
        source_ip=payload.source_ip,
        destination_ip=payload.destination_ip,
        port=payload.port,
        description=payload.description,
        severity=payload.severity,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    from app.detection import run_detection
    run_detection(event, db)

    return event


@router.get("", response_model=list[EventOut])
def list_events(limit: int = 100, db: Session = Depends(get_db)):
    return (
        db.query(SecurityEvent)
        .order_by(SecurityEvent.timestamp.desc())
        .limit(limit)
        .all()
    )


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event