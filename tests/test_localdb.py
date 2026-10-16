import os
from datetime import date, datetime, time

import pytest
from sqlalchemy import delete, inspect, select
from sqlalchemy.orm import Session

from backend.database import Base, create_database_engine
from backend.models import AmplifyJob, AmplifyPlanSource, BackendPlan, KTSession, KTTrackingActivity, KnowledgeNode, Stakeholder, Transition, WorkflowRun
from backend.services.amplify_plan_service import proposal_from_run, require_completed_run
from backend.schemas.backend_plan import PlanningProposal
from backend.services.backend_planning_service import create_report, execute_plan
from backend.sqlserver import install_delete_triggers, localdb_url
from test_backend_planning import proposal, snapshot


@pytest.fixture
def sql_db():
    database = os.getenv("KT_TEST_LOCALDB")
    if not database:
        pytest.skip("Set KT_TEST_LOCALDB to run transactional SQL Server integration tests")
    engine = create_database_engine(localdb_url(database))
    with engine.connect() as connection:
        transaction = connection.begin()
        Base.metadata.create_all(connection)
        install_delete_triggers(connection, Base.metadata)
        with Session(bind=connection, join_transaction_mode="rollback_only") as db:
            yield db
        transaction.rollback()
    engine.dispose()


def test_sqlserver_unicode_cascade_and_set_null(sql_db):
    db = sql_db
    name = "Synthetic \u65e5\u672c\u8a9e \u00e9"
    timestamp = datetime(2026, 10, 16, 12, 30, 40, 123456)
    transition = Transition(name=name, created_at=timestamp)
    db.add(transition)
    db.commit()
    db.expire_all()
    assert db.get(Transition, transition.id).name == name
    assert db.get(Transition, transition.id).created_at == timestamp
    person = Stakeholder(transition_id=transition.id, name="Synthetic person")
    parent = KnowledgeNode(transition_id=transition.id, node_type="topic", name="Synthetic parent")
    db.add_all([person, parent])
    db.commit()
    child = KnowledgeNode(transition_id=transition.id, parent_id=parent.id, node_type="subtopic", name="Synthetic child")
    db.add(child)
    db.commit()
    session = KTSession(
        transition_id=transition.id, node_id=child.id, sme_id=person.id, receiver_id=person.id,
        session_title="Synthetic session", scheduled_date=date(2026, 11, 2),
        start_time=time(10), end_time=time(12),
    )
    db.add(session)
    db.commit()
    tracking = KTTrackingActivity(transition_id=transition.id, session_id=session.id, activity_name="Synthetic")
    db.add(tracking)
    db.commit()
    person_id, session_id, child_id, parent_id, tracker_id = person.id, session.id, child.id, parent.id, tracking.id
    db.execute(delete(Stakeholder).where(Stakeholder.id == person_id))
    db.commit()
    db.expire_all()
    scheduled = db.get(KTSession, session_id)
    assert scheduled.sme_id is None and scheduled.receiver_id is None
    db.execute(delete(KnowledgeNode).where(KnowledgeNode.id == parent_id))
    db.commit()
    assert db.scalar(select(KnowledgeNode.id).where(KnowledgeNode.id == child_id)) is None
    assert db.scalar(select(KTSession.id).where(KTSession.id == session_id)) is None
    assert db.scalar(select(KTTrackingActivity.id).where(KTTrackingActivity.id == tracker_id)) is None
    plan = BackendPlan(transition_id=transition.id, source_bundle="Synthetic", source_files=[], proposal={})
    db.add(plan)
    db.commit()
    plan_id = plan.id
    db.execute(delete(Transition).where(Transition.id == transition.id))
    db.commit()
    assert db.scalar(select(BackendPlan.id).where(BackendPlan.id == plan_id)) is None


