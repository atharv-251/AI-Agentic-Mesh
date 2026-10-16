from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, JSON, String

from backend.database import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    run_id = Column(String(36), primary_key=True)
    transition_id = Column(String(36), ForeignKey("transitions.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(40), nullable=False)
    snapshot = Column(JSON, nullable=False)
    imported_at = Column(DateTime, default=datetime.utcnow, nullable=False)
