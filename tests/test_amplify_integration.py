import io
import zipfile
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.models import AmplifyJob, Transition
from backend.routers.amplify import router as connection_router
from backend.routers.amplify_jobs import MAX_FILE_BYTES, extract_source, router
from backend.services import amplify_service


@pytest.fixture
def integration(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'amplify.db'}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    with sessions() as db:
        kt = Transition(name="Synthetic integration")
        db.add(kt)
        db.commit()
        tid = kt.id
    app = FastAPI()
    app.include_router(router)
    app.include_router(connection_router)

    def connection():
        with sessions() as db:
            yield db

    app.dependency_overrides[get_db] = connection
    monkeypatch.setattr(amplify_service, "get_token", lambda: "synthetic-token-123456789")
    with TestClient(app) as client:
        yield client, tid, sessions
    engine.dispose()


def submit(client, tid, request_id=None, content=b"SYNTHETIC BRD\nTopic: feed operations", filename="BRD.txt"):
    return client.post(
        f"/api/v1/transitions/{tid}/amplify-jobs",
        data={"request_id": request_id or str(uuid4()), "instructions": "Synthetic test; no sending"},
        files=[("files", (filename, content, "application/octet-stream"))],
    )


def test_submission_and_idempotency(integration, monkeypatch):
    client, tid, sessions = integration
    remote_id = str(uuid4())
    calls = []

    def remote(transition_id, bundle):
        calls.append((transition_id, bundle))
        return httpx.Response(202, json={"accepted": True, "workflow_id": 167, "project_id": 77, "run_id": remote_id, "status": "queued"})

    monkeypatch.setattr(amplify_service, "submit_workflow", remote)
    request_id = str(uuid4())
    response = submit(client, tid, request_id)
    assert response.status_code == 201
    result = response.json()
    assert result["status"] == "accepted"
    assert result["remote_run_id"] == remote_id
    assert result["source_files"][0]["characters"] == 36
    assert len(result["source_files"][0]["sha256"]) == 64
    assert result["created_at"].endswith("+00:00")
    assert submit(client, tid, request_id).json()["id"] == request_id
    assert len(calls) == 1
    assert "BEGIN SOURCE BRD.txt" in calls[0][1]
    assert client.get(f"/api/v1/transitions/{tid}/amplify-jobs").json() == [result]
    assert client.get(f"/api/v1/transitions/{tid}/amplify-jobs/{request_id}").json() == result
    assert client.get(f"/api/v1/transitions/{tid}/amplify-jobs/{uuid4()}").status_code == 404
    with sessions() as db:
        assert db.get(Transition, tid).status == "draft"
        assert db.get(AmplifyJob, request_id).source_bundle == calls[0][1]


@pytest.mark.parametrize("status", [401, 403, 404, 429, 500])
def test_remote_rejections_are_not_success(integration, monkeypatch, status):
    client, tid, _sessions = integration
    monkeypatch.setattr(amplify_service, "submit_workflow", lambda *_: httpx.Response(status, json={"detail": "Rejected"}))
    response = submit(client, tid)
    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "submission_failed"
    assert str(status) in job["error"]
    assert job["remote_run_id"] is None


def test_timeout_is_unknown_and_never_automatically_retried(integration, monkeypatch):
    client, tid, _sessions = integration
    calls = []

    def fail(*_):
        calls.append(True)
        raise httpx.ReadTimeout("Synthetic timeout")

    monkeypatch.setattr(amplify_service, "submit_workflow", fail)
    request_id = str(uuid4())
    first = submit(client, tid, request_id).json()
    assert first["status"] == "submission_unknown"
    assert "may have started" in first["error"]
    assert submit(client, tid, request_id).json() == first
    assert len(calls) == 1


def test_no_token_invalid_sources_and_missing_kt(integration, monkeypatch):
    client, tid, _sessions = integration
    monkeypatch.setattr(amplify_service, "submit_workflow", lambda *_: pytest.fail("Should not call Amplify"))
    assert submit(client, tid, content=b"").status_code == 422
    assert submit(client, tid, content=b"\xff", filename="bad.txt").status_code == 422
    assert submit(client, tid, filename="file.exe").status_code == 422
    assert submit(client, tid, filename="bad.pdf").status_code == 422
    assert submit(client, tid, content=b"x" * (MAX_FILE_BYTES + 1)).status_code == 422
    assert submit(client, tid, content=b"x" * 80_001).status_code == 422
    assert submit(client, "missing").status_code == 404
    monkeypatch.setattr(amplify_service, "get_token", lambda: None)
    assert submit(client, tid).status_code == 503


