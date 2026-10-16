import hashlib
import io
import json
from datetime import date
from uuid import uuid4

import pytest
from docx import Document
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.models import AmplifyJob, AmplifyPlanSource, BackendPlan, KTSession, KTTrackingActivity, KnowledgeNode, ProjectProfile, RawExtraction, Stakeholder, Transition, WorkflowRun
from backend.routers import backend_plans
from backend.routers.workflow_runs import AGENTS
from backend.schemas.backend_plan import PlanningProposal
from backend.services import backend_planning_service as planning


def proposal():
    return {
        "project_name": "SYNTHETIC Backend Reliability Test",
        "business_purpose": "Synthetic planning verification, not a live transition.",
        "category": "development_and_ams", "intended_levels": ["L1"],
        "technology_stack": ["Python"], "environments": ["Test"],
        "support_model": "Test support", "integrations": [], "dependencies": [],
        "risks": ["Synthetic sources only"],
        "topics": [
            {"name": "Business scope", "category": "functional", "hours": 2, "evidence": "test.txt section 1"},
            {"name": "Architecture", "category": "technical", "hours": 2, "evidence": "test.txt section 2"},
            {"name": "Operations", "category": "ams_operations", "hours": 2, "evidence": "test.txt section 3"},
        ],
        "people": [
            {"name": "Synthetic SME", "role": "sme", "level": "L3", "email": None, "evidence": "test.txt section 4"},
            {"name": "Synthetic Receiver", "role": "receiver", "level": "L1", "email": None, "evidence": "test.txt section 4"},
        ],
        "uncertainties": ["Synthetic input; review actual calendar completeness"],
    }


def snapshot(run_id):
    data = proposal()
    profile = {
        "project_name": {"value": data["project_name"]},
        "purpose": {"value": data["business_purpose"]},
        "technology": {"value": data["technology_stack"]},
        "integrations": [], "risks": [{"risk": risk} for risk in data["risks"]],
    }
    people = [{
        "name": person["name"], "role": person["role"].title(),
        "support_level": person["level"], "intended_level": person["level"],
        "email": person["email"], "source_ref": person["evidence"],
    } for person in data["people"]]
    leaves = [{
        "hierarchy": {"topic": topic["name"], "category": topic["category"]},
        "estimated_hours": topic["hours"], "source_ref": topic["evidence"],
        "applicable_kt_levels": ["L1"],
    } for topic in data["topics"]]
    outputs = {
        165: {"project_profile": profile},
        166: {"stakeholders": people, "knowledge_plan": {"leaf_activities": leaves}},
    }
    return {
        "run_id": run_id, "workflow_id": 167, "project_id": 77, "status": "completed",
        "steps": [{
            "node_key": f"agent-{agent}", "node_type": "agent", "agent_id": agent,
            "agent_name": f"Synthetic agent {agent}", "status": "completed",
            "result": json.dumps(outputs.get(agent, {"synthetic_evidence": str(agent)})),
        } for agent in AGENTS],
    }


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'backend-plan.db'}", connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    with sessions() as db:
        transitions = [Transition(
            name=f"Synthetic {index}", start_date=date(2026, 11, 2), end_date=date(2026, 11, 6),
            total_duration_days=5, shadow_days=1, reverse_shadow_days=1,
            daily_kt_hours=2, available_kt_days=3, target_capacity_hours=6,
        ) for index in range(2)]
        db.add_all(transitions)
        db.commit()
        ids = [item.id for item in transitions]
        for transition_id in ids:
            db.add(AmplifyJob(
                transition_id=transition_id, remote_run_id=transition_id, status="accepted",
                source_bundle="test.txt: synthetic source",
                source_files=[{"filename": "test.txt", "sha256": "synthetic-hash", "characters": 16}],
            ))
            db.add(WorkflowRun(
                transition_id=transition_id, run_id=transition_id,
                status="completed", snapshot=snapshot(transition_id),
            ))
        db.commit()

    def connection():
        with sessions() as db:
            yield db

    app = FastAPI()
    app.include_router(backend_plans.router)
    app.dependency_overrides[get_db] = connection
    with TestClient(app) as client:
        yield client, ids, sessions
    engine.dispose()


