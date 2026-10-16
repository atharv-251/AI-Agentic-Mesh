from sqlalchemy import Column, ForeignKey, String

from backend.database import Base


class AmplifyPlanSource(Base):
    __tablename__ = "amplify_plan_sources"

    plan_id = Column(String(36), ForeignKey("backend_plans.id", ondelete="CASCADE"), primary_key=True)
    run_id = Column(String(36), ForeignKey("workflow_runs.run_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("amplify_jobs.id", ondelete="CASCADE"), nullable=False)
