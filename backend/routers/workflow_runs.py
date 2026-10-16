from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models import AmplifyJob, Transition, WorkflowRun


router = APIRouter(prefix="/api/v1/transitions/{transition_id}/workflow-runs", tags=["Workflow runs"])
AGENTS = (165, 166, 167, 168, 144, 142, 143)


class RunStep(BaseModel):
    node_key: str = Field(min_length=1, max_length=200)
    node_type: Literal["start", "agent", "approval", "end"]
    agent_id: int | None = None
    agent_name: str | None = Field(default=None, max_length=255)
    status: str = Field(min_length=1, max_length=40)
    result: str | None = Field(default=None, max_length=100_000)
    attempt: int | None = Field(default=None, ge=1)


class RunSnapshot(BaseModel):
    run_id: UUID
    workflow_id: Literal[167]
    project_id: Literal[77]
    status: str = Field(min_length=1, max_length=40)
    duration_ms: int | None = Field(default=None, ge=0)
    steps: list[RunStep] = Field(max_length=50)

    @model_validator(mode="after")
    def validate_steps(self):
        keys = [step.node_key for step in self.steps]
        if len(keys) != len(set(keys)):
            raise ValueError("Each node_key must be unique")
        agents = [step.agent_id for step in self.steps if step.node_type == "agent"]
        if any(agent not in AGENTS for agent in agents) or len(agents) != len(set(agents)):
            raise ValueError("Agent steps must be unique members of the seven-agent workflow")
        if sum(len(step.result or "") for step in self.steps) > 500_000:
            raise ValueError("Combined step output exceeds 500,000 characters")
        return self


class RunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    run_id: str
    transition_id: str
    status: str
    snapshot: RunSnapshot
    imported_at: datetime

    @field_serializer("imported_at")
    def serialize_imported_at(self, value: datetime):
        return value.replace(tzinfo=timezone.utc).isoformat() if value.tzinfo is None else value.isoformat()


def require_transition(transition_id: str, db: Session):
    if db.get(Transition, transition_id) is None:
        raise HTTPException(status_code=404, detail="Transition not found")


@router.get("", response_model=list[RunResponse])
def list_runs(transition_id: str, db: Session = Depends(get_db)):
    require_transition(transition_id, db)
    return db.query(WorkflowRun).filter_by(transition_id=transition_id).order_by(WorkflowRun.imported_at.desc()).all()


@router.post("", response_model=RunResponse, status_code=201)
def import_run(transition_id: str, payload: RunSnapshot, db: Session = Depends(get_db)):
    require_transition(transition_id, db)
    if db.get(WorkflowRun, str(payload.run_id)) is not None:
        raise HTTPException(status_code=409, detail="This run is already imported; saved snapshots are immutable")
    submitted = db.query(AmplifyJob).filter_by(remote_run_id=str(payload.run_id)).first()
    if submitted is not None and submitted.transition_id != transition_id:
        raise HTTPException(status_code=409, detail="This Amplify run was submitted for a different KT")
    run = WorkflowRun(
        run_id=str(payload.run_id),
        transition_id=transition_id,
        status=payload.status,
        snapshot=payload.model_dump(mode="json"),
    )
    db.add(run)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        if db.get(WorkflowRun, str(payload.run_id)) is not None:
            raise HTTPException(status_code=409, detail="This run is already imported; saved snapshots are immutable")
        raise
    db.refresh(run)
    return run


@router.get("/{run_id}", response_model=RunResponse)
def get_run(transition_id: str, run_id: UUID, db: Session = Depends(get_db)):
    require_transition(transition_id, db)
    run = db.get(WorkflowRun, str(run_id))
    if run is None or run.transition_id != transition_id:
        raise HTTPException(status_code=404, detail="Workflow run not found for this KT")
    return run


@router.get("/{run_id}/report")
def download_report(transition_id: str, run_id: UUID, db: Session = Depends(get_db)):
    run = get_run(transition_id, run_id, db)
    snapshot = RunSnapshot.model_validate(run.snapshot)
    report_step = next((step for step in snapshot.steps if step.agent_id == 143 and step.node_type == "agent"), None)
    if report_step is None or not report_step.result:
        raise HTTPException(status_code=404, detail="No reporting-agent output is present in this snapshot")
    return Response(
        content=report_step.result,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="KT_Plan_{run_id}.md"'},
    )