def prepare(client, transition):
    response = client.post(
        f"/api/v1/transitions/{transition}/backend-plan",
        data={"request_id": str(uuid4()), "amplify_run_id": transition},
    )
    assert response.status_code == 201
    return response.json()


def execute(client, transition, data=None):
    return client.post(f"/api/v1/transitions/{transition}/backend-plan/execute", json={
        "proposal": data or proposal(), "reviewed_by": "Synthetic tester", "approve_operational_write": True,
    })


def test_actual_services_persist_report_and_idempotency(workspace):
    client, (first, second), sessions = workspace
    base = f"/api/v1/transitions/{first}/backend-plan"
    assert client.get(base).json() is None
    prepared = prepare(client, first)
    assert prepared["status"] == "review_required"
    assert prepared["origin"]["type"] == "amplify"
    assert prepared["origin"]["run_id"] == first
    assert "source_bundle" not in prepared and "report" not in prepared
    assert prepare(client, first)["id"] == prepared["id"]
    response = execute(client, first)
    assert response.status_code == 200, response.text
    saved = response.json()
    assert saved["status"] == "completed"
    assert saved["result"]["capacity"]["generated_hours"] == 6
    assert saved["result"]["scheduled_hours"] == 6
    assert len(saved["result"]["sessions"]) == 3
    assert saved["result"]["release_status"] == "draft_not_released"
    assert saved["result"]["tracking_status"] == "awaiting_actual_transcripts"
    assert saved["delivery_status"] == "not_sent"
    assert saved["result"]["amplify_provenance"]["run_id"] == first
    assert len(saved["result"]["amplify_agent_outputs"]) == 7
    assert execute(client, first).json()["report_sha256"] == saved["report_sha256"]
    changed = proposal()
    changed["project_name"] = "Changed"
    assert execute(client, first, changed).status_code == 409
    report = client.get(f"{base}/report")
    assert report.status_code == 200
    assert hashlib.sha256(report.content).hexdigest() == saved["report_sha256"]
    doc = Document(io.BytesIO(report.content))
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    for expected in ("10. Provenance", "Synthetic SME", "Synthetic Receiver", "DRAFT", "test.txt", "6. Proposed"):
        assert expected in text
    assert "original seven-agent Amplify outputs" in text
    assert "Synthetic agent 143" in text and "synthetic_evidence" in text
    with sessions() as db:
        assert db.query(ProjectProfile).filter_by(transition_id=first).count() == 1
        assert db.query(Stakeholder).filter_by(transition_id=first).count() == 2
        assert db.query(KnowledgeNode).filter_by(transition_id=first).count() > 3
        assert db.query(KTSession).filter_by(transition_id=first).count() == 3
        assert db.query(KTTrackingActivity).filter_by(transition_id=first).count() == 3
    assert client.get(f"/api/v1/transitions/{second}/backend-plan/report").status_code == 404


def test_failed_service_rolls_back_all_operational_writes(workspace, monkeypatch):
    client, (first, _), sessions = workspace
    prepare(client, first)

    def fail(*args, **kwargs):
        raise RuntimeError("Synthetic service failure")

    monkeypatch.setattr(planning.SchedulingService, "auto_schedule_sessions", fail)
    response = execute(client, first)
    assert response.status_code == 422
    with sessions() as db:
        for model in (ProjectProfile, RawExtraction, Stakeholder, KnowledgeNode, KTSession):
            assert db.query(model).filter_by(transition_id=first).count() == 0
        assert db.query(BackendPlan).filter_by(transition_id=first).one().status == "execution_failed"
        assert db.get(Transition, first).status == "draft"


