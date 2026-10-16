from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PlanningTopic(StrictModel):
    name: str = Field(min_length=1, max_length=200)
    category: Literal["unclassified", "functional", "business", "support_process", "technical", "development", "database", "ams_operations", "integration"]
    hours: float = Field(gt=0, le=1000, allow_inf_nan=False)
    evidence: str = Field(min_length=1, max_length=2000)


class PlanningPerson(StrictModel):
    name: str = Field(min_length=1, max_length=255)
    role: Literal["sme", "receiver"]
    level: Literal["L1", "L2", "L3"]
    email: str | None = Field(default=None, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    evidence: str = Field(min_length=1, max_length=2000)


class PlanningProposal(StrictModel):
    project_name: str = Field(min_length=1, max_length=255)
    business_purpose: str = Field(max_length=5000)
    category: Literal["development_and_ams", "development", "ams_operations"]
    intended_levels: list[Literal["L1", "L2", "L3"]] = Field(min_length=1, max_length=3)
    technology_stack: list[str] = Field(max_length=100)
    environments: list[str] = Field(max_length=100)
    support_model: str = Field(max_length=100)
    integrations: list[str] = Field(max_length=100)
    dependencies: list[str] = Field(max_length=100)
    risks: list[str] = Field(max_length=100)
    topics: list[PlanningTopic] = Field(min_length=1, max_length=100)
    people: list[PlanningPerson] = Field(max_length=100)
    uncertainties: list[str] = Field(max_length=100)

    @model_validator(mode="after")
    def unique_inputs(self):
        if len(set(self.intended_levels)) != len(self.intended_levels):
            raise ValueError("Intended levels must be distinct")
        names = [topic.name.casefold().strip() for topic in self.topics]
        if len(set(names)) != len(names):
            raise ValueError("Topic names must be distinct")
        people = [(person.name.casefold().strip(), person.role) for person in self.people]
        if len(set(people)) != len(people):
            raise ValueError("People must be distinct within each role")
        return self


class ExecutePlanRequest(StrictModel):
    proposal: PlanningProposal
    reviewed_by: str = Field(min_length=1, max_length=100, pattern=r"\S")
    approve_operational_write: Literal[True]

    @model_validator(mode="after")
    def classified_topics(self):
        if any(topic.category == "unclassified" for topic in self.proposal.topics):
            raise ValueError("Map every unclassified Amplify topic to an operational category before execution")
        return self


class SendPlanRequest(StrictModel):
    recipients: list[str] = Field(min_length=1, max_length=20)
    approved_by: str = Field(min_length=1, max_length=100, pattern=r"\S")
    approve_email: Literal[True]
