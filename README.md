# AI Agentic Mesh - KT Transition Intelligence

## Repository setup and publication boundary

This private repository is a clean source snapshot of the Amplify-first KT
Planner standalone application. Its initial branch is `master`; it does not
include the original repository's history or local operational records.

Environment files (including `.env`), workflow tokens, local database selection,
SQLite databases, uploaded documents, generated exports, extracted project data,
binary PDF samples and the proprietary Agentic Blueprint wheel are not published.
The application source, workflow definitions, tests, documentation and compiled
frontend are included. Historical run IDs and migration notes describe earlier
tests; they do not restore those results or databases in a fresh checkout.

Before running:

1. Obtain `agentic_blueprint-1.0.5-py3-none-any.whl` from your approved internal
   package distribution and place it in the repository root. It remains ignored.
   The existing `requirements.txt` references this local dependency; do not fetch
   an unrelated similarly named public package.
2. Install backend requirements and configure a private local `.env` using your
   own approved credentials. Never commit environment files or credentials.
3. Run `run_kt_planner.bat`. The compiled standalone frontend is included. For
   frontend development, run `npm ci`, `npm test` and `npm run build` in `frontend`
   (presentation tests require Node 22.6+; verified on Node 24).
4. Configure your own Amplify workflow access token through the local app.
   Fresh checkouts use SQLite unless SQL Server LocalDB is explicitly configured.
   The original workstation's SQL database and credentials are not transferred.

Amplify execution is mandatory, but automatic result return is not implemented.
The current handoff requires explicit Full JSON import and human review. This
repository is not a claim that the application is hosted inside Amplify.

An Amplify-first Knowledge Transfer (KT) transition workspace. Seven connected
Amplify agents perform planning; the local backend supports reviewed operational
calculations, SQL persistence and professional report delivery. Plans remain
drafts until real evidence and human acceptance are supplied.

**Amplify execution is mandatory, not an optional advisory path.** The former
15-module frontend and independent backend model-intake path are retired from
the served application. Automatic result return is still not connected:
completed agent outputs currently require explicit, unverified manual import.

---

## Documentation Suite (Enterprise Guides)

Complete technical, architectural, and operational manuals are available in the [`docs/`](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs) directory:

The original module/API guides below describe the preserved legacy engines.
The active application boundary and workflow are documented in this README and
[the migration record](./docs/CHAMP_MIGRATION_PLAN.md); legacy operational routers
are no longer registered by the Amplify-first application.

