from fastapi.testclient import TestClient
from backend.main import app
from backend.database import engine
from types import SimpleNamespace

import pytest

client = TestClient(app)

def test_single_deployable_serves_frontend():
    # Test root endpoint returns HTML of React SPA
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "<!doctype html>" in resp.text.lower()
    assert "KT Planner" in resp.text

def test_single_deployable_serves_health_and_apis():
    # Test API endpoint
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    expected = "SQL Server LocalDB" if engine.dialect.name == "mssql" else "SQLite kt_planner.db"
    assert data["authoritative_db"] == expected


@pytest.mark.parametrize("dialect,expected", [
    ("sqlite", "SQLite kt_planner.db"), ("mssql", "SQL Server LocalDB"),
])
def test_health_identifies_active_database(monkeypatch, dialect, expected):
    import backend.main
    monkeypatch.setattr(backend.main, "engine", SimpleNamespace(dialect=SimpleNamespace(name=dialect)))
    assert client.get("/health").json()["authoritative_db"] == expected


@pytest.mark.parametrize("path", [
    "/api/v1/transitions/synthetic/extract",
    "/api/v1/transitions/synthetic/modules/1/run",
    "/api/v1/transitions/synthetic/profile/generate",
    "/api/v1/transitions/synthetic/scheduling/auto",
])
def test_retired_apis_are_not_registered(path):
    response = client.post(path)
    assert response.status_code in (404, 405)
    assert "text/html" not in response.headers.get("content-type", "")


def test_all_legacy_operational_routers_are_unmounted():
    from backend.routers import (
        documents_router, profile_router, knowledge_router, kt_levels_router,
        stakeholders_router, availability_router, scheduling_router,
        governance_router, export_router, database_gateway_router, modules_router,
    )
    registered = {
        (route.path, method) for route in app.routes if hasattr(route, "methods")
        for method in route.methods
    }
    for router in (
        documents_router, profile_router, knowledge_router, kt_levels_router,
        stakeholders_router, availability_router, scheduling_router,
        governance_router, export_router, database_gateway_router, modules_router,
    ):
        for route in router.routes:
            for method in route.methods:
                assert (route.path, method) not in registered
