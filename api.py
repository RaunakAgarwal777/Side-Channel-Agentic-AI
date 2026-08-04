"""
api.py - REST API routes for SideChannel Sentinel OS.
Exposes auth, incident, and detection-trigger endpoints.
Depends on: config.py, database.py, models.py, auth.py
"""

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from config import get_settings
from database import get_db
from models import User, Incident
from auth import hash_password, verify_password, create_access_token, decode_access_token

settings = get_settings()
router = APIRouter(prefix=settings.API_V1_PREFIX)


# ---------- Schemas ----------
class UserCreate(BaseModel):
    email: str
    password: str


class IncidentOut(BaseModel):
    id: str
    title: str
    attack_type: str | None
    confidence: float
    risk_score: float
    verdict: str

    class Config:
        from_attributes = True


# ---------- Auth routes ----------
@router.post("/auth/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(
        {"sub": user.email}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}


# ---------- Incident routes ----------
@router.get("/incidents", response_model=List[IncidentOut])
def list_incidents(db: Session = Depends(get_db), _=Depends(decode_access_token)):
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@router.get("/incidents/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: str, db: Session = Depends(get_db), _=Depends(decode_access_token)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}
