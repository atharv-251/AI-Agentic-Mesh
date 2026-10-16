from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, JSON, LargeBinary, String, Text

from backend.database import Base
from backend.models.transition import generate_uuid


class BackendPlan(Base):
    __tablename__ = "backend_plans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transition_id = Column(String(36), ForeignKey("transitions.id", ondelete="CASCADE"), unique=True, nullable=False)
    status = Column(String(40), nullable=False, default="review_required")
    source_bundle = Column(Text, nullable=False)
    source_files = Column(JSON, nullable=False)
    proposal = Column(JSON, nullable=False)
    result = Column(JSON, nullable=True)
    report = Column(LargeBinary, nullable=True)
    report_sha256 = Column(String(64), nullable=True)
    reviewed_by = Column(String(100), nullable=True)
    error = Column(Text, nullable=True)
    delivery_status = Column(String(40), nullable=False, default="not_sent")
    delivery_recipients = Column(JSON, nullable=True)
    delivery_error = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
