from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, JSON, String, Text

from backend.database import Base
from backend.models.transition import generate_uuid


class AmplifyJob(Base):
    __tablename__ = "amplify_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transition_id = Column(String(36), ForeignKey("transitions.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(60), nullable=False, default="submitting")
    source_bundle = Column(Text, nullable=False)
    source_files = Column(JSON, nullable=False)
    remote_run_id = Column(String(100), nullable=True)
    response = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