def test_sqlserver_original_services_and_report(sql_db):
    db = sql_db
    transition = Transition(
        name="SYNTHETIC transactional SQL planner test",
        start_date=date(2026, 11, 2), end_date=date(2026, 11, 6),
        total_duration_days=5, shadow_days=1, reverse_shadow_days=1, daily_kt_hours=2,
    )
    db.add(transition)
    db.commit()
    data = PlanningProposal.model_validate(proposal())
    plan = BackendPlan(
        transition_id=transition.id, source_bundle="Synthetic",
        source_files=[{"filename": "test.txt", "sha256": "synthetic", "characters": 9}],
        proposal=data.model_dump(), reviewed_by="Synthetic test",
    )
    db.add(plan)
    db.commit()
    result = execute_plan(db, plan, data)
    assert result["scheduled_hours"] == result["capacity"]["generated_hours"] == 6
    assert len(result["sessions"]) == 3
    assert create_report(plan, data, result).startswith(b"PK")


def test_sqlserver_amplify_provenance_and_cascade(sql_db):
    db = sql_db
    transition = Transition(name="SYNTHETIC Amplify provenance rollback test")
    db.add(transition)
    db.commit()
    job = AmplifyJob(
        transition_id=transition.id, remote_run_id=transition.id, status="accepted",
        source_bundle="Synthetic", source_files=[],
    )
    run = WorkflowRun(
        run_id=transition.id, transition_id=transition.id,
        status="completed", snapshot=snapshot(transition.id),
    )
    plan = BackendPlan(
        transition_id=transition.id, source_bundle="Synthetic",
        source_files=[], proposal=proposal(),
    )
    db.add_all([job, run, plan])
    db.commit()
    link = AmplifyPlanSource(plan_id=plan.id, run_id=run.run_id, job_id=job.id)
    db.add(link)
    db.commit()
    plan_id, job_id, run_id = plan.id, job.id, run.run_id
    assert require_completed_run(db, transition.id, run_id)[0].id == job_id
    assert len(proposal_from_run(run, "development_and_ams").topics) == 3
    db.execute(delete(Transition).where(Transition.id == transition.id))
    db.commit()
    db.expire_all()
    for model, key in ((AmplifyPlanSource, plan_id), (BackendPlan, plan_id), (AmplifyJob, job_id), (WorkflowRun, run_id)):
        assert db.get(model, key) is None


def test_sqlserver_outer_rollback_contains_legacy_service_commits():
    database = os.getenv("KT_TEST_LOCALDB")
    if not database:
        pytest.skip("Set KT_TEST_LOCALDB to run SQL Server rollback verification")
    engine = create_database_engine(localdb_url(database))
    try:
        with engine.connect() as connection:
            if "backend_plans" not in inspect(connection).get_table_names():
                pytest.skip("Rollback verification requires the initialized target schema")
            connection.rollback()
            transaction = connection.begin()
            try:
                with Session(bind=connection, join_transaction_mode="rollback_only") as db:
                    transition = Transition(
                        name="SYNTHETIC rollback probe", start_date=date(2026, 11, 2),
                        end_date=date(2026, 11, 6), total_duration_days=5,
                        shadow_days=1, reverse_shadow_days=1, daily_kt_hours=2,
                    )
                    db.add(transition)
                    db.commit()
                    transition_id = transition.id
                    data = PlanningProposal.model_validate(proposal())
                    plan = BackendPlan(
                        transition_id=transition_id, source_bundle="Synthetic", source_files=[],
                        proposal=data.model_dump(),
                    )
                    db.add(plan)
                    db.commit()
                    assert execute_plan(db, plan, data)["scheduled_hours"] == 6
                    db.commit()
            finally:
                transaction.rollback()
        with engine.connect() as connection:
            assert connection.scalar(select(Transition.id).where(Transition.id == transition_id)) is None
            assert connection.scalar(select(KTSession.id).where(KTSession.transition_id == transition_id)) is None
            assert connection.scalar(select(KTTrackingActivity.id).where(KTTrackingActivity.transition_id == transition_id)) is None
    finally:
        engine.dispose()
