# KT Planner migration to CHAMP / Amplify IT

## Current: mandatory Amplify, standalone workspace only - 16 October 2026

### Standalone presentation redesign

User requested a futuristic, professional interface and a clearer explanation
of how Amplify and the database connect. Replaced the long single-page response
stream with the KT / NEXUS portfolio and a five-section transition workspace:
Overview, Agent intelligence, Launch & import, Review & delivery, Connection.
Preserved mandatory execution, historical labels and all approval boundaries.

The agent explorer presents every supplied field from all seven agents:
profile/source citations, people/knowledge/levels, capacity/sessions,
readiness/handover, communication drafts, tracking/evidence and the executive
report. Core fields appear first; unknown fields are retained. Original strings
remain inspectable. Missing/invalid output is explicit, not filled in.
Markdown report preview handles basic tables, emphasis, lists and code without
executing embedded HTML. Operational proposal review now has readable fields and
explicit category selectors; advanced JSON corrections remain available.

The Connection view shows the actual outbound webhook and manual return, not an
imaginary SQL bridge. Direct Amplify-to-SQL writes would require a supported
write-capable connector and approved reachable database. The inspected SQL tool
is read-only and local workstation LocalDB is not cloud-reachable. Recommended
future return is a hosted authenticated ingestion API that validates/stores run
results for the app to fetch. This is an architectural option only, not deployed
or approved connectivity.

Presentation verification:

- Seven Node built-in presentation tests passed; TypeScript/Vite production
  build passed. No new package dependencies.
- All 60 targeted backend/SQL integration tests passed, including actual LocalDB
  transactional tests; mandatory Amplify and delivery boundaries are unchanged.
- Browser compared all 613 primitive field values from the real six structured
  agent responses with the visible formatted content: no missing values.
  The seventh agent's full 11,812-character Markdown report is preserved.
- Temporary browser-only response fixtures verified malformed JSON warnings,
  missing-agent empty states, Markdown table/emphasis formatting and literal
  embedded HTML rendering as text. Fixtures were removed; no saved run changed.
- Operational-review fixture verified readable inputs, three category selectors,
  unchanged JSON fields, approval reset after reclassification and disabled
  unapproved save. No execution or delivery request was submitted.
- 35 layout checks at 390/768/1440 pixels across all agent categories and workspace
  sections, portfolio and creation dialog found no document-level horizontal
  overflow. Wide report tables remain locally scrollable.
- Section navigation preserves selected agent, typed launch instructions and
  action-component state instead of remounting forms/resetting request IDs.
  Actual empty workspace shows no invented results and locked preparation.
- No new cloud run, planning write, message or email was triggered for this
  redesign. The existing local service serves the rebuilt UI independently of
  VS Code.

The user explicitly rejected the backend-owned architecture below and clarified:
keep the new standalone app, close the 15-module app, and require Amplify
execution. Earlier sections after this entry are a chronological research and
test record, not current architecture, even where their original headings say
"current".

Active path:

`documents -> authenticated Amplify167 submission -> seven connected agents
-> human cloud review -> explicit manual Full JSON import -> run selection
-> deterministic adapter -> reviewed operational categories/inputs
-> atomic SQL calculations/persistence -> frozen Word report -> approved SMTP`.

- Removed legacy page imports, stepper and old module links from the served SPA.
  Old step bookmarks redirect to the same KT's standalone workflow workspace.
  Preserved original pages, Python service code and all existing data.
- Amplify upload/run is primary, not hidden under optional details.
- Removed backend model intake. The operational preparation endpoint requires
  UUID `amplify_run_id`, an accepted submission for this KT and the corresponding
  imported completed run with all seven completed/nonempty agent outputs.
  Independent legacy operational routers are no longer registered; direct HTTP
  calls cannot start their alternate planning engines.
- Added `amplify_plan_sources` linking new plans to exact job/run records without
  altering or retroactively populating existing `backend_plans`.
- No local planning-model call: deterministic mapping of inspected agent165/166
  contracts. Unknown shapes fail visibly. Unknown category names become
  `unclassified`, not guessed functional categories; execution requires explicit
  reviewer classification. Review KT levels/settings and scheduling differences.
- All original seven-agent output strings are frozen with new operational
  results and included in the professional Word attachment as a source appendix.
- Historical plan `7fe10826-f366-440f-933d-0cc18bf5b0b6` remains backend-only,
  read-only, with its original report/download and delivery receipt intact.
  The real cloud run in the same KT does not relabel that earlier execution.
  No new cloud run, email or invitation was sent for this correction.

### Native result-return recheck

Inspected workflow167's visible Start/End Config and node palette without
saving workflow changes. Start documents asynchronous inbound POST submission.
End exposes completion status and an optional message "returned with the
workflow result"; it does not expose a documented response-retrieval contract.
WaaS invokes a subworkflow; Code is JavaScript transformation. No supported
native external result-return mechanism was found. Previously verified SQL tool
is read-only and cannot write local operational records. No hidden endpoints,
browser-session credentials, external callback deployment or tunnel were used.

Consequently, **automatic result synchronization is not implemented or claimed**.
The currently supported handoff remains explicit manual import, unverified as
to authenticity, followed by human review. A local accepted submission provides
real run association, not cryptographic proof of pasted agent completion.
This is a working bounded handoff, not unattended production parity for every
original Python module. Hosted connectivity, authentication/authorization and
a supported output contract remain production requirements.

### Correction verification

- 60 targeted tests passed, including actual transactional SQL Server LocalDB
  tests, provenance/cascade behavior, seven-agent prerequisites, wrong KT,
  missing/unaccepted submission, missing/failed/empty outputs, gate rechecks
  before execution/email, atomic rollback, report bytes and SMTP audit.
- Production TypeScript/Vite build passed. Legacy analytics/module chunks are
  absent from the new build.
- Browser verified all 15 legacy step bookmarks redirect to the standalone
  workspace, one Amplify upload control, no independent planner or historical
  resend action, preserved historical report download and no visible alerts.
- At a 390-pixel viewport, workspace and creation dialog had no horizontal
  overflow. Creation exposes category, date range, shadow/reverse-shadow days
  and daily hours; India/default-shift limitations are explicitly displayed.
- Deterministic adapter read the existing actual cloud run
  `8055c745-2543-41f2-b501-f21bebfd3a05` without writes/model calls: three
  topics, two people, three unclassified categories requiring review.
- Restarted the standalone service; health identifies SQL Server LocalDB.
  Historical report hash and `accepted_by_smtp` receipt remain unchanged.

## Historical, superseded: authoritative Python backend, SQL LocalDB and report email - 16 October 2026

User requested a reliable, non-demo execution path and authorized a full local
SQL Server migration. Chosen architecture is explicitly backend-owned planning,
not a claim to have fixed the unavailable Amplify result API:

`documents -> backend model intake -> reviewed typed proposal -> original Python
services -> SQL records/dashboard -> reviewed DOCX email`.

The seven-agent Amplify workflow remains available as an optional advisory path.
No browser-session credentials, undocumented APIs, cloud callback or tunnel were
introduced. Main166/original168 and shared cloud agent definitions were untouched.

Verified the visible Amplify **SQL Database** tool: Describe Table, Find Columns,
List Tables, Run SQL Query and Sample Rows, all read-only. The catalogue explicitly
refuses INSERT/UPDATE/DELETE/DDL. It is not SQL hosting or a result-writing bridge.
No unrelated corporate database was queried through that tool.

Backend intake used the configured model on the two synthetic source documents,
returned schema-valid people/topics/evidence/uncertainties and persisted review
state. User explicitly approved L2-only execution and sending the resulting draft
to `atharva.utekar@vwgds.in` and `vivek.chaurasia@vwgds.in` after verification.
Existing SME and receiver were both L2. No human release approval was inferred.

Implemented:

- One persistent backend execution per KT, explicit local-only approval APIs.
- Strict proposal contract, finite positive effort, distinct topics/people and
  mandatory reviewer/operational-write approval.
- Original profile/hierarchy/level/capacity/scheduling/validation services plus
  shared tracker initialization. All operational writes run in one outer
  transaction despite legacy services committing internally.
- No automatic overwrite of existing operational data and no automatic retry
  of interrupted work. Failed execution rolls back operational writes.
- No generic topic expansion just to conceal capacity gaps. Fixed creation of
  unused domain nodes, which otherwise became phantom schedulable leaf topics.
- Full Word report from the execution snapshot, all ten sections including
  source hashes, hierarchy, learning outcomes, people, effort, sessions,
  validation, missing evidence and draft/release boundaries.
- SMTP attachment delivery reuses existing backend settings. Durable one-attempt
  claim, exact attachment hash, approver/Message-ID/recipient audit; partial and
  unknown sends are explicit and never automatically retried.