def test_duplicate_names_and_kt_boundaries(integration, monkeypatch):
    client, tid, sessions = integration
    monkeypatch.setattr(amplify_service, "submit_workflow", lambda *_: httpx.Response(202, json={"accepted": True, "workflow_id": 167, "project_id": 77, "run_id": str(uuid4()), "status": "queued"}))
    request_id = str(uuid4())
    submit(client, tid, request_id)
    with sessions() as db:
        other = Transition(name="Other synthetic KT")
        db.add(other)
        db.commit()
        other_id = other.id
    assert submit(client, other_id, request_id).status_code == 409
    assert client.get(f"/api/v1/transitions/{other_id}/amplify-jobs/{request_id}").status_code == 404
    response = client.post(
        f"/api/v1/transitions/{tid}/amplify-jobs",
        data={"request_id": str(uuid4())},
        files=[("files", ("same.txt", b"a")), ("files", ("SAME.txt", b"b"))],
    )
    assert response.status_code == 422


def test_credentials_are_never_returned_and_local_origin_required(integration, monkeypatch):
    client, tid, _sessions = integration
    saved = []
    monkeypatch.setattr(amplify_service, "save_token", lambda value: saved.append(value))
    token = "synthetic-private-token-0123456789"
    response = client.put("/api/v1/amplify/connection", json={"token": token})
    assert response.status_code == 200
    assert saved == [token]
    assert token not in response.text
    assert token not in client.get("/api/v1/amplify/connection").text
    assert client.put("/api/v1/amplify/connection", json={"token": "short"}).status_code == 422
    assert "short" not in client.put("/api/v1/amplify/connection", json={"token": "short"}).text
    assert client.get("/api/v1/amplify/connection", headers={"Origin": "https://untrusted.invalid"}).status_code == 403
    assert client.get("/api/v1/amplify/connection", headers={"Host": "untrusted.invalid"}).status_code == 403
    monkeypatch.setattr(amplify_service, "submit_workflow", lambda *_: httpx.Response(401, json={"detail": "synthetic-token-123456789"}))
    response = submit(client, tid)
    assert "synthetic-token-123456789" not in response.text
    assert "[REDACTED]" in response.text


def test_document_parsers_preserve_source_text():
    assert extract_source("example.txt", b"\xef\xbb\xbfSYNTHETIC") == "SYNTHETIC"
    docx = io.BytesIO()
    with zipfile.ZipFile(docx, "w") as archive:
        archive.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Synthetic topic</w:t></w:r></w:p></w:body></w:document>')
    assert extract_source("example.docx", docx.getvalue()) == "Synthetic topic"
    import openpyxl
    workbook = openpyxl.Workbook()
    workbook.active.append(["Synthetic topic", 2])
    xlsx = io.BytesIO()
    workbook.save(xlsx)
    workbook.close()
    assert "Synthetic topic | 2" in extract_source("example.xlsx", xlsx.getvalue())
    import fitz
    with fitz.open() as pdf:
        pdf.new_page().insert_text((72, 72), "Synthetic PDF topic")
        assert "Synthetic PDF topic" in extract_source("example.pdf", pdf.tobytes())


def test_request_contract_has_no_redirects_or_automatic_retry(monkeypatch):
    calls = []
    monkeypatch.setattr(amplify_service, "get_token", lambda: "synthetic-token")
    monkeypatch.setattr(amplify_service.httpx, "post", lambda url, **kwargs: calls.append((url, kwargs)) or httpx.Response(202))
    amplify_service.submit_workflow("kt-id", "source bundle")
    assert len(calls) == 1
    url, kwargs = calls[0]
    assert url == amplify_service.WEBHOOK_URL
    assert kwargs["json"] == {"transition_id": "kt-id", "document_bundle": "source bundle"}
    assert kwargs["headers"] == {"Authorization": "Bearer synthetic-token"}
    assert kwargs["follow_redirects"] is False


@pytest.mark.parametrize("data", [
    {"accepted": False}, {"run_id": "invalid"},
    {"accepted": True, "workflow_id": 168, "project_id": 77, "run_id": str(uuid4()), "status": "queued"},
])
def test_success_http_with_invalid_receipt_is_not_accepted(integration, monkeypatch, data):
    client, tid, _sessions = integration
    monkeypatch.setattr(amplify_service, "submit_workflow", lambda *_: httpx.Response(200, json=data))
    job = submit(client, tid).json()
    assert job["status"] == "response_error"
    assert job["remote_run_id"] is None
    assert "before retrying" in job["error"]
