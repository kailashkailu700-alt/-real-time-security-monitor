from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import SecurityEvent, Alert


# Suspicious ports (445 removed — normal on Windows)
SUSPICIOUS_PORTS = {21, 23, 1433, 3306, 3389, 5900, 6379, 27017}

# Alert cooldown (minutes) — same alert repeat aagama irukka
ALERT_COOLDOWN_MINUTES = 5


def _recent_alert_exists(db: Session, device_id: str, alert_type: str) -> bool:
    since = datetime.utcnow() - timedelta(minutes=ALERT_COOLDOWN_MINUTES)
    return (
        db.query(Alert)
        .filter(
            Alert.device_id == device_id,
            Alert.alert_type == alert_type,
            Alert.created_at >= since,
        )
        .first()
        is not None
    )


def _create_alert(db: Session, device_id: str, event_id: int, alert_type: str,
                  risk_level: str, message: str):
    if _recent_alert_exists(db, device_id, alert_type):
        return

    alert = Alert(
        device_id=device_id,
        event_id=event_id,
        alert_type=alert_type,
        risk_level=risk_level,
        message=message,
        status="open",
    )
    db.add(alert)
    db.commit()


def run_detection(event: SecurityEvent, db: Session):
    # Rule 1: Repeated failed logins
    if event.event_type == "failed_login":
        since = datetime.utcnow() - timedelta(minutes=5)
        count = (
            db.query(SecurityEvent)
            .filter(
                SecurityEvent.device_id == event.device_id,
                SecurityEvent.event_type == "failed_login",
                SecurityEvent.timestamp >= since,
            )
            .count()
        )
        if count >= 5:
            _create_alert(
                db, event.device_id, event.id,
                "repeated_failed_login", "CRITICAL",
                f"{count} failed login attempts in 5 minutes on {event.device_id}",
            )
            return

    # Rule 2: Suspicious port
    if event.port and event.port in SUSPICIOUS_PORTS:
        _create_alert(
            db, event.device_id, event.id,
            f"suspicious_port_{event.port}", "HIGH",
            f"Suspicious port {event.port} activity on {event.device_id}",
        )
        return

    # Rule 3: High network traffic
    if event.event_type == "high_traffic":
        _create_alert(
            db, event.device_id, event.id,
            "high_traffic", "MEDIUM",
            f"High network activity detected on {event.device_id}",
        )
        return

    # Rule 4: Port scan
    if event.event_type == "port_scan":
        _create_alert(
            db, event.device_id, event.id,
            "port_scan", "HIGH",
            f"Possible port scan from {event.source_ip} on {event.device_id}",
        )
        return