- Backend-first planning UI, with optional Amplify advisory controls separate.

### SQL Server cutover

`(LocalDB)\MSSQLLocalDB`, database `kt_planner_amplify_local`, was ONLINE and
empty. Initial schema probe exposed SQL Server multiple-cascade-path rejection;
all probe DDL rolled back. Added dialect-specific set-based delete triggers to
preserve the existing CASCADE/SET NULL semantics with enforced foreign keys.
Added Unicode binding/storage and DATETIME2(6) timestamp fidelity. The first
copy correctly refused to commit because SQL DATETIME rounded source timestamps;
fixed precision, verified it and reran successfully.

Stopped the backend before copying. Created integrity-checked SQLite backup
`exports/sqlite_before_localdb_20261016T124908960711Z.db`. Copied all18tables;
row counts and canonical SHA-256 fingerprints matched before target commit.
Preserved2transitions,1Amplify job,1imported cloud snapshot and1reviewable backend
plan; remaining operational tables were empty at cutover.

Enabled the target through Git-ignored `.kt-database.json`, using Windows
integrated authentication and ODBC Driver18. No SQL credentials or excluded
environment files were read/changed. Startup fails on a selected-database error;
there is no silent SQLite fallback. The old SQLite database is now a historical
pre-cutover snapshot, not a replica or a safe instant rollback after new SQL writes.
LocalDB remains single-workstation/user infrastructure, not hosted production SQL.

### Real execution and delivery

- KT: `6a964b45-c8f9-4d09-92d5-a1f4b9e5788f`.
- Backend execution: `7fe10826-f366-440f-933d-0cc18bf5b0b6`.
- Project: **Synthetic Parts Service Transition**.
- Dates2-6November2026,5total days minus1shadow and1reverse=3KT days.
-6target hours,6reviewed topic hours,6scheduled hours,0gap.
-3actual SQL-backed L2 sessions on2/3/4November,08:00-10:00, Demo SME -> Demo Receiver.
-3tracker activities,0completed,0actual hours,0invitations,0transcript evidence.
- Word report39,246bytes, ten sections, download hash matched persisted bytes.
- Submitted report email from the browser's approval form to both user-approved
  recipients. Saved delivery state **accepted_by_smtp**; no recipient refusal
  returned. This is not independent proof of inbox receipt.
- Subject: **KT Planned for Synthetic Parts Service Transition - Draft for Review**.
- No calendar invitations or transition-release action was performed.

Final targeted verification:52passed, including real transactional LocalDB tests,
Unicode/timestamp fidelity, CASCADE/SET NULL behavior, operational rollback,
idempotency, attachment byte matching, uncertain/partial SMTP results, existing
tracker/analytics/capacity/static serving. TypeScript/Vite build passed with the
existing chunk warning.390px browser layout had no horizontal overflow.

An additional legacy smoke-test run had4failures: it calls extraction with no
uploaded documents and expects the old synthetic fallback, then assumes a profile
exists. Those failures occur before changed hierarchy execution; no fallback was
reintroduced to make them pass. The exact records those tests created during this
run were removed, preserving the real synthetic demonstration records.

This is not multi-user production deployment: application-wide authentication,
per-KT user authorization, hosted service/database operations and enterprise
monitoring remain deployment work. Calendar/transcript/acceptance evidence must
still be supplied; lifecycle events cannot be fabricated by a planning pipeline.

## Historical: real backend submission on workflow167 - 16 October 2026

This section supersedes the earlier discovery/local-first snapshots below.
User authorized proceeding on167 and a synthetic test. Configured and saved:

- Start trigger API, path `kt-planner-workflow-2`, token authentication.
- Workflow memory explicitly off, overriding agent flags.
- Required string inputs `transition_id` and `document_bundle`, interpolated
  explicitly as `${inputs.transition_id}` and `${inputs.document_bundle}` in
  the intake task. Inline source text counts as usable supplied documents;
  citations retain original filenames, with no claim of opening original binaries.
- Same seven agents and11nodes; no new sending/callback/tool nodes.
- Main166 and original168 not saved or changed; shared agent instructions untouched.

The real configured webhook rejected an unauthenticated call with401.
Generated a seven-day Workflow access token. The first newly generated test
token could not be captured from the one-time UI and was revoked immediately.
Its replacement was transferred through the local password setup form without
printing it and stored with Windows user-scoped DPAPI encryption in a Git-ignored
file. No `.env` access, frontend/browser-storage credential or token in source.
Token remains active for local testing and must be renewed/revoked in Profile.
GET connection status never returns it.

Implemented local connection setup and persistent planning-job APIs. Multipart
sources are parsed locally into cited text; the backend submits a fixed
authenticated webhook with TLS verification, no redirects and no automatic retry.
Persisted jobs include request ID, extracted bundle, source metadata/hash,
receipt, remote run ID and explicit failures. A repeated request ID does not
resubmit. A timeout is unknown, not failed-or-safe-to-retry. A successful HTTP
response is accepted only with the expected workflow167/project77/UUID receipt.
No database schema migration to SQL Server occurred; SQLite remains authoritative.

Real test:

- Local KT: **SYNTHETIC - Amplify API End-to-End Test**,
  `6a964b45-c8f9-4d09-92d5-a1f4b9e5788f`.
- Local job: `144e1f93-87cb-451c-8cc2-efd25025b026`.
- Amplify run: `8055c745-2543-41f2-b501-f21bebfd3a05`.
- Submitted both synthetic source documents through the local backend API.
- Platform accepted receipt returned the matching run ID and inputs.
- All seven agents completed; duration205,909ms.
- Intake cited both files and preserved the planning-reference conflict rather
  than silently erasing it.
- Planning:5-1-1=3days;3*2=6target hours;2+2+2=6leaf hours;gap0.
- Validation stayed `draft_not_released`. Scheduler had empty delivery_results,
  messages_sent false. No transcripts/actual operational evidence supplied.
- Portal recorded approval-step completion and final End. Assistant did not
  submit approval; do not infer its source.
- Actual Full JSON was transferred via visible portal Output into the local
  import form, not a guessed result API. The imported snapshot and job persist.

**Remaining blocker: automatic result return.** User initially said they could
provide result API documentation, then confirmed they do not have it. No supported
result/status endpoint or approved hosted callback was available. Do not reuse
browser-session credentials, guess undocumented endpoints or expose localhost
through an unapproved tunnel. This is a real launch + manual result-return
implementation, not a fully automatic end-to-end migration.

UI now provides a document-upload/consent/start workspace, saved job receipts,
direct Amplify review links, explicit manual import, readable report and report
download. Connection settings are collapsed. New workspace creation asks for
name and dates instead of fixed demo values. Existing15module screens remain
separate; agent outputs are not automatically committed to their operational
tables and original deterministic engines were not executed by the agents.
No emails/invitations are sent. Source/input sizes fail explicitly rather than
truncate. Shared-local-workspace warnings remain; no multi-user authentication
or per-user access isolation has been added.

Final verification:28targeted tests passed across the Amplify connector, snapshot
API, existing capacity rules and single-deployment serving. TypeScript/Vite
production build passed; existing chunk-size and Python dependency/deprecation
warnings remain. Browser reopened the persisted real report using the final
bundle;390px layout had no horizontal overflow. Upload/consent state gates were
checked without starting a second real run. Original module stage1 still opened.
The report endpoint returned200 with a Markdown attachment header, and all11,812
characters matched the persisted reporting-agent result exactly. Native browser
download-event automation timed out; the direct HTTP attachment response and
final UI download URL were verified instead. Backend restarted on loopback,
credential configuration survived, and the synthetic job/snapshot remained saved.
No email/calendar delivery was tested or performed.

## Portal integration discovery - 16 October 2026

Broader visible-portal inspection corrects the earlier inconclusive API finding.
The workflow palette explicitly offers **Webhook / API Trigger**, **Workflow as
a Service (WaaS)**, **Post to Teams / Webhook**, and JavaScript data transformation.
These are orchestration features, not evidence that Amplify hosts arbitrary
FastAPI/Python applications.

Inspected workflow167's Start Config. Trigger choices: Manual, Webhook / API,
Schedule, Parent Workflow. Previewed Webhook / API only in the unsaved draft:
Webhook Path, Authentication, and a generated Webhook URL. UI states:
POST JSON to start a run; body becomes workflow inputs. Authentication choices
include Platform API Token, Shared Secret Header and None (public).
Do not use public mode. An explicit temporary path produced a platform-derived
URL, not an invented endpoint. No request was sent to it. Discarded the draft;
reloaded/exported 167 to verify `trigger.type: manual`, 11 nodes and no temporary
path persisted.

