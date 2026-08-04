"""
models.py - SQLAlchemy ORM models for users, incidents, and detection logs.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, Boolean, Text, JSON
from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="analyst")  # analyst, admin
    created_at = Column(DateTime, default=datetime.utcnow)


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    attack_type = Column(String, nullable=True)  # e.g., side-channel, spoofing
    confidence = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    verdict = Column(String, default="unknown")  # yes/no/unknown
    explanation = Column(Text, nullable=True)
    evidence = Column(JSON, nullable=True)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(String, primary_key=True, default=gen_uuid)
    incident_id = Column(String, nullable=True)
    agent_name = Column(String, nullable=False)  # supervisor/detector/retriever/reporter
    input_summary = Column(Text, nullable=True)
    output_summary = Column(Text, nullable=True)
    latency_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