def test_single_domain_does_not_generate_empty_domain_sessions(workspace):
    client, (first, _), _sessions = workspace
    prepare(client, first)
    data = proposal()
    for topic in data["topics"]:
        topic["category"] = "functional"
    response = execute(client, first, data)
    assert response.status_code == 200, response.text
    result = response.json()["result"]
    assert len(result["sessions"]) == 3
    assert result["scheduled_hours"] == result["capacity"]["generated_hours"] == 6
    assert len([node for node in result["hierarchy"] if node["type"] == "domain"]) == 1


def test_approval_schema_and_existing_data_guards(workspace):
    client, (first, _), sessions = workspace
    prepare(client, first)
    bad = proposal()
    bad["topics"][0]["hours"] = float("inf")
    with pytest.raises(ValueError):
        PlanningProposal.model_validate(bad)
    bad = proposal()
    bad["people"] = []
    assert execute(client, first, bad).status_code == 422
    assert client.post(f"/api/v1/transitions/{first}/backend-plan/execute", json={
        "proposal": proposal(), "reviewed_by": "Tester", "approve_operational_write": False,
    }).status_code == 422
    with sessions() as db:
        db.add(Stakeholder(transition_id=first, name="Existing person"))
        db.commit()
    assert execute(client, first).status_code == 422
    with sessions() as db:
        assert db.query(Stakeholder).filter_by(transition_id=first).one().name == "Existing person"


@pytest.mark.parametrize("delivery", ["accepted", "partial", "timeout"])
def test_email_exact_attachment_audit_and_no_resend(workspace, monkeypatch, delivery):
    client, (first, _), sessions = workspace
    prepare(client, first)
    assert execute(client, first).status_code == 200
    monkeypatch.setenv("KT_SCHEDULER_SENDER_EMAIL", "test@example.com")
    monkeypatch.setenv("KT_SCHEDULER_SMTP_SERVER", "smtp.example.com")
    messages = []

    def send(message):
        messages.append(message)
        if delivery == "timeout":
            raise TimeoutError("Synthetic ambiguous disconnect")
        return {"refused@example.com": (550, b"no")} if delivery == "partial" else {}

    monkeypatch.setattr(backend_plans, "send_smtp_message", send)
    base = f"/api/v1/transitions/{first}/backend-plan"
    payload = {"recipients": ["one@example.com", "two@example.com"], "approved_by": "Tester", "approve_email": True}
    response = client.post(f"{base}/email", json=payload)
    assert response.status_code == 200
    assert response.json()["delivery_status"] == {
        "accepted": "accepted_by_smtp", "partial": "partial", "timeout": "unknown",
    }[delivery]
    assert client.post(f"{base}/email", json=payload).status_code == 409
    assert len(messages) == 1
    attachment = list(messages[0].iter_attachments())[0]
    assert attachment.get_payload(decode=True) == client.get(f"{base}/report").content
    assert "Draft for Review" in messages[0]["Subject"]
    assert response.json()["delivery_recipients"] == payload["recipients"]
    assert response.json()["result"]["email_receipt"]["attachment_sha256"] == response.json()["report_sha256"]
    assert response.json()["result"]["email_receipt"]["approved_by"] == "Tester"


def test_mapping_failure_visible_and_local_guard(workspace):
    client, (first, _), sessions = workspace
    with sessions() as db:
        run = db.get(WorkflowRun, first)
        data = snapshot(first)
        data["steps"][0]["result"] = "not JSON"
        run.snapshot = data
        db.commit()
    base = f"/api/v1/transitions/{first}/backend-plan"
    response = client.post(base, data={"request_id": str(uuid4()), "amplify_run_id": first})
    assert response.status_code == 422
    assert "no local model" in response.json()["detail"]
    assert client.get(base).json() is None
    assert client.get(base, headers={"Origin": "https://untrusted.example"}).status_code == 403
    assert client.get(base, headers={"Host": "untrusted.example"}).status_code == 403