Profile has **Workflow access token**: explicitly for external systems starting
workflows through webhooks, acting as the user. One active token permitted;
this account showed no active token. No token was generated, read or saved.
Thus backend-to-Amplify triggering has a real exposed configuration path.
Still unverified: actual authenticated execution, token header syntax,
HTTP request/response contract, document attachment handling, input interpolation,
status/result retrieval, callback authentication/retries and revision activation.
Do not claim end-to-end integration or equate a palette node with tested runtime.

Recommended split:
- Workflow168: preserved Amplify-native/manual planning baseline.
- Workflow167: future app-connected workflow, invoked by the KT backend.
- Existing frontend/backend: operational KT storage, deterministic calculations
  and dashboard. Backend calls Amplify; a generic agent API tool is not required
  merely to start the workflow.
- If results return via outbound webhook, a reachable authenticated backend is
  required. Polling from localhost depends on a supported result API.

Visible Tools catalogue still has 11 toolsets and no generic HTTP/custom backend
tool. Handover agent Tools shows no assignable tools. This constrains agent-to-
backend calls, not the separate inbound workflow webhook capability.
Product detail navigation showed only its configuration heading in this account;
no administrative API provisioning interface was verified.

Runtime memory needs explicit review before confidential/multi-user data:
the agent Runtime UI warns experimental memory is shared across users/agents;
its Memory checkbox was checked. Workflow Start Config offers On (workflow-wide
memory retained 7 days), Off (overrides agent flags), Inherit (uses agent flags);
167 showed Inherit. These are UI descriptions, not independently tested isolation
guarantees. Prefer explicit Off for independent confidential KT runs, after an
authorized change. No memory setting was saved in this inspection.

## Retired - Workflow 2 and local API dashboard - 16 October 2026

User selected local-first API/UI development, with the live Amplify connection
explicitly pending, and redesign of the landing dashboard plus workflow
run-details view while preserving all existing KT module screens.

Copied the live exported YAML from workflow **168** into existing retired
workflow **167**, renamed it **Retired - Workflow 2**, saved, reloaded and
re-exported both. The persisted exports match exactly after normalizing only
name and slug. Seven agent IDs remain `[165,166,167,168,144,142,143]`;
11 nodes including human review and alternate End. Both branches remain
no-send. Original 168 and main 166 were not saved or changed. Agents are
shared references, not independent agent clones; edits to those agents would
affect every workflow using their latest versions. No API tool was added.

The frontend landing dashboard now shows a dark/cyan mission-control layout,
the seven-agent/stage blueprint, existing saved KT search/filter/sort/cards,
and an explicit **Amplify API integration: Pending** indicator. Each KT has a
Workflow runs link. Existing module screens are preserved.

Added a local `workflow_runs` SQLite table and per-transition list/import/detail
API. The run explorer consumes this real API and displays immutable,
manually imported workflow167/project77 snapshots with agent outputs and review
records. Imports are unverified data, not execution, live sync, release approval
or normalization into operational KT tables. Missing outputs/agents remain
missing. Duplicate runs are rejected, including cross-KT reassignment.
Unknown platform metadata is dropped; text output is escaped by React.

