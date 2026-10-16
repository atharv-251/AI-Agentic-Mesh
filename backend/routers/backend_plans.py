import hashlib
import logging
import os
import re
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import make_msgid
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AmplifyPlanSource, BackendPlan, Transition
from backend.routers.amplify import require_local_request
from backend.routers.workflow_runs import require_transition
from backend.schemas.backend_plan import ExecutePlanRequest, PlanningProposal, SendPlanRequest
from backend.services import backend_planning_service as planning
from backend.services.teams_scheduler_service import send_smtp_message
from backend.services.amplify_plan_service import proposal_from_run, require_completed_run, require_plan_source

logger = logging.getLogger("kt_planner.backend_plans")
router = APIRouter(prefix="/api/v1/transitions/{transition_id}/backend-plan", tags=["Backend planning"])


def public_plan(plan: BackendPlan, db: Session) -> dict:
    source = db.get(AmplifyPlanSource, plan.id)
    return {
        "id": plan.id, "transition_id": plan.transition_id, "status": plan.status,
        "source_files": plan.source_files, "proposal": plan.proposal, "result": plan.result,
        "reviewed_by": plan.reviewed_by, "error": plan.error,
        "report_sha256": plan.report_sha256, "delivery_status": plan.delivery_status,
        "delivery_recipients": plan.delivery_recipients, "delivery_error": plan.delivery_error,
        "updated_at": plan.updated_at.replace(tzinfo=timezone.utc).isoformat(),
        "origin": {
            "type": "amplify" if source else "historical_backend_only",
            "run_id": source.run_id if source else None,
            "transfer": "manual_unverified_snapshot" if source else None,
        },
    }


def find_plan(transition_id: str, db: Session) -> BackendPlan:
    require_transition(transition_id, db)
    plan = db.query(BackendPlan).filter_by(transition_id=transition_id).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Prepare a backend plan first")
    return plan


@router.get("")
def get_plan(transition_id: str, request: Request, db: Session = Depends(get_db)):
    require_local_request(request)
    require_transition(transition_id, db)
    plan = db.query(BackendPlan).filter_by(transition_id=transition_id).first()
    return public_plan(plan, db) if plan else None


@router.post("", status_code=201)
def prepare_plan(
    transition_id: str, request: Request,
    request_id: UUID = Form(...),
    amplify_run_id: UUID = Form(...),
    db: Session = Depends(get_db),
):
    require_local_request(request)
    require_transition(transition_id, db)
    job, run = require_completed_run(db, transition_id, str(amplify_run_id))
    existing = db.query(BackendPlan).filter_by(transition_id=transition_id).first()
    if existing:
        source = require_plan_source(db, existing)
        if source.run_id != str(amplify_run_id):
            raise HTTPException(status_code=409, detail="This workspace already has a different immutable plan source")
        return public_plan(existing, db)
    proposal = proposal_from_run(run, db.get(Transition, transition_id).category)
    plan = BackendPlan(
        id=str(request_id), transition_id=transition_id, status="review_required",
        source_bundle=job.source_bundle, source_files=job.source_files,
        proposal=proposal.model_dump(mode="json"),
    )
    db.add(plan)
    try:
        db.flush()
        db.add(AmplifyPlanSource(plan_id=plan.id, run_id=run.run_id, job_id=job.id))
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(BackendPlan).filter_by(transition_id=transition_id).first()
        if existing:
            source = require_plan_source(db, existing)
            if source.run_id != str(amplify_run_id):
                raise HTTPException(status_code=409, detail="This KT already has a different plan source")
            return public_plan(existing, db)
        raise HTTPException(status_code=409, detail="Request ID belongs to another KT")
    db.refresh(plan)
    return public_plan(plan, db)


@router.post("/execute")
def execute_plan(
    transition_id: str, payload: ExecutePlanRequest, request: Request,
    db: Session = Depends(get_db),
):
    require_local_request(request)
    plan = find_plan(transition_id, db)
    source = require_plan_source(db, plan)
    if plan.status == "completed":
        if plan.proposal != payload.proposal.model_dump(mode="json"):
            raise HTTPException(status_code=409, detail="Completed inputs are immutable; use a new workspace for a changed plan")
        return public_plan(plan, db)
    plan_id = plan.id
    updated = db.query(BackendPlan).filter(
        BackendPlan.id == plan_id,
        BackendPlan.status.in_(["review_required", "execution_failed", "preparation_failed"]),
    ).update({"status": "running", "error": None})
    db.commit()
    if not updated:
        raise HTTPException(status_code=409, detail="Preparation/execution is already in progress. Refresh; an interrupted process requires operator inspection, not automatic retry")
    try:
        with db.get_bind().begin() as connection:
            # Legacy engines commit internally; bind them to one outer transaction.
            if connection.dialect.name == "sqlite":
                connection.exec_driver_sql("BEGIN")
            with Session(bind=connection, join_transaction_mode="rollback_only") as work:
                executing = work.get(BackendPlan, plan_id)
                executing.proposal = payload.proposal.model_dump(mode="json")
                executing.reviewed_by = payload.reviewed_by
                result = planning.execute_plan(work, executing, payload.proposal)
                result["amplify_provenance"] = {
                    "run_id": source.run_id, "job_id": source.job_id,
                    "transfer": "manual_unverified_snapshot",
                    "reviewed_normalization": True,
                }
                _, cloud_run = require_completed_run(work, transition_id, source.run_id)
                result["amplify_agent_outputs"] = [
                    {"agent_id": step["agent_id"], "agent_name": step.get("agent_name"), "result": step["result"]}
                    for step in cloud_run.snapshot["steps"] if step["node_type"] == "agent"
                ]
                report = planning.create_report(executing, payload.proposal, result)
                executing.result = result
                executing.report = report
                executing.report_sha256 = hashlib.sha256(report).hexdigest()
                executing.status = "completed"
                work.commit()
    except Exception as exc:
        logger.error("Backend execution %s rolled back (%s)", plan_id, type(exc).__name__)
        db.expire_all()
        plan = db.get(BackendPlan, plan_id)
        plan.status = "execution_failed"
        plan.error = str(exc) if isinstance(exc, ValueError) else "Python execution failed; operational writes were rolled back. Check backend diagnostics."
        db.commit()
        raise HTTPException(status_code=422, detail=plan.error) from exc
    db.expire_all()
    return public_plan(db.get(BackendPlan, plan_id), db)


