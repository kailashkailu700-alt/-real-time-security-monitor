from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    hostname = Column(String(100))
    ip_address = Column(String(45))
    operating_system = Column(String(150))
    status = Column(String(20), default="online")   # online / offline / inactive
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("SecurityEvent", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), ForeignKey("devices.device_id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(60), nullable=False, index=True)   # failed_login, port_scan, high_traffic, etc.
    source_ip = Column(String(45))
    destination_ip = Column(String(45))
    port = Column(Integer)
    description = Column(Text)
    severity = Column(String(20), default="LOW")   # LOW / MEDIUM / HIGH / CRITICAL
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    device = relationship("Device", back_populates="events")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), ForeignKey("devices.device_id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("security_events.id", ondelete="SET NULL"), nullable=True)
    alert_type = Column(String(60), nullable=False)
    risk_level = Column(String(20), default="LOW")   # LOW / MEDIUM / HIGH / CRITICAL
    message = Column(Text, nullable=False)
    status = Column(String(20), default="open")      # open / acknowledged / resolved
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    device = relationship("Device", back_populates="alerts")


class AgentToken(Base):
    __tablename__ = "agent_tokens"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), ForeignKey("devices.device_id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)