This is intentionally a local-first foundation, not completed cloud integration.
Authentication/authorization, approved HTTPS hosting and an enabled Amplify
API tool are prerequisites before agents can call the original planner services.
No SQL Server connection, automatic calendar/email delivery or new LLM call is
introduced by the run explorer. API details and local operation are in
[README](../README.md#saved-kts-local-frontend).

Verification: frontend TypeScript/production build passed (existing large-chunk
warning remains). Twelve targeted API/capacity/static-serving tests passed,
including exact output-size/step-count boundaries, duplicate rejection and
per-KT lookup boundaries. Browser verification used the real local API for
import/reopen/reload of an explicitly synthetic partial snapshot; six missing
agents remained missing and HTML-looking output rendered as plain text.
Checked invalid JSON, wrong-workflow rejection, empty history, controlled 503
and retry, Back/Forward navigation, original Document Intake navigation, and
390px dashboard/run layouts without horizontal overflow. The named synthetic
test snapshot was deleted afterward; no real workflow167 run was performed.
The local service is bound to `127.0.0.1:8000` for review. No messages were sent.

## Document attachment and email request - 16 October 2026

User requested a professional complete-plan attachment and short email titled
for the application. Confirmed draft recipients:
`atharva.utekar@vwgds.in`, `vivek.chaurasia@vwgds.in`.
User selected manual preparation while automatic attachment delivery is blocked;
this did not authorize sending.

Rechecked the live Documents catalogue: Create Document supports `.docx`
from complete Markdown, under the platform connection. However, the dedicated
handover agent's Tools tab displayed **No tools available**, so it could not
be assigned to the workflow. Standalone **Try it once** returned a successful
artifact result (`zk8GbEvMMjzVJcTXKJgNBuSUCUt1bLJa`, 41,059 bytes), but exposed
no download link. Its Content Markdown field was a single-line input that
stripped newlines; that test artifact is not a verified professional deliverable.
Do not present it as a downloadable attachment or invent a URL.

Inspected the existing Send Email node's Config without saving any main-workflow
changes: recipients, kind, subject, body, format, template and failure controls;
no attachment input. Left the editor without saving incidental selection state.
No attachment-capable transport is verified.

Prepared a fallback Word document and an unsent `.eml` draft in the session
deliverables directory, not application source. The Word document includes
document control, a session summary table, the complete saved KT overview,
capacity/source/people/curriculum/validation/invitation/tracking sections,
page headers/numbering and a distribution checklist. Corrected the two known
historical report passages about agent identities and post-review execution;
source plan values were not changed.

Draft subject: **KT Planned - Synthetic Parts Service Transition [TEST - Draft]**.
The short body describes the application, window, people, three proposed
sessions/six hours, timezone, review status and outstanding blockers.
The `.eml` embeds the complete `.docx` as one MIME attachment with `X-Unsent: 1`.
No SMTP/network-send code was used. Reopened the Word document and verified all
ten report sections; parsed the email and verified the attached bytes exactly
match the Word file. User must review/open the files in their mail application
and send manually if desired.

Workflow 168 remains no-send; no new automatic attachment delivery was enabled.
Operational subject convention: **KT Planned - <Application Name>**.
Native automation still requires assignable document generation and an
attachment-capable sender, with approval of exact recipients/body/document.

## Current: Amplify-native KT transition planning adaptation - 16 October 2026

The user authorized migrating whatever is feasible natively in Amplify.
Replaced **only existing workflow 168**, retaining its requested name
**Retired - Workflow**, with an advisory KT transition planning/review flow.
The earlier four-node transcript definition below is historical.
Current importable source: [CHAMP_KT_TRANSITION_WORKFLOW.yaml](CHAMP_KT_TRANSITION_WORKFLOW.yaml).
Do not import the historical `CHAMP_KT_REAL_TRANSCRIPT_TEST.yaml` to obtain
this new flow: it would restore the old transcript-only graph.

### Connected stages

| Agent | ID | KT Planner responsibilities adapted |
|---|---|---|
| KT Transition Intake & Profile | 165 (new) | 1-3: multi-document review, profile and settings |
| KT People & Knowledge Plan | 166 (new agent, not workflow 166) | 4-6: people, proposed hierarchy, KT levels/objectives |
| KT Capacity & Session Planner | 167 (new agent) | 7-10: advisory formula worksheet, sessions, availability checklist and proposed slots |
| KT Plan Validation & Handover | 168 (new agent, not workflow 168) | 11-12: advisory validation, release blockers and handover text |
| KT Scheduler | 144 (reused without instruction changes) | 13: invitation draft only |
| KT Tracker | 142 (reused without instruction changes) | 14: actual transcript evidence if supplied; otherwise awaiting_transcripts |
| KT Reporting/Analytics | 143 (reused without instruction changes) | 15: readable KT transition overview |

Start -> seven agents in the order above -> human draft review -> reviewed
draft end or revision-required end. Both end branches are no-send.
Agent names/IDs and workflow names/IDs are different namespaces.
The final approval is assigned to user 164; it is **draft review**, not an
authorization to send mail, book meetings, publish or update application data.
The report is readable text in both the approval and agent output.

### Available experience and explicit limits

- Start and review the flow from Amplify; no VS Code, localhost, Python API,
  local database or local LLM key is called by this native definition.
- Attach the KT BRDs plus a plain-text settings/people/slot document. Supply
  duration, shadow/reverse-shadow days, daily KT hours, dates/timezone,
  SME/receiver names/roles, topic estimates and proposed slots where known.
- Every stage consumes the preceding state explicitly. Facts require source
  references; source conflicts and inaccessible/partial attachments remain
  visible. Missing source documents produce needs_input rather than facts.
- The overview covers project/scope, source gaps, settings/capacity, people,
  knowledge/levels, proposed sessions, blockers, invitation text and tracking.
  Find it in Run History -> run -> Timeline -> details for **15 KT Transition
  Overview - Readable Report**, or in the final human-review task.
- Amplify run history retains outputs under its own access/retention policy.
  This is not the existing React dashboard, a custom native interactive app,
  a writable KT database, a record ownership model or plan-version tracking.
- Capacity formula was adapted from the Python service:
  `max(0,total_duration_days-shadow_days-reverse_shadow_days)*daily_kt_hours`.
  LLM arithmetic and validation are advisory, not execution of deterministic
  Python engines; a human must verify them. Leaf hours are counted once.
- Calendar availability, holidays, leave, shifts, DST and cross-calendar
  conflicts are unverified. Only supplied slots may be proposed.
- BRDs cannot establish attendance, delivery, actual hours or acceptance.
  No transcripts means awaiting_transcripts and unknown delivery metrics.
- No notification node exists. Invitation bodies are drafts; no real mail,
  Teams links, appointments, exports or database writes are fabricated.
- A later transcript run needs original planning context supplied again.
  There is no automatic cross-run lookup, correlation, merge or resume.
- Rejected/incorrect/missing-input drafts are revised by starting another run;
  there is no claim that earlier checkpoints enforce application governance.

### Native validation

Saved workflow 168 and reloaded it: 11 nodes including seven agents, review,
Start and two End branches. YAML references/edges parsed successfully;
no notify nodes. Uploaded two actual small synthetic `.txt` attachments
(`KT_Demo_BRD.txt`, `KT_Demo_Transition_Inputs.txt`) through Amplify's run UI.
The UI reported 1,386 and 1,269 characters read, respectively.
Test run: `02874fbc-7d3d-4077-a1a3-35d39843b07c`.
The local walkthrough backend was stopped after launch to remove any local
service dependency. The run **completed 10/10 executed steps in 688,990 ms
(11 minutes 29 seconds)**: Start, all seven agents (each attempt 1), human
draft review and the reviewed-draft End. The alternate revision End was not
executed. The portal recorded `approved`; the assistant did not submit an
approval or rejection. The user had selected leaving the test paused to
review it, but by the subsequent inspection it had advanced through approval.

Verified actual runtime output, not only prompts:

- Both attached source files appear in the intake register, with section refs.
- Demo SME and Demo Receiver retained their supplied roles and topic assignments.
- Three 2-hour topics/sessions retained dates 2026-11-02/03/04 and
  10:00-12:00 Asia/Kolkata.
- Capacity operands 5/1/1/2 produced 3 available KT days, 6 target hours,
  6 leaf hours and zero proposed gap; parent hours were not counted.
- Validation remained `draft_not_released`; the unconfirmed access approver,
  synthetic/non-deliverable email addresses and unverified calendars stayed
  visible as blockers. Approval of a draft did not make it released.
- Scheduler returned `delivery_results: []`, `messages_sent: false`,
  `teams_meeting_created: false` and `mutations_performed: false`.
- Tracker used its standard overall status `needs_input` with
  `evidence_scope.transcript_status: awaiting_transcripts`, empty findings
  and resolved items, and three tracking-template rows. Progress, attendance,
  actual hours and acceptance were all null, and mutations_performed was false.
- Final overview was readable Markdown with synthetic/draft labels, source
  names, people, supplied dates, capacity, risks and missing delivery metrics.
  It was about 1,485 words, longer than the requested 1,000-word prompt budget;
  that budget is not a runtime-enforced constraint.
- Separately tested new intake agent 165 in a fresh playground chat with no
  documents: it returned `needs_input`, an empty source register, null project
  settings and no invented people, curriculum or external actions.

One report-quality defect was found: its closing agent list repeated generic
upstream planning roles and incorrectly included the human gate as an agent.
Saved and re-exported tighter curriculum/reporter task instructions to prohibit
invented topology and approval-triggered execution claims in **future runs**.
Confirmed both guards persisted, with seven agents and no notify node.
The completed test retains its original report; no corrected full run was
launched after the user chose to review the existing test. This is a known
historical report defect, not a claim that an extra agent ran.

### Manual use in Amplify

1. Open existing **Retired - Workflow** (168), not the separate main workflow.
2. Attach BRDs and a settings/people/slot document. The tested `.txt` inputs
   were fully read; do not assume every format/large document has full coverage.
3. Enter a reference such as `KT-<project>-<version>`, request a proposed KT
   transition plan and explicitly identify missing availability or transcripts.
4. Run and watch the seven-agent Timeline. Inspect input coverage and blockers,
   not merely a green completion badge.
5. Review the readable **KT Transition Overview** in the last agent's details
   or Approval Center. Approve only a reviewed draft, or Reject for revision.
   Neither action sends email/invitations or marks KT delivery complete.
6. Reopen Run History -> selected run -> Timeline -> details for
   **15 KT Transition Overview - Readable Report** to read the saved overview.
   Output/Summary shows the End message and review decision, not the whole plan.
7. For later transcript review, start another run with original planning
   context and transcripts, plus a verified meeting date where known.
   No automated merge with the earlier run is implemented.

The live tool catalogue was rechecked before this adaptation: My Tools=0,
11 catalogue toolsets; SQL operations explicitly reject writes/DDL.
No shared tools, other users' agents/workflows or main workflow 166 were edited.

## Synthetic browser run of workflow 168 - 16 October 2026

At the user's request, ran existing workflow 168 without changing its graph.
Run ID: `6d0f8cce-0b06-4d53-9a95-ae24277a6876`.
Supplied two tiny complete inline synthetic VTT equivalents, explicitly
labelled as synthetic and not the original real transcripts. Tracker (142)
completed in 31 seconds and Reporting/Analytics (143) completed in about
one minute. Both outputs were inspected in the browser: the runbook question
was resolved by the later answer; production access approver remained unknown.
Reporting preserved operational metrics as null and mutations_performed false.

The portal recorded cancellation from the run panel during Reporting.
Final overall status was Cancelled (about 1 minute 32 seconds), with Start,
Tracker and Reporting marked Completed; End was not executed. This is not a
successful full-workflow completion. No replacement run was launched.
The source of the run-panel interaction is not established by this record.

Results are in Amplify run history, not in LocalDB or the local dashboard.
No notifications or database-write nodes exist in this graph. Workflow 166
and other users' resources were not changed. The persisted report still uses
the existing task's fixed report date 2026-10-14, not the actual run/meeting
date; this demonstration does not correct that pre-existing task setting.

## Dedicated SQL Server LocalDB database - 16 October 2026

The user selected SQL Server instance `(LocalDB)\MSSQLLocalDB` and database
name `kt_planner_amplify_local`. Created that database using Windows integrated
authentication after verifying the requested name did not already exist.
A separate connection to the new database verified status `ONLINE` and zero
user tables. No existing database was changed or copied.

Also verified a Python `pyodbc` connection using the installed ODBC Driver 18
and Windows authentication. The database remained empty; this confirms driver
connectivity, not application/schema migration. Creating `.env` and
`.env.example` was blocked by organization content policy; the user must
configure their local environment file themselves. No real API key was
entered or read.

Connection string for local SQL Server clients:

```text
Data Source=(LocalDB)\MSSQLLocalDB;Initial Catalog=kt_planner_amplify_local;Integrated Security=True;
```

This database is empty and not yet connected to KT Planner. The application
still uses its existing SQLite configuration. SQL Server integration requires
a supported Python driver, database configuration, dialect-compatible schema
and migration testing before changing the application's data source.
LocalDB is local to this Windows user and is not directly reachable by the
hosted Amplify workflow. No network exposure or workflow changes were made.

## Local frontend implementation - 16 October 2026

The user authorized local SQL storage and delegated the frontend choice.
Retained the application's configured local SQLite database; no separate
SQL Server connection or database/schema change was made. Reused the existing
React application instead of creating a second frontend.

Added a **Saved KTs** home screen backed by the existing transitions API:
search by name/ID, status filtering, update/name sorting, record dates and
capacity, create/open actions and Scheduler/Tracker/Analytics shortcuts.
The existing 15 stages remain available. URL fragments identify the selected
transition and stage for bookmarks, reload and Back/Forward. Switching KTs
resets stage-specific form state and starts at Document Intake.

The screen explicitly identifies the shared local workspace and does not
claim private user records, version snapshots or complete change history.
Database errors are visible with a retry action rather than shown as empty
successful lists. Existing transition timestamps do not track every child
record update.

Validation: TypeScript/Vite production build passed; browser checks with
synthetic intercepted API responses covered search, filtering, sorting,
create/open, reload, Back/Forward, cross-KT state reset, invalid/missing
record navigation, error/retry, empty results and 390px layout. The browser
checks did not connect to or mutate the real database. Rebuilt the tracked
frontend distribution for FastAPI static hosting. Dependency restoration
reported 8 audit findings (2 moderate, 6 high); dependency versions were
not changed as part of this frontend work.

No Amplify workflows or agents were modified for this local frontend work.
Amplify-to-localhost connectivity, production authentication, per-user
authorization and full-workflow service Tools remain unimplemented.

## Full-project workflow request - 16 October 2026

At the user's request, renamed existing workflow **168** from
**RETIRED - KT Separate Transcript Review** to **Retired - Workflow**.
Workflow 166 (the main scheduler/tracker/reporting flow) was not changed.
Workflow 168 still contains its previous four-node transcript-review graph;
the rename is not a completed full-project migration.

The user selected **Production integration: Amplify workflow + hosted KT
Planner services and authenticated UI** and confirmed infrastructure is
**Not provisioned yet**. Deployment is blocked on approved hosting, identity,
durable storage and assigned Amplify Tools. The project workflow editor was
rechecked and still states **This project holds no tools yet**.

### Target module mapping

These are the application's actual 15 UI stages, not 15 independent LLM agents.
The implementation must preserve their existing service logic and reviewer
actions rather than replace calculations or persistence with prompts.

| Stage | Responsibility | Production execution |
|---|---|---|
| 1 | Multiple-document intake and extraction | Persist source files and extraction provenance under a transition |
| 2 | Project profile review | Generate profile; pause for edits/approval |
| 3 | Transition settings | Collect dates, timezone, countries, shifts, duration and daily hours |
| 4 | Stakeholders | Collect/confirm SMEs, receivers, levels and assignments |
| 5 | Six-tier knowledge hierarchy | Existing hierarchy generation and review |
| 6 | KT level matrix | Existing applicability/objective/exit-criteria logic |
| 7 | Capacity planning | Existing deterministic capacity and balancing services |
| 8 | Session review | Persist reviewed session/topic choices |
| 9 | Availability/conflicts | Supplied or integrated calendars, holidays, leave and shifts |
| 10 | Schedule building | Deterministic scheduling, eligibility, timezone and conflict logic |
| 11 | Validation/approval | Existing validation services plus authenticated human decisions |
| 12 | Publish/deliver | Versioned plan exports and audit records |
| 13 | Invitations | Approved, idempotent send integration; no invented Teams links |
| 14 | KT tracking | Later transcript uploads, reviewed activity linkage and optional AI analysis |
| 15 | Reporting/analytics | Existing calculated metrics and advisory narrative |

A BRD alone cannot establish participant availability, approved dates, actual
delivery, future transcripts, attendance or acceptance. Missing inputs must
pause the workflow. Stage 14 runs after sessions occur; one workflow definition
must support later authenticated continuation against the same transition and
plan version, not a single uninterrupted BRD-to-completed-KT execution.
The current small LangGraph graph only invokes profile, hierarchy, KT levels,
decomposition and quality; wrapping that graph alone does not execute all stages.

### Where users see their data

Recommended user surface: an authenticated KT Planner UI with **My KTs** and
authorized project/team KTs. Opening a transition displays uploaded BRDs,
profile, settings, stakeholders, hierarchy, plans, schedule, validation,
exports, transcripts, tracker records and analytics. Users can reopen earlier
plans/runs and resume only authorized work. The existing React transition
selector and stage screens can be retained, but authenticated filtering,
permissions and version-history navigation require implementation and tests.
Email should provide a readable summary and an authorized application link;
email is not the system of record.

Amplify Run History is useful for execution evidence and troubleshooting.
Its visibility, retention, attachment retention and access rules must be
confirmed with the platform team; it must not be treated as an application
database or a proven private per-user KT workspace.

### Storage and isolation requirements

- Approved managed relational database for transitions, memberships, source
  metadata, extraction, profile, stakeholders, hierarchy, levels, schedules,
  plan versions, approvals, tracker records, assessments and audit events.
- Approved durable file/object storage for BRDs, calendars, transcripts and
  versioned exports; database rows reference stored objects rather than
  developer-machine paths.
- Server-established authenticated identity and project/transition membership.
  Do not trust a user ID supplied in a message or filename as authorization.
  Enforce permissions on list, read, write, run/resume and file-download paths.
- Correlate operations with tenant/project, transition ID, plan version,
  workflow run ID and actor. Use transactions, optimistic concurrency and
  idempotency for retries, especially invitation sends.
- Explicit retention, backup, restore, audit and failure/retry behavior.

The inspected current backend uses SQLite and local uploaded-file paths.
The transition model has no owner/membership fields, and the inspected list
route returns all transitions rather than a verified per-user authorized list.
Simply assigning transition UUIDs or moving SQLite does not establish
production multi-user isolation. Managed-database support also requires
adapting the existing SQLite-specific engine setup and schema migrations.

### Required platform provisioning before production implementation

1. Approved backend and frontend hosting with Amplify-to-service network access.
2. Enterprise identity/SSO integration and agreed project/transition roles.
3. Managed database and file storage, retention and backup requirements.
4. Approved typed Tools for document intake, each service stage, authorized
   retrieval/resume and reviewer-confirmed persistence, assigned to project 77.
5. Approved mail/calendar integration with idempotency and delivery results.
   The visible Amplify email node has no verified file-attachment field; sending
   actual plan attachments needs a supported sender, not a prompt instruction.
6. Tests for two users with separate and shared transitions, denied cross-user
   access, multi-file provenance, deterministic results, retries/resume,
   duplicate sends, exports and historical record retrieval.

No new full-project agents or fake integration nodes were deployed. No real
emails or data uploads were performed for this request. Once provisioned, wire
the preserved services into workflow 168 and verify the complete lifecycle.

## Readable approval and email presentation - 16 October 2026

Updated existing workflow 166, not a new workflow. The approval node is now
**Review KT Follow-up Email**. Its instructions show recipients, subject,
Approve/Reject meanings and the exact email-body preview, without embedding
the scheduler or tracker JSON.

Reporting agent 143 retains JSON as its default for standalone analytics.
Its instructions now allow plain text when explicitly requested by a workflow.
The connected workflow requests a concise plain-text email body with sections
for the proposed session, source review, open follow-ups, answered questions,
next-session questions and limitations. The same `state.executive_report`
text is interpolated into approval and used directly as the notification body.
No parsing of model-generated JSON is needed on this path. The portal compiler
still exports inferred state entries as `object`; runtime agent outputs are
text, and this is not an enforced structured-output schema.

The email subject is now **KT follow-up review - Parts Dashboard Automation**.
The expired 15 October slot was not silently replaced: the report must flag
expired proposals and the reviewer must reject stale or incomplete drafts.
The scheduler's fixed proposal still needs a valid future slot before actual
reuse. Evidence and metric safeguards remain, and missing metrics are displayed
as "Not available" rather than technical null fields.

### Presentation verification and send outcome

Ran the saved workflow once with no attachments intentionally, to validate
readable missing-evidence handling without uploading source data.
[Run f3ebfcf2-f508-454d-8ce1-3f37c02a5187](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows/166/runs?projectId=77&runId=f3ebfcf2-f508-454d-8ce1-3f37c02a5187)
executed replacement agents 144, 142 and 143 and paused at approval. Its draft
said **NOT READY TO SEND**, identified missing transcripts and the expired slot,
and did not invent transcript findings. In the actual Approval Center modal,
both **What to review** and **Previous result** displayed readable text, not
raw JSON. The platform tabs remain; they do not need to be hidden for this fix.

During inspection the portal recorded the test approval as **Approved**, and
the run completed its notification step, reporting
`Sent to atharva.utekar@vwgds.in, vivek.chaurasia@vwgds.in.`
The assistant's attempted rejection never executed: its preceding note-field
locator timed out after the dialog had already closed. The source of the
recorded approval was not established. This unexpected send was disclosed
immediately; recipients should disregard the presentation-test draft.
Inbox receipt is not independently verified. No further run was started.

The workflow relies on human approval: **NOT READY TO SEND is a warning, not
a deterministic send-blocking branch**. No approval bypass was added.
Existing approval requests retain the older run's content and will not be
retroactively reformatted. This test verifies presentation and missing-input
handling, not a new full two-transcript review.

## Current workflow: three connected agents with email approval

The user confirmed receipt of the earlier test email and requested one workflow
instead of three. Workflow **166** was updated in place and renamed:

**KT Scheduler / Tracker / Reporting & Analytics**

Current workflow step labels are **KT Scheduler**, **KT Tracker**, and
**KT Reporting/Analytics**, respectively referencing agent IDs 144, 142, and
143. These labels and the workflow title were renamed in place. The agent
library editor explicitly states that agent names and roles are set at
creation and are not editable there.
At the user's later request, the scheduler and reporting definitions were also
replaced with **KT Scheduler (144)** and **KT Reporting/Analytics (143)**.
Their instructions and roles were copied from agents 139 and 141, respectively.
Both are Product agents in project 77 with default OpenAI GPT-5.5 and no Tools.
Required responsibilities describe the same preview/advisory scope.
Both passed prompt validation and small actual playground tests:
the scheduler preserved the synthetic session and returned `preview_ready`
with empty delivery results; reporting preserved supplied 37.5 percent,
null actual hours and false final acceptance, labeled `supplied_snapshot`,
returned `report_ready`, and indicated no mutations.

Saved main workflow 166 now references **144 -> 142 -> 143**; export confirmed
the approval gate and sole email node remain. Our retired workflows 167 and
168 were also updated to use the appropriate replacements before deletion of
the old agents. Amplify's Delete action disabled agents 139 and 141, preserving
history. No new workflow, full real-data workflow run, approval decision, or
email send occurred during these replacements. Historical runs used the old
agent definitions, not these new ones.
At the user's subsequent explicit request, the transcript agent was replaced
with **KT Tracker (142)** and the old **KT Transcript Follow-up Agent (140)**
was deleted using the portal's soft-delete action: disabled for new runs,
with history retained. This was not a hard deletion.

KT Tracker was created as a Product agent in project 77 with the copied module
14 instructions and role, default OpenAI GPT-5.5 model, no Tools, and a required
responsibility describing advisory evidence review. Prompt validation passed
with advisory warnings. A real playground run on a small synthetic supplied
transcript returned `analysis_ready`, correctly recognized a resolved runbook
question and an unresolved production-access approver question, required human
review, and reported no mutations. Its supplied unknown meeting date was
preserved as the string `unknown`; no date was inferred.

The main workflow 166 and our retired review workflow 168 were saved with
agent 142 replacing 140. Main workflow export verified agent references
139 -> 142 -> 141 with the approval gate and one email node retained.
Existing historical runs, including the previously paused run, executed agent
140; they are not tests of the replacement. No full real-transcript workflow
rerun or email send was performed during replacement. The historical dummy
YAML still references 140 and is not suitable for import while that agent is
disabled. Use the current connected YAML instead.

Previously renamed to **KT Scheduler/Tracker** from **KT Connected Agents -
Review and Approved Email**, then to the current title, preserving workflow ID
166 and its connections. No new
workflow or run was created for this rename.

Email transport clarification: the received test email was sent by Amplify's
built-in `notify` / Send Email workflow node, not by KT Planner's local SMTP
service or directly by an AI agent. The underlying Amplify mail provider/SMTP
configuration was not exposed in the inspected step result. No KT Planner SMTP
configuration was connected to this workflow.

- [Open the current workflow](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows?workflowId=166&projectId=77)
- [Validation run awaiting approval](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows/166/runs?projectId=77&runId=57350bcd-7faf-4c2a-8828-3e531b71febf)
- [Current importable YAML](./CHAMP_KT_CONNECTED_WORKFLOW.yaml)

```text
Start: attach both original VTT transcripts
  -> KT Scheduler (144): proposed session preview
  -> KT Tracker (142): actual source analysis
  -> KT Reporting/Analytics (143): combined advisory report
  -> Human approval assigned to Atharva Utekar
       Approved -> Send Email -> End
       Rejected -> End without sending
```

The user selected approval before email sending. All three replacements are
documented above. Earlier test runs remain historical evidence, not evidence of
the replacement agents together or the new workflow's email branch.

### Consolidated workflow verification

Uploaded both original VTT files to a real run of the saved consolidated
workflow. Run `57350bcd-7faf-4c2a-8828-3e531b71febf` reached **paused** at its
human approval node after all three agents completed on attempt 1 with no
recorded errors. The reporting result was `report_ready`. The actual run JSON
contained Start, agent IDs 139/140/141, and a waiting approval step, with **no
executed notification step**. The report was displayed as the output on which
the approval decision is based. No approval was submitted by the assistant and
no second SME email was sent during consolidation.

The saved configuration's exported YAML was checked: approval is assigned to
Atharva (portal user 164), approval routes to the sole Send Email node, rejection
routes directly to an End node, and unanswered approval expires after 48 hours
with `on_expiry: fail`. Rejection, expiry and approved delivery have not been
executed in this consolidated run; only the pause-before-send behavior is
runtime-verified.

To continue, inspect the existing run and open **Approvals**. Review its report
and the proposed slot before deciding. **Approve** authorizes a new plain email
to both SMEs containing the readable advisory report; **Reject** is the
intended no-send route. The full VTT files are not attached to that email.
The current slot remains 15 October 2026, 10:00-11:00 AM Asia/Kolkata, and must
be edited before reuse if stale. No Teams link or calendar event is created.

Approval is **per run**, not cross-run duplicate prevention. Rerunning and
approving again can send another email. No automatic resume/approval was
performed. Prefer reviewing this existing paused run rather than starting
another run simply to inspect its output.

### Retired test workflows, not deleted

The portal's delete confirmation states that already-run workflows cannot be
deleted. An authorized deletion attempt for workflow 167 returned HTTP 403
with a permission error. No attempt was made to bypass this restriction.
The user then explicitly selected retiring both old workflows and disabling
the old email send:

- **167: RETIRED - KT SME Email Test - Sending Disabled**. Removed the
  notification node and its edges. Saved and re-exported the definition to
  verify no `notify` node or email channel remains. It is now preview-only.
- **168: RETIRED - KT Separate Transcript Review**. Renamed and saved with a
  message directing users to 166; it still has no notification/write node.

Both retired entries remain visible with their history. They were not deleted
or platform-archived, and the separate review can still be run if deliberately
selected. Their local YAML files now match these retired definitions; the dummy
YAML remains a historical non-sending example, not the current workflow 166.
Other users' workflows, including Transition-Planner, remain untouched.

The sections below document earlier tests before consolidation.

## Authorized SME email and real-transcript test - 14 October 2026

Created two additional isolated workflows in project 77. The original dummy
workflow, existing agents, and other users' resources were not modified.
Separating email from analysis prevents a transcript-review rerun from sending
the email again. Neither workflow was published.

### Plain email test

- [Workflow 167: KT SME Proposed Session - Plain Email Test](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows?workflowId=167&projectId=77)
- [Verified run](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows/167/runs?projectId=77&runId=feebb62c-8fc6-4d92-8c08-c8ae6bc4dbc8)
- [Importable YAML](./CHAMP_KT_SME_EMAIL_TEST.yaml)

Flow: Start -> scheduling agent 139 preview -> built-in Send Email node -> End.
The user authorized one plain-email test to `atharva.utekar@vwgds.in` and
`vivek.chaurasia@vwgds.in`, proposed as SMEs for **Parts Dashboard Automation -
KT Follow-up**, Thursday **15 October 2026, 10:00-11:00 AM Asia/Kolkata
(UTC+05:30)**. Availability and SME assignments are not independently verified.

The run was started once and completed four steps in approximately 45 seconds.
The notification step completed on attempt 1, with no recorded error, and
returned: `Sent to atharva.utekar@vwgds.in, vivek.chaurasia@vwgds.in.`
This is the platform's send result, not independently verified inbox receipt.
No transport receipt/message identifier was shown in that step result.
Do not rerun this workflow merely to inspect results: it can send another email.

This was a fixed plain-text proposed-session email, not an ICS calendar
invitation or a created Teams meeting. The visible Send Email node offered
no file-attachment field. The real transcripts were attached to the analysis
run below, **not to the outgoing email**, and their findings were not emailed.

### Real transcript analysis and reporting

- [Workflow 168: KT Real Transcript Review - Parts Dashboard Automation](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows?workflowId=168&projectId=77)
- [Completed real-data run](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows/168/runs?projectId=77&runId=f7245ecd-db89-4641-ae17-5086ab3dce88)
- [Importable YAML](./CHAMP_KT_REAL_TRANSCRIPT_TEST.yaml)

Flow: Start -> transcript agent 140 -> executive reporting agent 141 -> End.
There is no notification or record-write node.

Execution steps:

1. Imported the YAML into a new draft and saved workflow 168.
2. Used **Attach a document** on its run page to select both original VTT files.
   The portal showed both filenames and reported 182,369 and 142,099 characters
   read, respectively. No conversion to YAML or replacement with dummy text was
   needed.
3. Submitted a run message requiring both actual sources, later-answer checks,
   filename/timestamp citations, unknown meeting dates, and no sends or writes.
4. Inspected the transcript step's JSON, then checked evidence against the local
   originals. Actual transcript contents were not added to this repository.
5. After the browser login expired, the user signed in again; reopened the same
   run without rerunning it, and inspected the completed final report.

The actual run completed four steps, with agent IDs 140 and 141 both completing
on attempt 1, no step errors, and duration 529,134 ms (approximately 8 minutes
49 seconds).

Source coverage checks against the original files:

| Source | VTT cues | First timestamp | Last timestamp |
|---|---:|---|---|
| Parts Dashboard Automation Part 1 1.vtt | 1,166 | 00:00:06.464 | 01:06:25.424 |
| Parts Dashboard Automation Part 2.vtt | 879 | 00:00:06.549 | 00:53:53.509 |

Both source endpoints reported by the agent matched the originals. All 46
cited speaker labels and timestamp endpoints existed in their cited files.
After joining cues for the cited speaker and normalizing whitespace/case,
45 of 46 quotes or explicitly ellipsized excerpts matched. The remaining
citation joined a split numeric value as `82,000` rather than the source's
`82, 000`; it is not strictly verbatim. These checks support actual source use,
but do not prove exhaustive review of every cue or correct interpretation of
every finding. Human review remains mandatory.

The transcript agent returned `analysis_ready`; the reporting agent returned
`report_ready`, with six open follow-up items and seven resolved discussion
items. Broad follow-up themes were documentation details, incremental-load
documentation, gateway/DSN root cause, deployment reference sharing, sign-off
checks, and remaining HPG/dashboard KT. Later explanations in Part 2 were
recognized instead of treating every earlier question as still unanswered.

The final report used attached transcripts, not live application data. All ten
operational metrics, including completion percentage, planned/actual hours,
completed sessions, readiness, acceptance, sign-off, deployment completion,
and verified attendance, remained null. Both agent results required human review
and indicated no mutations. Source access through document search/read is
described by the agent output; that description is not an independent tool
audit. Do not interpret workflow completion as a production migration or final
KT acceptance.

To inspect this test yourself, open its completed-run link, expand each agent
under **Timeline**, or open **Output > Full JSON**. The advisory executive report
is the reporting agent's result; the End-node completion message is not the
report itself.

## Isolated end-to-end dummy workflow

At the user's subsequent request, created a separate workflow using only the
three agents below, in **SAVWIPL - CTMS revamp**. No other user's agents or
workflows were edited, and the existing orchestrator was not used or modified.

- Name: **KT Last 3 Modules - Dummy Data Demo**
- [Open workflow](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows?workflowId=166&projectId=77)
- [Completed test run](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows/166/runs?projectId=77&runId=947fae71-97d5-41f3-8add-7a00992123f2)
- [Importable YAML](./CHAMP_KT_DUMMY_DEMO.yaml)

```text
Start
  -> Module 13: synthetic invitation preview
  -> Module 14: synthetic transcript follow-up
  -> Module 15: executive report with preceding outputs and dummy metrics
  -> End
```

Dummy inputs are embedded in the node tasks, so no document upload or manual
data entry is needed. The preview uses an `example.invalid` recipient, the
transcript is fictional, and analytics are an independent precomputed fixture.
The earlier fictitious meeting is not represented as the future previewed
session. No invitation, external integration, or database-write node is present.

### Verified run

Run `947fae71-97d5-41f3-8add-7a00992123f2` completed all five steps, with zero
failed final steps, in approximately 4 minutes 30 seconds. The reporting node
completed on attempt 2; a temporary HTTP 503 was observed during the run.

Assertions against the actual run's JSON verified:

- Agent IDs 139, 140, and 141 executed in sequence.
- Invitation status was `preview_ready`, with no delivery results.
- Runbook location was resolved; the access approver remained unresolved.
- Transcript output required review and indicated no mutations.
- Final report used `supplied_snapshot` and preserved 37.5% completion, null
  actual hours, and false final acceptance.
- Final report included both preceding synthetic session and transcript results.

Agent results are JSON text rather than enforced structured output. The
transcript result included an additional advisory wrapper/guard summary; this
is generated content, not an additional executed agent or persistence action.
The actual executed agents are established by the run timeline.

### Running it yourself

1. Open the workflow link above.
2. Click **Run** without attachments; optionally enter "Run the synthetic demo".
3. Wait for completion and inspect **Timeline**.
4. Expand each agent step to see its result.
5. Open **Output > Summary** for the final executive report; **Full JSON** contains
   the detailed run record.

This proves agent sequencing and supplied-data handoff in Amplify, not live
KT Planner connectivity, real invitation delivery, or tracker persistence.
Workflow configuration is saved and runnable; no publish action was taken.
The earlier live-integration blocker remains unchanged.

## Current scope and portal implementation - 14 October 2026

The user narrowed deployment to modules 13, 14, and 15, rather than the whole
application. Three Product agents were created in the portal workspace named
**SAVWIPL - CTMS revamp**:

| Module | Agent | Portal ID |
|---|---|---|
| 13 | [KT Teams Scheduling Agent](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/agents/139/playground) | 139 |
| 14 | [KT Transcript Follow-up Agent](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/agents/140/playground) | 140 |
| 15 | [KT Executive Reporting Agent](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/agents/141/playground) | 141 |

All use the portal's default model selection, shown as OpenAI GPT-5.5 at creation.
Their instructions define structured JSON outputs, explicitly distinguish
supplied test input from live data, and require approved Tools for system access.
Prompt validation returned "Brief looks good" for each, with advisory warnings.
These checks do not establish operational or integration readiness.

### Playground tests

At this earlier playground-test stage, only synthetic inputs were submitted.
No source files, real transcripts, live transition records, or credentials were
uploaded, and no real invitations were sent.
The resulting test conversations are retained in the agents' playground history.

| Test | Observed result | Status |
|---|---|---|
| Scheduling preview with explicit-offset timestamps and synthetic recipient | `preview_ready`; input session preserved; delivery results empty | Passed for supplied-input preview |
| Scheduling request for live retrieval and sending without Tools/approval | `blocked_integration`; missing capabilities explicit; delivery results empty | Passed missing-integration handling; live sending blocked |
| Transcript with a later answer, an unresolved access approver, and an embedded instruction to mark work complete | Runbook question resolved; approver question unresolved; exact evidence retained; human review required; mutations false | Passed supplied-input analysis |
| Transcript requested by identifiers only | `blocked_integration`; findings empty; earlier synthetic evidence not reused | Passed missing-integration handling; live retrieval blocked |
| Analytics snapshot with 37.5% completion, null actual hours, and false final acceptance | Values preserved; source labeled `supplied_snapshot`; no mutations | Passed supplied-input reporting |
| Live analytics requested for a different transition without a snapshot | `blocked_integration`; no invented metrics or reuse of earlier values | Passed missing-integration handling; live retrieval blocked |

JSON parsing and assertions were executed against the actual displayed transcript
and analytics positive outputs and the scheduling negative output. This is
bounded behavioral validation, not a guarantee across future model runs.

### Remaining deployment blocker

The selected workspace's agent creation screen explicitly displayed **No tools
available**. The existing `Transition-Manager-Orchestrator` was previously
observed with zero assigned Tools and read-only access for the current account.
The three new agents are therefore saved definitions with tested supplied-input
behavior, **not connected replacements for the application's three modules**.
At that point no linking workflow had been saved and the teammate's agent was
not modified. The isolated dummy workflow subsequently created is described above;
it does not link to the teammate's orchestrator.
After reviewing this blocker, the user selected **Keep the agents as supplied-input
prototypes for now**. Live integration and workflow deployment are deferred.

To finish, the project/platform administrator must provision an approved runtime
connection and assign operations for session retrieval, conflict validation,
approved/idempotent invitation delivery, transcript/activity retrieval, and
calculated analytics retrieval. Reviewer-confirmed persistence needs separate
typed write operations if included. Then wire the agents into appropriately
triggered workflows and test against an authorized test transition.

Do not substitute prompts, fabricated Tool results, or a public tunnel for this
missing integration. The historical whole-application migration considerations
below remain reference material, not the current implementation scope.

## Decision summary

CHAMP supports importing workflow definitions as YAML. This is a verified route
for migrating orchestration, not a verified route for deploying KT Planner's
React frontend, Python services, database, and files inside the portal.

Preserve the existing application while proving a CHAMP workflow integration.
Do not rename source files to YAML or replace deterministic calculations with
LLM prompts. Whole-application hosting remains conditional on platform-team
confirmation.

## Evidence and limits

Initially inspected the authenticated portal on 14 October 2026 using the user's
existing Project Member access. No workflow was saved, imported, or executed; no
connections were configured and no project source or business data was uploaded.
The later agent creation and synthetic playground runs are recorded above.

Portal: [CHAMP / Amplify IT](https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/approvals).

| Surface | Observed behavior | Migration implication |
|---|---|---|
| Approval Center | Assigned human decisions gate workflow progression | Use for review gates, with decisions persisted in KT Planner |
| Create > Workflows | Canvas with validation, simulation, and save controls | Rebuild orchestration as platform-native nodes |
| Workflow YAML | `champ.workflow/v1`, compiled for `crewai_flow` | Generate this schema, not generic YAML or renamed source code |
| YAML import | Choose a file or paste YAML, then Load onto canvas; import replaces the canvas | Import only into a dedicated draft; preserve existing workflows |
| Download package | Described as workflow YAML plus full definitions of agents used, including instructions, tools, connectors, and model | Portable workflow/agent definition package, not evidence of application-code packaging |
| Trigger palette | Manual, schedule, and Webhook / API triggers | Candidate invocation paths; endpoint/authentication behavior still needs verification |
| Node palette | Agent, sub-workflow, Tool, email, Teams/webhook, branching, loops, human approval/input, transformations, guardrails | Supports representing the planning process |
| Code node | Described as JavaScript for transforming data | Not evidence of arbitrary Python execution or React hosting |
| Tools catalog | 11 visible Toolsets; no KT Planner Toolset or generic custom API registration control observed | Custom integration is the first feasibility gate |
| SQL Database | Read-only operations; mutation and DDL explicitly refused | Cannot replace application write APIs or initialize the application database |

These observations are UI evidence, not a successful runtime test or a complete
inventory of administrator-only capabilities. Catalog visibility does not imply
permission, connectivity, or correct execution. The inspected account displays
Project terminology; the supplied manual uses Product terminology.

The empty-canvas export shows sections for workflow metadata, project binding,
settings, trigger inputs, state, nodes, graph edges, and positions. It is not a
complete node schema. Do not invent node configuration fields from this sample.

## Current application boundary

- [Frontend controller](../frontend/src/App.tsx): 15-stage React user experience.
- [Backend entry point](../backend/main.py): FastAPI routes and built SPA hosting.
- [Database setup](../backend/database.py) and
  [configuration](../backend/config.py): local SQLite and local file directories.
- [Orchestration](../backend/ai/workflow.py): LangGraph graph with Python nodes
  opening database sessions.
- [Agent implementations](../backend/ai/agents.py): several named agents use
  deterministic rules; preserve those operations as service capabilities.
- [Business services](../backend/services/): scheduling, capacity, availability,
  validation, exports, invitations, transcript processing, and analytics.

The LangGraph graph is not directly interchangeable with the portal's CrewAI
Flow definition. Translate the process contract and state transitions; do not
assume Python functions or database sessions can be embedded in workflow YAML.

## Target architecture

```text
CHAMP project workspace
  Workflow YAML + approved agents + human review + guardrails
                         |
              Approved KT Planner integration
                         |
KT Planner service on approved enterprise hosting
  Typed business APIs + deterministic engines
  Authoritative database + persistent document/export storage
                         |
Existing React interface for rich editing, calendars, tracker, analytics
```

This target preserves functionality without claiming that CHAMP hosts the
application. If the requirement is no separate application hosting, pause after
Phase 1 until hosting, storage, and custom UI support are proven.

## Phased implementation plan

### Phase 1 - Confirm platform integration and hosting contracts

Work with the project owner and CHAMP administrator to confirm:

1. Correct workspace and permissions for KT Planner, using the approved
   enterprise onboarding/synchronization process.
2. How custom Toolsets are registered: supported API, connector, or MCP contract,
   ownership, review process, and deployment location.
3. Runtime connectivity to KT Planner, authentication, secret storage, and
   propagation of user identity and workspace scope.
4. Trigger invocation API, authentication, run-status retrieval, approval resume
   behavior, cancellation, retries, and runtime timeout semantics.
5. File transfer, export delivery, payload limits, retention, and trace masking.
6. Whether arbitrary Python/container deployment, custom React UI hosting or
   embedding, and persistent application storage are supported.
7. A schema reference or representative exported workflow containing configured
   Tool and Human Approval nodes.

**Exit gate:** documented, authorized integration route and a decision on
hybrid deployment versus platform-native hosting. If custom integrations are
unavailable, YAML import alone is not sufficient to migrate the whole product.

### Phase 2 - Prove a small workflow before rewriting anything

Build a dedicated draft with representative, non-sensitive test input:

```text
Manual trigger with transition_id
  -> Tool: retrieve or generate profile
  -> Human approval
       approved -> Tool: persist authenticated decision -> End
       rejected -> record revision request -> End
```

Use a separate test transition. Define inputs, typed outputs, reviewer assignment,
error paths, and correlation between CHAMP Run ID and KT Planner transition ID.
Use only one owner for each operation; do not run the old orchestration and CHAMP
orchestration simultaneously for the same request.

**Exit gate:** a real run reaches the reviewer; approval is persisted correctly;
rejection cannot publish; errors remain visible; a retry does not duplicate data.

### Phase 3 - Make KT Planner an enterprise integration service

Reuse existing business endpoints where possible, adding narrowly scoped
adapters only when the confirmed platform contract requires them.

- Authenticate backend access and enforce workspace/transition authorization.
- Validate mutations through typed APIs, not generated SQL.
- Add safe retry/idempotency behavior for writes and external side effects.
- Persist verified reviewer identity, decision, timestamp, and reviewed plan
  version; reject approval of a stale version.
- Externalize configuration and provision persistent database/file storage.
  Assess SQLite against concurrency and deployment needs; select a managed
  database only when justified.
- Preserve source-document evidence, transcript links, invitation state, exports,
  and approval history.
- Support run correlation and explicit failures without exposing secrets in logs.
- Verify deployment dependencies, health checks, backups, and recovery.

**Exit gate:** approved hosting is responsive and authorized CHAMP calls reach
the correct business operations without bypassing access controls.

### Phase 4 - Translate orchestration into workflow YAML

Use the verified node schema and portal exports as the source of truth.
Start with three workflows rather than one large automatic pipeline:

| Workflow | Responsibilities |
|---|---|
| Intake and profile review | Extraction, profile creation, evidence review, human approval |
| Planning and publication | Hierarchy, KT levels, capacity, availability, scheduling, validation, final approval, publication/export |
| Delivery follow-up | Invitations, transcript review/analysis, advisory follow-up, tracker updates with human confirmation |

Keep capacity, calendar rules, scheduling, validation, and export generation as
deterministic Tools. Use agents for evidence-grounded interpretation where
appropriate. Keep detailed UI editing in React unless an equivalent platform
experience is demonstrated.

Pass identifiers, revision numbers, and small structured results through workflow
state. Store authoritative plans and large documents in application storage.
Do not put credentials or connection secrets in YAML or exported packages.

**Exit gate:** each workflow imports, validates, saves, and completes a real test
run with correct routing and typed outputs.

### Phase 5 - Parity verification and staged cutover

| Test | Required outcome |
|---|---|
| Existing regression tests | Unchanged deterministic behavior |
| Calendar and scheduling fixtures | Correct time zones, holidays, leave, capacity, and conflict handling |
| Approval rejection or stale approval | No publication or invitation side effect |
| Tool timeout / invalid agent output | Visible failure; no success-shaped fallback |
| Retried mutation or invitation | No duplicate records or messages |
| Cross-workspace access attempt | Denied by backend as well as portal |
| Export and tracker checks | Existing output shapes, evidence links, and analytics preserved |
| Cancellation | Completed external actions remain accounted for; unfinished work recoverable |
| Storage migration, if needed | IDs, relationships, counts, documents, evidence, and history reconciled |

Pilot with one approved transition, then expand. Keep a validated backup and
rollback route. Disable the superseded orchestration only after acceptance, and
prevent both paths from creating the same side effects during cutover.

## YAML import procedure

1. Open Create > Workflows and the intended dedicated draft workspace.
2. Open **Import or export workflow YAML**.
3. Select **Import** and choose the generated YAML or paste its contents.
4. Select **Load onto canvas**; remember this replaces the current canvas.
5. Review project bindings, node configuration, approved tools, models,
   connections, inputs, outputs, and reviewer assignments.
6. Resolve validation issues and save only after review.
7. Use simulation as a configuration check, then perform a controlled real run.
8. Verify backend data and side effects, not just the workflow's displayed status.

Import success is not proof of deployment, connector availability, or functional
parity. A downloadable agent package also does not prove the target environment
has the required integrations, models, permissions, or credentials.

## Immediate next action

Confirm registration of an approved KT Planner Toolset and obtain a configured
Tool/Human Approval YAML export. Then implement the small profile-review proof
of concept. Do not attempt whole-source-file conversion or full migration before
this integration gate passes.
