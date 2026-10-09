from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Device
from app.schemas import DeviceRegister, DeviceOut

router = APIRouter(prefix="/api/devices", tags=["Devices"])


@router.post("/register", response_model=DeviceOut)
def register_device(payload: DeviceRegister, db: Session = Depends(get_db)):
    existing = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if existing:
        existing.hostname = payload.hostname
        existing.ip_address = payload.ip_address
        existing.operating_system = payload.operating_system
        existing.status = "online"
        existing.last_seen = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing

    device = Device(
        device_id=payload.device_id,
        hostname=payload.hostname,
        ip_address=payload.ip_address,
        operating_system=payload.operating_system,
        status="online",
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("", response_model=list[DeviceOut])
def list_devices(db: Session = Depends(get_db)):
    return db.query(Device).order_by(Device.last_seen.desc()).all()


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device