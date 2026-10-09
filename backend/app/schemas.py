from datetime import datetime
from pydantic import BaseModel, Field


# ---------- Device ----------
class DeviceRegister(BaseModel):
    device_id: str = Field(..., min_length=3, max_length=100)
    hostname: str
    ip_address: str
    operating_system: str


class DeviceOut(BaseModel):
    id: int
    device_id: str
    hostname: str
    ip_address: str
    operating_system: str
    status: str
    last_seen: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Security Event ----------
class EventIn(BaseModel):
    device_id: str
    event_type: str
    source_ip: str | None = None
    destination_ip: str | None = None
    port: int | None = None
    description: str | None = None
    severity: str = "LOW"


class EventOut(BaseModel):
    id: int
    device_id: str
    event_type: str
    source_ip: str | None
    destination_ip: str | None
    port: int | None
    description: str | None
    severity: str
    timestamp: datetime

    class Config:
        from_attributes = True