@router.get("/report")
def download_plan(transition_id: str, request: Request, db: Session = Depends(get_db)):
    require_local_request(request)
    plan = find_plan(transition_id, db)
    if plan.status != "completed" or not plan.report:
        raise HTTPException(status_code=409, detail="Execute and validate the backend plan before downloading its report")
    return Response(
        content=plan.report,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="KT_Plan_{plan.id}.docx"',
            "X-KT-Plan-Origin": "amplify" if db.get(AmplifyPlanSource, plan.id) else "historical-backend-only",
        },
    )


@router.post("/email")
def email_plan(
    transition_id: str, payload: SendPlanRequest, request: Request,
    db: Session = Depends(get_db),
):
    require_local_request(request)
    plan = find_plan(transition_id, db)
    require_plan_source(db, plan)
    if plan.status != "completed" or not plan.report:
        raise HTTPException(status_code=409, detail="Execute and review the backend report before sending")
    recipients = list(dict.fromkeys(address.strip().lower() for address in payload.recipients))
    if any(not re.fullmatch(r"[^@\s,;]+@[^@\s,;]+\.[^@\s,;]+", address) for address in recipients):
        raise HTTPException(status_code=422, detail="Every recipient must be a single valid email address")
    if not os.getenv("KT_SCHEDULER_SENDER_EMAIL") or not os.getenv("KT_SCHEDULER_SMTP_SERVER"):
        raise HTTPException(status_code=503, detail="Configure the backend SMTP sender and server before delivery")
    if plan.delivery_status != "not_sent":
        raise HTTPException(status_code=409, detail="Delivery was already attempted. Inspect its saved receipt and mailbox before any manual resend")
    proposal = PlanningProposal.model_validate(plan.proposal)
    message = EmailMessage()
    message["From"] = os.environ["KT_SCHEDULER_SENDER_EMAIL"].strip()
    message["To"] = ", ".join(recipients)
    subject_name = re.sub(r"[\r\n]+", " ", proposal.project_name)
    message["Subject"] = f"KT Planned for {subject_name} - Draft for Review"
    message["Message-ID"] = make_msgid()
    message.set_content(
        f"Dear colleagues,\n\nPlease find attached the complete Knowledge Transfer plan for "
        f"{proposal.project_name}.\n\nThe document includes application context, SMEs and receivers, "
        f"knowledge scope, effort, proposed sessions, validation results, outstanding blockers and "
        f"handover requirements.\n\nStatus: DRAFT - human review required. This is not a release "
        f"authorization or calendar invitation. Please review the documented assumptions and blockers "
        f"before approving delivery.\n\nReport approved for email by: {payload.approved_by}\n"
        f"Execution reference: {plan.id}\nAttachment SHA-256: {plan.report_sha256}\n\n"
        "Kind regards,\nKT Planner\n"
    )
    message.add_attachment(
        plan.report, maintype="application",
        subtype="vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"KT_Plan_{plan.id}.docx",
    )
    claimed = db.query(BackendPlan).filter_by(id=plan.id, delivery_status="not_sent").update({
        "delivery_status": "sending", "delivery_recipients": recipients,
        "delivery_error": None,
        "result": {**plan.result, "email_receipt": {
            "approved_by": payload.approved_by, "message_id": str(message["Message-ID"]),
            "attempted_at": datetime.now(timezone.utc).isoformat(),
            "attachment_sha256": plan.report_sha256, "recipients": recipients,
        }},
    })
    db.commit()
    if not claimed:
        raise HTTPException(status_code=409, detail="Another request already claimed delivery")
    try:
        refused = send_smtp_message(message)
        plan.delivery_status = "partial" if refused else "accepted_by_smtp"
        if refused:
            plan.delivery_error = f"SMTP refused: {', '.join(refused)}. Other recipients may have been accepted. Do not retry automatically."
    except (OSError, smtplib.SMTPException, ValueError) as exc:
        logger.error("Report delivery %s uncertain (%s)", plan.id, type(exc).__name__)
        plan.delivery_status = "unknown"
        plan.delivery_error = "Delivery failed or is uncertain; inspect the mailbox/SMTP logs. No automatic retry is permitted."
    db.commit()
    db.refresh(plan)
    return public_plan(plan, db)
