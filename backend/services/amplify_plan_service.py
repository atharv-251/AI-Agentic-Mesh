import json

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.models import AmplifyJob, AmplifyPlanSource, WorkflowRun
from backend.routers.workflow_runs import AGENTS, RunSnapshot
from backend.schemas.backend_plan import PlanningProposal


def require_completed_run(db: Session, transition_id: str, run_id: str) -> tuple[AmplifyJob, WorkflowRun]:
    job = db.query(AmplifyJob).filter_by(
        transition_id=transition_id, remote_run_id=run_id, status="accepted",
    ).first()
    run = db.get(WorkflowRun, run_id)
    if job is None or run is None or run.transition_id != transition_id:
        raise HTTPException(status_code=409, detail="A saved accepted Amplify submission and its imported result for this KT are mandatory")
    snapshot = RunSnapshot.model_validate(run.snapshot)
    agents = {step.agent_id for step in snapshot.steps
              if step.node_type == "agent" and step.status == "completed" and step.result and step.result.strip()}
    if str(snapshot.run_id) != run.run_id or run.status != "completed" or snapshot.status != "completed" or agents != set(AGENTS):
        raise HTTPException(status_code=409, detail="All seven Amplify agents must have completed with outputs before operational review")
    return job, run


def require_plan_source(db: Session, plan) -> AmplifyPlanSource:
    source = db.get(AmplifyPlanSource, plan.id)
    if source is None:
        raise HTTPException(status_code=409, detail="This is a historical backend-only record. New execution and delivery require mandatory Amplify provenance; create a new KT workspace")
    require_completed_run(db, plan.transition_id, source.run_id)
    return source


def proposal_from_run(run: WorkflowRun, category: str) -> PlanningProposal:
    """Adapt the known agent output contract; never call a second planning model."""
    snapshot = RunSnapshot.model_validate(run.snapshot)
    try:
        outputs = {
            step.agent_id: json.loads(step.result)
            for step in snapshot.steps if step.node_type == "agent" and step.agent_id in (165, 166)
        }
        profile = outputs[165]["project_profile"]
        people_output = outputs[166]
        leaves = people_output["knowledge_plan"]["leaf_activities"]
        uncertainties = [
            "Result transfer is a manually imported, unverified snapshot, not an authenticated result API.",
            "Review workspace dates, capacity, category and intended levels against the Amplify outputs.",
            "Backend recalculation may propose different calendar slots; Amplify's original proposal is preserved.",
        ]
        levels = sorted({level for leaf in leaves for level in leaf["applicable_kt_levels"]})
        topics = []
        for leaf in leaves:
            topic_name = leaf["hierarchy"]["topic"]
            classification = leaf["hierarchy"]["category"]
            allowed = {"functional", "business", "support_process", "technical", "development", "database", "ams_operations", "integration"}
            if classification not in allowed:
                uncertainties.append(f"Topic classification required: {topic_name}. Amplify category '{classification}' has no exact operational taxonomy match. Choose its category before saving.")
                classification = "unclassified"
            topics.append({
                "name": topic_name, "category": classification,
                "hours": leaf["estimated_hours"], "evidence": leaf["source_ref"],
            })
        people = []
        for person in people_output["stakeholders"]:
            role = person["role"].lower()
            level = person.get("support_level") if role == "sme" else person.get("intended_level")
            people.append({
                "name": person["name"], "role": role, "level": level,
                "email": person.get("email"), "evidence": person["source_ref"],
            })
        return PlanningProposal.model_validate({
            "project_name": profile["project_name"]["value"],
            "business_purpose": profile["purpose"]["value"], "category": category,
            "intended_levels": levels, "technology_stack": profile["technology"]["value"],
            "environments": [], "support_model": "",
            "integrations": [item["value"] for item in profile["integrations"]],
            "dependencies": [], "risks": [item["risk"] for item in profile["risks"]],
            "topics": topics, "people": people,
            "uncertainties": uncertainties + [
                "Environments, support model and dependencies require review; absent fields were not inferred."
            ],
        })
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError, ValidationError) as exc:
        raise HTTPException(
            status_code=422,
            detail="Amplify output does not match the supported operational mapping contract. Review the original agent outputs; no local model or silent fallback was used.",
        ) from exc