@pytest.mark.parametrize("case", ["no_job", "unaccepted", "no_result", "wrong_kt", "missing_agent", "failed_agent", "empty_agent", "whitespace_agent", "failed_run"])
def test_mandatory_amplify_prerequisites(workspace, case):
    client, (first, second), sessions = workspace
    with sessions() as db:
        job = db.query(AmplifyJob).filter_by(transition_id=first).one()
        run = db.get(WorkflowRun, first)
        if case == "no_job":
            db.delete(job)
        elif case == "unaccepted":
            job.status = "submission_unknown"
        elif case == "no_result":
            db.delete(run)
        elif case == "wrong_kt":
            run.transition_id = second
        else:
            data = snapshot(first)
            if case == "missing_agent":
                data["steps"].pop()
            elif case == "failed_agent":
                data["steps"][0]["status"] = "failed"
            elif case == "empty_agent":
                data["steps"][0]["result"] = ""
            elif case == "whitespace_agent":
                data["steps"][-1]["result"] = " \n\t"
            else:
                data["status"] = "failed"
            run.snapshot = data
        db.commit()
    response = client.post(f"/api/v1/transitions/{first}/backend-plan", data={
        "request_id": str(uuid4()), "amplify_run_id": first,
    })
    assert response.status_code == 409
    with sessions() as db:
        assert db.query(BackendPlan).count() == 0
        assert db.query(ProjectProfile).count() == 0


def test_upload_alone_cannot_start_local_model(workspace):
    client, (first, _), _sessions = workspace
    response = client.post(f"/api/v1/transitions/{first}/backend-plan", data={"request_id": str(uuid4())},
                           files={"files": ("test.txt", b"Do local planning instead")})
    assert response.status_code == 422
    assert "amplify_run_id" in response.text
    assert not hasattr(planning, "propose_plan")


def test_amplify_gate_rechecked_before_execution_and_email(workspace, monkeypatch):
    client, (first, _), sessions = workspace
    prepare(client, first)
    assert execute(client, first).status_code == 200
    with sessions() as db:
        db.query(AmplifyJob).filter_by(transition_id=first).update({"status": "submission_unknown"})
        db.commit()
    assert execute(client, first).status_code == 409
    sent = []
    monkeypatch.setattr(backend_plans, "send_smtp_message", lambda message: sent.append(message))
    assert client.post(f"/api/v1/transitions/{first}/backend-plan/email", json={
        "recipients": ["test@example.com"], "approved_by": "Tester", "approve_email": True,
    }).status_code == 409
    assert sent == []


def test_unknown_categories_require_explicit_review(workspace):
    client, (first, _), sessions = workspace
    with sessions() as db:
        run = db.get(WorkflowRun, first)
        data = snapshot(first)
        output = json.loads(data["steps"][1]["result"])
        output["knowledge_plan"]["leaf_activities"][0]["hierarchy"]["category"] = "feed operations"
        data["steps"][1]["result"] = json.dumps(output)
        run.snapshot = data
        db.commit()
    saved = prepare(client, first)
    assert saved["proposal"]["topics"][0]["category"] == "unclassified"
    assert any("feed operations" in item for item in saved["proposal"]["uncertainties"])
    assert execute(client, first, saved["proposal"]).status_code == 422
    assert execute(client, first).status_code == 200


def test_historical_plan_read_only_without_relabelling(workspace):
    client, (first, _), sessions = workspace
    prepare(client, first)
    assert execute(client, first).status_code == 200
    with sessions() as db:
        plan = db.query(BackendPlan).filter_by(transition_id=first).one()
        db.delete(db.get(AmplifyPlanSource, plan.id))
        db.commit()
    base = f"/api/v1/transitions/{first}/backend-plan"
    assert client.get(base).json()["origin"]["type"] == "historical_backend_only"
    assert client.get(f"{base}/report").status_code == 200
    assert client.get(f"{base}/report").headers["x-kt-plan-origin"] == "historical-backend-only"
    assert execute(client, first).status_code == 409
    assert client.post(base, data={"request_id": str(uuid4()), "amplify_run_id": first}).status_code == 409
    assert client.post(f"{base}/email", json={
        "recipients": ["one@example.com"], "approved_by": "Tester", "approve_email": True,
    }).status_code == 409