1. [**Architecture Blueprint (`docs/ARCHITECTURE.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/ARCHITECTURE.md):
   - Guiding principles, single deployable service topology, component layout, and security gateway.
2. [**Data Model & Relational Schema Reference (`docs/DATA_MODEL.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/DATA_MODEL.md):
   - Entity-Relationship Diagram (ERD), table specifications, column dictionaries, foreign keys, and indexes.
3. [**REST API Reference (`docs/API_REFERENCE.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/API_REFERENCE.md):
   - Endpoint reference across all 12 stages, JSON payloads, and Controlled Read-Only SQL API (`POST /api/v1/database/query`).
4. [**Deterministic Core Engines (`docs/DETERMINISTIC_ENGINES.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/DETERMINISTIC_ENGINES.md):
   - Mathematical equations, holiday exclusion logic (`holidays.json`), Outlook CSV parser, and conflict algorithms.
5. [**LangGraph Multi-Agent Architecture (`docs/AI_AGENT_WORKFLOW.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/AI_AGENT_WORKFLOW.md):
   - Compiled `StateGraph` pipeline, memory isolation principle, and detailed Agent 1 through 6 execution mechanics.
6. [**Deliverables & Governance Matrix (`docs/DELIVERABLES_MATRIX.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/DELIVERABLES_MATRIX.md):
   - Section 15 deliverables breakdown and column-by-column structure of the 8-sheet master Excel workbook.
7. [**Operations, Deployment & Runbook (`docs/OPERATIONS_RUNBOOK.md`)**](file:///c:/Users/V6P5LAR/Downloads/KT_Planner_V4/docs/OPERATIONS_RUNBOOK.md):
   - Installation guide, single-service deployment, backup/recovery, health checks, and troubleshooting runbook.

---

## Single Deployable Architecture

```
Browser (standalone React / TypeScript workflow workspace)
   │ (HTTP REST)
   ▼
Uvicorn ASGI Server (:8000)
   ▼
FastAPI Application (backend/main.py)
   ├─► API Routers (/api/v1/...)
   ├─► Static SPA Hosting (frontend/dist)
   ├─► Authenticated submission -> Amplify workflow 167 -> seven connected agents
   │      Result return: manual Full JSON import, not live synchronization
   ├─► Mandatory run gate -> human review -> deterministic Python calculations
   ├─► Frozen DOCX (including all seven original outputs) -> approved SMTP delivery
   └─► Authoritative database (SQLite by default; verified SQL Server LocalDB option)
```

---

## Quick Start Guide

### 1. Launch Single Deployable Service

Before starting the backend, create a local `.env` in the repository root
(beside this README), then set `LLMAAS_API_KEY` to your real LLMaaS virtual key.
If the file already exists, edit it rather than overwrite it. The backend
loads this file through `python-dotenv`; restart the backend after changing
the key. An empty key does not satisfy the SDK's startup requirement.
Keep the key out of chat, frontend/Vite variables and source control.
The repository ignores `.env` in Git.

Double-click [`run_kt_planner.bat`](./run_kt_planner.bat) or run:
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open your browser at **`http://localhost:8000`**.

### Saved KTs (local frontend)

The landing page is the **KT / NEXUS** transition portfolio: a dark graphite,
violet-accented standalone command centre for **Retired - Workflow 2**
(Amplify workflow 167). Workflow 168 was copied
into 167 and the saved exports were compared: identical except name/slug.
The main workflow 166 and original 168 were not changed.

Choose **Planning workspace** on a KT card. There is one planning path:

The workspace has five focused sections, not a long stream of raw responses:

- **Overview:** selected snapshot, reported agent execution, workspace capacity,
  reported duration, seven-agent pipeline, planning dates and run lineage.
  Agent execution is never presented as KT completion.
- **Agent intelligence:** seven categories for profile, people/knowledge,
  sessions/capacity, readiness, communication drafts, evidence and report.
  JSON is displayed as labelled facts, source citations, lists and nested record
  cards. Core business content comes first; every other supplied field remains
  visible, including unfamiliar future fields. False, zero, null, empty lists
  and missing agent outputs retain distinct meanings. Malformed structured
  output shows a warning and preserves the original response.
- **Launch & import:** source upload, actual submission history and immutable
  manual Full JSON import. A successful import opens agent intelligence.
- **Review & delivery:** readable operational inputs, explicit topic-category
  selectors, reviewer approval, saved calculations and controlled report email.
  Advanced JSON editing remains available for other corrections. Changing inputs
  resets operational approval. Historical backend-only records stay read-only.
- **Connection:** an explanatory current-data-flow diagram, direct-SQL versus
  hosted-ingestion requirements, manual-return limitation and backend token setup.

When no run is specified, the most recently imported snapshot is selected and
labelled in the run selector. It is not assumed to be the latest cloud run.
Original agent strings remain available under **Original agent response**.
The executive-report preview formats headings, emphasis, lists, code and basic
Markdown tables, while the download remains the original Markdown. Model output
is rendered as text, not executable HTML. Layouts adapt to mobile; wide report
tables scroll within their own container.

#### Mandatory Amplify execution

Configure the workflow token, upload documents and start Amplify as described
below. Complete the cloud run/review and import Full JSON. Select that saved run,
then open **Review & delivery** and choose **Prepare review from Amplify outputs**.
The backend requires an
accepted submission for the same KT/run and completed, nonempty outputs from all
seven agents. An accepted job alone, failed/partial output, a foreign KT run or
an arbitrary unsubmitted snapshot cannot unlock operational processing.

The deterministic adapter supports the inspected agent165 project-profile and
agent166 people/leaf-activity JSON contracts. Unsupported contracts fail visibly;
there is no second planning-model call or silent fallback. Free-text categories
without an exact operational-taxonomy match become `unclassified`, which blocks
execution until the reviewer explicitly maps them. Missing environments, support
model and dependencies remain empty with review notices. Review all KT levels,
effort, evidence and workspace settings; the normalized calculation is not an
exact replay of proposed cloud calendar slots.

Enter the reviewer name, approve operational writes, and choose **Validate & save
reviewed Amplify plan**. Original deterministic profile, hierarchy, KT-level,
capacity, scheduling, tracking and validation services save operational records
in one outer transaction. A downstream failure rolls back those writes. No
generic capacity-expansion topics are added to conceal gaps. Inspect sessions,
blockers and the Word report, including the full seven-agent source appendix.
Execution completion is not KT completion, release or acceptance.

Expand **Approve report email**, enter recipients/reviewer and approve the exact
draft attachment. Existing backend `KT_SCHEDULER_*` SMTP settings are reused.
The saved receipt records approver, Message-ID, recipients and attachment hash.

`backend_plans` holds one execution per KT. `amplify_plan_sources` immutably links
new plans to their submitted job and imported run; startup creates this additive
table without rewriting existing plans. Historical backend-only plans remain
explicitly labelled read-only records: report download and delivery receipts
are preserved, but new execution, reclassification as Amplify work and further
delivery are blocked. A different cloud run on the same KT does not retroactively
give a historical plan Amplify provenance. Existing operational records are
never overwritten by this path; use a new workspace for a changed plan.
Preparation/execution claims are persisted before work. An interrupted
`preparing`/`running` state requires operator inspection; it is not automatically
retried. A failed, rolled-back execution can be corrected and resubmitted.
Inputs and report are frozen on successful execution. Later manual module edits
do not silently regenerate that historical report.

SMTP acceptance is not proof of inbox delivery. Partial/unknown sends remain
explicit and cannot be retried automatically, preventing accidental duplicates.
Sending a draft report does not approve the transition or send meeting invites.
Real transcripts, calendars, leave records and completion/acceptance evidence
still have to be supplied. No artificial progress is created.

Local-only endpoints under `/api/v1/transitions/{id}/backend-plan`:
`GET` saved state, `POST` multipart UUID `request_id` and `amplify_run_id`
(not source uploads), `POST /execute` reviewed JSON plus
`approve_operational_write: true`, `GET /report` DOCX, and `POST /email` recipients,
approver and `approve_email: true`. These APIs enforce the existing loopback
client/Host/Origin guard; they are not a substitute for production authentication.

#### Starting Amplify and returning its results

1. Expand **Connection settings / workflow token** and configure a token from
   Amplify Profile -> Workflow access token. Tokens act as their creating user.
   The setup form stores the token with Windows user-scoped DPAPI encryption in
   a Git-ignored local file. It is not returned by the API or stored in browser
   storage. Alternatively set backend `AMPLIFY_WORKFLOW_TOKEN`; this environment
   value takes precedence. Never use a Vite variable for credentials.
2. Upload 1-10 BRDs/supporting documents, add optional planning instructions and
   explicitly confirm transmission. Click **Start planning in Amplify**.
3. The backend extracts text, stores a job and submits a real authenticated
   webhook request to workflow167. The saved receipt contains its remote run ID.
4. Open **Review run in Amplify** for actual progress and human approval.
5. Open that run's Output -> Full JSON, copy it and use **Bring the reviewed
   result into this KT**. This last step is explicitly manual. The dashboard
   displays the report, individual agent outputs and review records, with a
   Markdown report download.

**Live submission works; automatic result return is not connected.** No supported
status/result API documentation or approved reachable callback was available.
Refreshing saved jobs reads the local database, not Amplify's current status.
Accepted means only that submission was acknowledged. Manual snapshots are
unverified data, not proof of completion/release. Missing agent outputs remain
missing. URL fragments preserve selected KT/run across reload and Back/Forward.

Supported sources: UTF-8 TXT/MD/JSON/CSV/VTT, DOCX, XLSX (cached formula values)
and text-based PDF. Scanned PDFs require OCR first. Limits: 5 MB per file,
80,000 extracted characters combined, 200 PDF pages, 5,000 spreadsheet rows,
20 MB expanded Office archive. Unsupported/empty/oversized sources fail visibly;
nothing is silently truncated. Extracted text and source filename/size/hash
metadata persist with the job in `amplify_jobs`. They do not automatically populate
the existing module document/profile/people/session tables.

The backend generates a durable request ID before submission. Repeating that
request returns its existing job, not a second remote run. Remote HTTP failures,
unrecognized receipts and uncertain transport failures are distinct saved states.
There is no automatic retry after an ambiguous timeout; inspect Amplify before
starting another request. The remote service's own idempotency is not established.

Local run-record endpoints (also described by `/docs`):

- `GET /api/v1/transitions/{id}/workflow-runs`
- `POST /api/v1/transitions/{id}/workflow-runs` (Full JSON snapshot)
- `GET /api/v1/transitions/{id}/workflow-runs/{run_id}`
- `GET /api/v1/transitions/{id}/workflow-runs/{run_id}/report`
- `GET /api/v1/amplify/connection`
- `PUT /api/v1/amplify/connection` (local credential setup; never returns token)
- `POST /api/v1/transitions/{id}/amplify-jobs` (multipart sources, instructions, UUID request_id)
- `GET /api/v1/transitions/{id}/amplify-jobs`
- `GET /api/v1/transitions/{id}/amplify-jobs/{job_id}`

The POST requires UUID `run_id`, `workflow_id: 167`, `project_id: 77`, `status`,
and `steps`. Each step contains `node_key`, `node_type` (`start`, `agent`,
`approval`, `end`), `status` and optional `agent_id`, `agent_name`, string
`result`, and positive `attempt`. Optional `duration_ms` is non-negative.
Agent IDs must be unique members of `[165,166,167,168,144,142,143]`.
Unknown platform metadata is discarded; output strings are retained verbatim.
Limits: 50 steps, 100,000 characters per output, 500,000 combined output
characters. Duplicate runs return 409; invalid snapshots 422; mismatched KT
lookups 404. Import timestamps are UTC. Importing never updates planner module
records, sends mail, executes agents, or grants approval.

**Workflow167 configuration:** authenticated Webhook/API trigger at
`/api/workflow-hooks/kt-planner-workflow-2`, with workflow memory explicitly off.
The backend sends `Authorization: Bearer <workflow-access-token>` and a JSON
body containing `transition_id` and `document_bundle`. Both inputs are declared
and explicitly interpolated in the intake task. This was tested against the
real platform, not just a mocked API. Workflow168 remains the manual baseline;
main166 remains unchanged. The workflows share agent references, not cloned agents.

Synthetic test run `8055c745-2543-41f2-b501-f21bebfd3a05` completed all seven agents
in 205,909 ms. Its real report was manually imported into the synthetic local KT.
The portal recorded draft-review approval; the assistant did not submit it.
No messages/invitations were sent. Proposed math was 3 KT days, 6 target hours,
6 leaf hours, zero gap; release remained blocked and transcript evidence absent.

This is not a full automatic migration of the original 15-stage engines. Import
alone does not populate operational tables; the separate mandatory-run gate,
review and explicit approval above are required. Rechecked native Start/End
configuration: the Start API acknowledges queued work; End supplies completion
status/message within the workflow result. WaaS calls another platform workflow,
not an external Python service. No documented native synchronous return/polling
contract was found. The SQL catalogue is read-only, not LocalDB hosting or a
result-writing bridge. Automatic result return remains blocked pending a
supported result API or an approved hosted integration. No hidden APIs, browser
credentials or tunnel are used. Production also requires authentication and
per-KT authorization. Keep credentials backend-only and keep this service local.

The home screen lists saved transitions from the selected authoritative database,
with name/ID search, status filters and last-updated/name sorting.
Choose **Planning workspace** for the standalone app. There is no legacy
stepper, module switch or Scheduler/Tracker/Analytics shortcut. Old
`#transition=...&step=1..15` bookmarks are replaced with the same KT's workflow
workspace, never the old module screens. Selected KT/run remains in the URL
fragment for reload and Back/Forward navigation.

The list shows current records, not historical plan snapshots. Its update timestamp
belongs to the transition record and does not track every document/session change.
Opening a KT does not execute agents or send email. Existing data, reports and
service code are preserved; legacy module pages and operational API routers are
not exposed by this application. Missing API paths return explicit errors, not
a successful HTML fallback.

This is a **shared local workspace**, not an authenticated "My KTs" portal. All
records returned by the backend are visible; per-user isolation and versioned
audit history are not implemented. Keep the service local for this setup (use
`--host 127.0.0.1`), rather than exposing it to a shared network. Amplify cannot
call localhost without an approved service connection; no such connection is
created by this frontend.

After frontend changes, run `npm run build` from `frontend` before using the
FastAPI-served UI. For development, run `npm run dev` there; Vite proxies `/api`
to the backend on port 8000.

Run `npm test` from `frontend` for presentation-helper tests using Node's
built-in test runner (Node 22.6+ with type stripping; verified on Node 24).
No browser fixture writes or remote Amplify execution are needed to test
presentation of missing, malformed or future agent fields.

### SQL Server LocalDB migration

The default remains SQLite for a fresh checkout. This worktree was explicitly
migrated to `(LocalDB)\MSSQLLocalDB`, database `kt_planner_amplify_local`.
The Git-ignored `.kt-database.json` selects it persistently:

```json
{"provider":"sqlserver-localdb","database":"kt_planner_amplify_local"}
```

Requires Windows, the SQL LocalDB instance, ODBC Driver 18 and `pyodbc`.
Windows integrated authentication is used; no SQL password is stored.
The local selection is intentionally not committed. `/health` identifies the
active provider. Failure to open the selected database fails explicitly;
there is no silent fallback to the old SQLite snapshot.

For a **new, empty** destination database, stop the backend/writers first, then:

```powershell
python -m backend.migrate_localdb --database kt_planner_amplify_local
```

This creates an integrity-checked SQLite backup under ignored `exports`, copies
all registered tables in dependency/parent order and compares row counts and
canonical SHA-256 fingerprints before committing. It refuses a destination with
user tables and never overwrites source data. It does not activate the target;
create the selection file only after verification. Unicode strings and timestamp
microseconds are preserved. SQL Server rejects the model's multiple cascade
paths, so dialect-specific set-based delete triggers preserve CASCADE/SET NULL
behavior while foreign keys remain enforced. Transactional SQL tests cover
hierarchical deletion, stakeholder SET NULL, Unicode and original planning services.

The preserved SQLite file/backup is a **pre-cutover snapshot**, not a live replica.
Do not remove the selection file as a casual rollback after new SQL writes:
stop writers and perform a separately verified reverse migration/recovery first.
LocalDB runs under this Windows user and is not a hosted/multi-user production
database. Amplify's read-only SQL tool does not host a database, write these
records or make a workstation LocalDB instance reachable from the cloud.

### 2. Run Automated Verification Tests
```powershell
$env:KT_TEST_LOCALDB = "kt_planner_amplify_local"
python -m pytest tests\test_backend_planning.py tests\test_database_migration.py tests\test_localdb.py tests\test_amplify_integration.py tests\test_workflow_runs.py tests\test_modules.py tests\test_analytics.py tests\test_capacity.py tests\test_single_deployable.py -q
# 52 passed; LocalDB-specific tests skip when KT_TEST_LOCALDB is unset.
```

---

## Compliance With Blueprint Requirements

### Amplify-native KT transition planning

Existing Amplify workflow **168**, **Retired - Workflow**, has a separate
seven-agent advisory planning/review definition in
[CHAMP_KT_TRANSITION_WORKFLOW.yaml](docs/CHAMP_KT_TRANSITION_WORKFLOW.yaml).
Users attach BRDs and planning inputs in Amplify, review a readable KT overview,
and approve/reject the draft there. It does not call the local application.
See [migration scope and usage](docs/CHAMP_MIGRATION_PLAN.md) for the stage map
and verified limitations. This adapts planning responsibilities, not the Python
engines or React UI: no calendar verification, real invitation sending, external
database writes, generated export files or local-dashboard updates are enabled.
Do not import the older transcript-test YAML as the current transition flow.

### Tab 14: Transcript-First KT Tracking

Choose the meeting date and a Teams `.vtt` file, then select **Read transcript**.
Previously uploaded transcripts can also be reviewed without uploading again.
The review extracts speakers, the timestamp span, discussion highlights, questions,
follow-up statements, potential concerns, and document mentions locally.
Evidence excerpts include the speaker and the containing speaker-turn time range.

Review the suggested activities and select **Confirm meeting**. Only activities
scheduled for the selected day are checked by default; additional keyword matches
are suggestions, not proof of coverage. Confirmation links the evidence to the
selected activities and changes planned activities to in progress. Reconfirming
the same transcript replaces its activity links without duplicating the meeting.
Other statuses, manual records, and final acceptance remain unchanged.

The **Meetings** view retains reviewed evidence; **Activities** provides search,
status filters, and optional corrections/sign-off. Extraction is deterministic,
not an LLM assessment: speakers are not a full attendance list, transcript duration
is not verified working time, questions may already be answered, and document
mentions do not prove delivery. VTT relative timestamps do not establish a calendar
date, so the meeting date is supplied by the reviewer.

Review API: `GET /api/v1/transitions/{id}/kt-tracker/transcripts/{document_id}/review?meeting_date=YYYY-MM-DD`.
Confirm using `POST` to the same path with `meeting_date` and `activity_ids`.

**AI follow-up analysis:** Select **AI analysis** in a transcript review or an
expanded saved meeting. The configured Agentic Blueprint LLM reviews the full
cleaned transcript for unresolved issues and risks, including later answers,
and proposes questions/actions for the next call. Findings include priority,
resolution uncertainty, and source quotes/timestamps. Human review is required;
the assessment does not change progress or acceptance. Successful results are
stored per transcript; **Run again** refreshes them. Provider failures retain any
previous result and do not fall back to fabricated AI output.

This action requires a valid `LLMAAS_API_KEY` and connectivity to the configured
LLM provider. Replace local setup credentials in the environment configuration
and restart the server; never share credentials in chat. Only clicking the action
sends transcript speech and speaker labels to that provider. The existing
**Read transcript** extraction remains local. Full transcripts above the analysis
size limit are rejected rather than silently truncated.

AI endpoint: `POST /api/v1/transitions/{id}/kt-tracker/transcripts/{document_id}/ai-analysis`
(`?refresh=true` for regeneration). The additive `kt_transcript_assessments` table
is created by the application's existing startup schema initialization.

### Tab 15: Executive Dashboard / Analytics

The read-only dashboard combines the preceding 14 stages for the selected transition.
Date range (scheduled dates, inclusive), domain, KT level, SME, receiver, and activity
status filters apply to delivery metrics, charts, session-linked findings, and CSV export.
The risk register also supports severity, source, and text search. Transition-wide
readiness, capacity, profile risks, validation checks, and unlinked AI assessments
are explicitly outside those delivery filters. Source links open the owning tab.

- Completion is `sum(planned hours * recorded progress / 100) / sum(planned hours)`.
   Cancelled sessions are excluded; no scheduled hours means N/A, not zero or complete.
   Sessions without tracker records use their schedule completion status, otherwise zero progress.
- Completed session count, actual hours, and explicit final acceptance are separate measures.
   Transcript links and invitation records do not prove attendance, delivery, or acceptance.
- The delivery chart is current progress grouped by scheduled date, not historical velocity.
   Overdue means an unfinished activity before today's date in the transition timezone.
- Blockers are recorded tracker text or an on-hold status. Other signals include recorded
   risks, overdue activities, missing participants, and saved scheduling conflicts.
   Import/Graph metadata is not itself a conflict. Validation checks are rule-based,
   not a fresh calendar availability computation.
- Saved AI findings are advisory, may be stale, and are counted once per transcript finding
   even when linked to multiple sessions. Signals from different sources may overlap.
   Mitigations are proposals, not agreed actions; no new AI call or status mutation occurs.

API: `GET /api/v1/transitions/{id}/analytics`, with optional `start_date`, `end_date`,
`domain`, `level`, `sme_id`, `receiver_id`, and `status` query parameters.
Verification: `python -m pytest tests/test_analytics.py -q` and the frontend build.

### Platform Requirements

- [x] **Single Source of Truth**: SQLite database (`kt_planner.db`) holds all projects, hierarchy, evaluations, and schedules.
- [x] **Holidays Management**: Strictly driven by `holidays.json`. Zero hardcoding in Python.
- [x] **Capacity Mathematics**: Available KT Days = Duration - Shadow - Reverse Shadow; 100% capacity balance required.
- [x] **6-Tier Taxonomy**: Application $\rightarrow$ Domain $\rightarrow$ Capability $\rightarrow$ Process $\rightarrow$ Topic $\rightarrow$ Subtopic.
- [x] **KT Level Evaluation**: L1, L2, L3, and composite combinations evaluated independently for all granular topics.
- [x] **Outlook Calendar Ingestion**: Standard CSV headers parsed with optional subject privacy masking.
- [x] **Conflict-Free Scheduling**: Sequencing L1 $\rightarrow$ L2 $\rightarrow$ L3 sessions, skipping weekends, bank holidays, and busy events.
- [x] **LangGraph AI Orchestrator**: Compiled `StateGraph` pipeline with Agents 1 through 6.
- [x] **Controlled Database Gateway**: `POST /api/v1/database/query` allows read-only `SELECT` queries while blocking mutations.
- [x] **Deliverables Package**: 8-sheet Master Excel Workbook (`.xlsx`) and calendar CSV stream.
