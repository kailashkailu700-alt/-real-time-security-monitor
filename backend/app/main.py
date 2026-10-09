from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db, Base, engine
from app import models  # noqa: F401
from app.routes import devices, events, alerts, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Real-Time Device Security Monitor",
    description="External Device Intrusion Detection System",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices.router)
app.include_router(events.router)
app.include_router(alerts.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Real-Time Device Security Monitor API"
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/db-health")
def db_health(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT version();"))
        return {
            "status": "database connected",
            "postgres_version": result.scalar()
        }
    except Exception as e:
        return {
            "status": "database connection failed",
            "error": str(e)
        }
