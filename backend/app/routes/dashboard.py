from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Device, SecurityEvent, Alert

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    total_devices = db.query(Device).count()
    online_devices = db.query(Device).filter(Device.status == "online").count()
    offline_devices = db.query(Device).filter(Device.status == "offline").count()
    total_events = db.query(SecurityEvent).count()
    total_alerts = db.query(Alert).count()
    open_alerts = db.query(Alert).filter(Alert.status == "open").count()

    # Count by risk level
    critical = db.query(Alert).filter(Alert.risk_level == "CRITICAL").count()
    high = db.query(Alert).filter(Alert.risk_level == "HIGH").count()
    medium = db.query(Alert).filter(Alert.risk_level == "MEDIUM").count()
    low = db.query(Alert).filter(Alert.risk_level == "LOW").count()

    return {
        "devices": {
            "total": total_devices,
            "online": online_devices,
            "offline": offline_devices,
        },
        "events": {
            "total": total_events,
        },
        "alerts": {
            "total": total_alerts,
            "open": open_alerts,
            "by_risk": {
                "CRITICAL": critical,
                "HIGH": high,
                "MEDIUM": medium,
                "LOW": low,
            },
        },
    }