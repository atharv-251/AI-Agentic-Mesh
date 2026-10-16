from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.models import AmplifyJob, Transition
from backend.routers.workflow_runs import AGENTS, router


@pytest.fixture
def workspace(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'workflow-test.db'}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    with sessions() as db:
        transitions = [Transition(name="Synthetic workflow API test"), Transition(name="Other KT")]
        db.add_all(transitions)
        db.commit()
        ids = [transition.id for transition in transitions]

    def connection():
        with sessions() as db:
            yield db

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = connection
    with TestClient(app) as client:
        yield client, ids, sessions
    engine.dispose()


def snapshot():
    return {
        "run_id": str(uuid4()), "workflow_id": 167, "project_id": 77,
        "status": "completed", "duration_ms": 1200,
        "steps": [
            {"node_key": f"agent-{agent}", "node_type": "agent", "agent_id": agent,
             "status": "completed", "result": '{"synthetic":true}', "attempt": 1}
            for agent in AGENTS
        ] + [
            {"node_key": "review", "node_type": "approval", "status": "approved", "result": "Draft only"},
            {"node_key": "end", "node_type": "end", "status": "completed", "result": "No send"},
        ],
        "unneeded_platform_field": "not persisted",
    }


def test_import_persistence_isolation_and_immutability(workspace):
    client, (first, second), sessions = workspace
    base = f"/api/v1/transitions/{first}/workflow-runs"
    payload = snapshot()
    assert client.get(base).json() == []
    response = client.post(base, json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["transition_id"] == first
    assert len(result["snapshot"]["steps"]) == len(payload["steps"])
    for expected, actual in zip(payload["steps"], result["snapshot"]["steps"]):
        for key, value in expected.items():
            assert actual[key] == value
    assert result["imported_at"].endswith("+00:00")
    assert "unneeded_platform_field" not in result["snapshot"]
    assert client.get(base).json() == [result]
    assert client.get(f"{base}/{payload['run_id']}").json() == result
    report = client.get(f"{base}/{payload['run_id']}/report")
    assert report.status_code == 200
    assert report.text == '{"synthetic":true}'
    assert report.headers["content-disposition"] == f'attachment; filename="KT_Plan_{payload["run_id"]}.md"'
    assert report.headers["content-type"].startswith("text/markdown")
    assert client.get(f"/api/v1/transitions/{second}/workflow-runs").json() == []
    assert client.get(f"/api/v1/transitions/{second}/workflow-runs/{payload['run_id']}").status_code == 404
    assert client.post(base, json=payload).status_code == 409
    assert client.post(f"/api/v1/transitions/{second}/workflow-runs", json=payload).status_code == 409
    with sessions() as db:
        assert db.get(Transition, first).status == "draft"


def test_submitted_run_cannot_be_imported_into_another_kt(workspace):
    client, (first, second), sessions = workspace
    payload = snapshot()
    with sessions() as db:
        db.add(AmplifyJob(
            transition_id=first, status="accepted", source_bundle="Synthetic source",
            source_files=[], remote_run_id=payload["run_id"],
        ))
        db.commit()
    assert client.post(f"/api/v1/transitions/{second}/workflow-runs", json=payload).status_code == 409
    assert client.get(f"/api/v1/transitions/{second}/workflow-runs").json() == []
    assert client.post(f"/api/v1/transitions/{first}/workflow-runs", json=payload).status_code == 201
    assert client.get(f"/api/v1/transitions/{second}/workflow-runs/{payload['run_id']}/report").status_code == 404


@pytest.mark.parametrize("field,value", [
    ("workflow_id", 168), ("project_id", 78), ("run_id", "not-a-uuid"), ("duration_ms", -1),
])
def test_invalid_run_fields(workspace, field, value):
    client, (first, _), _sessions = workspace
    payload = snapshot()
    payload[field] = value
    assert client.post(f"/api/v1/transitions/{first}/workflow-runs", json=payload).status_code == 422


def test_invalid_steps_and_missing_kt(workspace):
    client, (first, _), _sessions = workspace
    base = f"/api/v1/transitions/{first}/workflow-runs"
    payload = snapshot()
    payload["steps"][0]["agent_id"] = 999
    assert client.post(base, json=payload).status_code == 422
    payload = snapshot()
    payload["steps"].append(payload["steps"][0])
    assert client.post(base, json=payload).status_code == 422
    payload = snapshot()
    payload["steps"][0]["result"] = "x" * 100_001
    assert client.post(base, json=payload).status_code == 422
    payload = snapshot()
    for step in payload["steps"][:6]:
        step["result"] = "x" * 90_000
    assert client.post(base, json=payload).status_code == 422
    assert client.get("/api/v1/transitions/missing/workflow-runs").status_code == 404
    assert client.post("/api/v1/transitions/missing/workflow-runs", json=snapshot()).status_code == 404


def test_partial_run_preserves_unknowns(workspace):
    client, (first, _), _sessions = workspace
    payload = snapshot()
    payload.pop("duration_ms")
    payload["status"] = "running"
    payload["steps"] = [payload["steps"][0]]
    payload["steps"][0]["result"] = None
    response = client.post(f"/api/v1/transitions/{first}/workflow-runs", json=payload)
    assert response.status_code == 201
    saved = response.json()["snapshot"]
    assert saved["duration_ms"] is None
    assert saved["steps"][0]["result"] is None
    assert len(saved["steps"]) == 1
    assert client.get(f"/api/v1/transitions/{first}/workflow-runs/{payload['run_id']}/report").status_code == 404


def test_output_and_step_limits_at_boundary(workspace):
    client, (first, _), _sessions = workspace
    base = f"/api/v1/transitions/{first}/workflow-runs"
    payload = snapshot()
    for step in payload["steps"]:
        step["result"] = None
    for step in payload["steps"][:5]:
        step["result"] = "x" * 100_000
    for index in range(50 - len(payload["steps"])):
        payload["steps"].append({
            "node_key": f"extra-{index}", "node_type": "end", "status": "not_executed",
        })
    assert client.post(base, json=payload).status_code == 201
    payload["run_id"] = str(uuid4())
    payload["steps"].append({"node_key": "over-limit", "node_type": "end", "status": "not_executed"})
    assert client.post(base, json=payload).status_code == 422
