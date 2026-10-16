import React, { useEffect, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, CalendarDays, CheckCircle2, ChevronRight, Clock3, ExternalLink, FileSearch, GitBranch, LayoutDashboard, Link2, LockKeyhole, Play, RefreshCw, Send, Sparkles } from 'lucide-react';
import { api, TransitionSummary, WorkflowRun } from '../../api/client';
import { AmplifyConnection } from './AmplifyConnection';
import { AmplifyJobs } from './AmplifyJobs';
import { AmplifyResults, RESULT_AGENTS } from './AmplifyResults';
import { BackendPlanning } from './BackendPlanning';
import { IntegrationMap } from './IntegrationMap';

export const AMPLIFY_WORKFLOW_URL = 'https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io/workflows?workflowId=167&projectId=77';
export const WORKFLOW_AGENTS = RESULT_AGENTS;

const WORKSPACE_VIEWS = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard, caption: 'Transition at a glance' },
  { id: 'results', label: 'Agent intelligence', icon: Sparkles, caption: 'All seven agent outputs' },
  { id: 'launch', label: 'Launch & import', icon: Play, caption: 'Documents and run history' },
  { id: 'operations', label: 'Review & delivery', icon: Send, caption: 'SQL, reports and approval' },
  { id: 'connection', label: 'Connection', icon: Link2, caption: 'Architecture and credentials' },
] as const;
type WorkspaceView = typeof WORKSPACE_VIEWS[number]['id'];

interface Props { transition: TransitionSummary; runId: string | null }

export function WorkflowRuns({ transition, runId }: Props) {
  const [view, setView] = useState<WorkspaceView>('overview');
  const [runs, setRuns] = useState<WorkflowRun[]>([]);
  const [selected, setSelected] = useState<WorkflowRun | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [input, setInput] = useState('');
  const [importing, setImporting] = useState(false);
  const [importError, setImportError] = useState<string | null>(null);
  const [revision, setRevision] = useState(0);
  const importController = useRef<AbortController | null>(null);
  const base = `transition=${encodeURIComponent(transition.id)}&view=workflow`;
  const completed = selected?.snapshot.steps.filter(step => step.node_type === 'agent' && step.status === 'completed' && step.result?.trim()).length;

  useEffect(() => () => importController.current?.abort(), []);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    setSelected(null);
    Promise.all([
      api.listWorkflowRuns(transition.id, controller.signal),
      runId ? api.getWorkflowRun(transition.id, runId, controller.signal) : Promise.resolve(null),
    ]).then(([list, detail]) => {
      if (!controller.signal.aborted) { setRuns(list); setSelected(detail ?? list[0] ?? null); }
    }).catch((err: unknown) => {
      if (!controller.signal.aborted) {
        console.error('Failed to load workflow runs', err);
        setError(err instanceof Error ? err.message : 'Failed to load workflow runs');
      }
    }).finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [transition.id, runId, revision]);

  const importSnapshot = async (event: React.FormEvent) => {
    event.preventDefault();
    setImporting(true);
    setImportError(null);
    const controller = new AbortController();
    importController.current = controller;
    try {
      const payload: unknown = JSON.parse(input);
      const saved = await api.importWorkflowRun(transition.id, payload, controller.signal);
      if (controller.signal.aborted) return;
      setInput('');
      setView('results');
      window.location.hash = `${base}&run=${encodeURIComponent(saved.run_id)}`;
    } catch (err) {
      if (controller.signal.aborted) return;
      console.error('Workflow snapshot import failed', err);
      setImportError(err instanceof Error ? err.message : 'Snapshot import failed');
    } finally { if (!controller.signal.aborted) setImporting(false); }
  };

  const emptyResults = <section className="mission-panel empty-state"><FileSearch size={36} /><h2>{loading ? 'Loading saved results' : 'Your agent intelligence will appear here'}</h2>
    <p>Launch the mandatory Amplify workflow, complete its review and import Full JSON. We never fill missing results with invented data.</p>
    <button className="mission-button" onClick={() => setView('launch')}>Go to launch &amp; import <ArrowRight size={15} /></button>
  </section>;

  return <div className="workspace-layout">
    <aside className="workspace-sidebar">
      <a className="workspace-back" href="#kts"><ArrowLeft size={15} /> Transition portfolio</a>
      <div className="sidebar-project"><span className="project-avatar"><GitBranch size={23} /></span><span className="mission-eyebrow">Transition workspace</span><h2>{transition.name}</h2><span className="status-pill">{transition.status.replace(/_/g, ' ')}</span></div>
      <nav aria-label="Transition sections">{WORKSPACE_VIEWS.map(item => <button key={item.id} aria-pressed={view === item.id} className={view === item.id ? 'is-active' : ''} onClick={() => setView(item.id)}>
        <item.icon size={18} /><span>{item.label}<small>{item.caption}</small></span>{view === item.id && <ChevronRight size={14} />}
      </button>)}</nav>
      <div className="sidebar-boundary"><LockKeyhole size={17} /><strong>Amplify required</strong><p>No independent backend planning. Results require explicit return and human review.</p><button onClick={() => setView('connection')}>How the connection works <ArrowRight size={12} /></button></div>
    </aside>
    <div className="workspace-content space-y-6">
      <section className="workspace-heading">
        <div><p className="mission-eyebrow">KT orchestration / workflow 167</p><h1>{WORKSPACE_VIEWS.find(item => item.id === view)?.label}</h1><p>{transition.name}</p></div>
        <a className="mission-button mission-button-secondary" href={AMPLIFY_WORKFLOW_URL} target="_blank" rel="noreferrer">Open Amplify <ExternalLink size={14} /></a>
      </section>
      <div className="workspace-runbar">
        <div className="min-w-0"><label htmlFor="selected-run">Result snapshot</label>
          <select id="selected-run" disabled={loading || !runs.length} value={selected?.run_id ?? ''} onChange={event => { window.location.hash = `${base}&run=${encodeURIComponent(event.target.value)}`; }}>
            {!runs.length && <option value="">{loading ? 'Loading runs...' : 'No imported runs'}</option>}
            {runs.map(run => <option key={run.run_id} value={run.run_id}>{run.status} / {new Date(run.imported_at).toLocaleString()} / {run.run_id}</option>)}
          </select>
        </div>
        <span className="status-pill status-warning">Manual snapshot / not live</span>
        <button className="icon-button" disabled={loading} aria-label="Refresh workflow runs" onClick={() => setRevision(value => value + 1)}><RefreshCw size={16} /></button>
      </div>
      {error && <div role="alert" className="error-banner">{error}<button onClick={() => setRevision(value => value + 1)}>Retry</button></div>}
      {view === 'overview' && <>
        <section className="mission-hero overview-hero">
          <div><span className="status-pill"><Sparkles size={13} /> Amplify-powered intelligence</span><h2>Clarity across<br /><span>every handover.</span></h2><p>One place for your application brief, knowledge plan, proposed sessions and transition evidence. Agent outputs stay separate from operational approval.</p>
            <div className="mt-6 flex flex-wrap gap-3"><button className="mission-button" onClick={() => setView(selected ? 'results' : 'launch')}>{selected ? 'Explore agent results' : 'Start a planning run'} <ArrowRight size={15} /></button><button className="text-button" onClick={() => setView('connection')}>Understand the connection <Link2 size={14} /></button></div>
          </div>
          <div className="hero-orbit" aria-hidden="true"><div className="orbit-line orbit-line-outer" /><div className="orbit-line orbit-line-inner" /><span className="orbit-node orbit-node-one" /><span className="orbit-node orbit-node-two" /><span className="orbit-core"><GitBranch size={34} /><strong>AMPLIFY</strong><small>7 AGENTS / 1 WORKFLOW</small></span></div>
        </section>
        <div className="metric-grid">
          <article className="metric-card"><span><CheckCircle2 size={17} /> Agent execution</span><strong>{selected ? `${completed} / 7` : 'No result'}</strong><p>{selected ? 'Completed with output in this snapshot' : 'Awaiting an imported result'}</p></article>
          <article className="metric-card"><span><CalendarDays size={17} /> Workspace capacity</span><strong>{transition.target_capacity_hours}<small> hours</small></strong><p>{transition.available_kt_days} planned KT days / not agent-verified</p></article>
          <article className="metric-card"><span><Clock3 size={17} /> Reported run time</span><strong>{selected?.snapshot.duration_ms != null ? `${(selected.snapshot.duration_ms / 1000).toFixed(1)}` : 'Not supplied'}{selected?.snapshot.duration_ms != null && <small> sec</small>}</strong><p>Snapshot duration / not a live timer</p></article>
        </div>
        <section className="mission-panel">
          <div className="section-heading"><div><p className="mission-eyebrow">Connected intelligence</p><h2>Your seven-agent pipeline</h2><p>Reported agent execution, not KT completion or release approval.</p></div><button className="text-button" onClick={() => setView('results')}>View outputs <ArrowRight size={14} /></button></div>
          <div className="agent-pipeline">{WORKFLOW_AGENTS.map((agent, index) => {
            const step = selected?.snapshot.steps.find(item => item.node_type === 'agent' && item.agent_id === agent.id);
            return <article key={agent.id}><span className="pipeline-index">{String(index + 1).padStart(2, '0')}</span><div><h3>{agent.name}</h3><p>{agent.description}</p></div><span className={`status-pill ${step?.status === 'completed' ? 'status-connected' : ''}`}>{step?.status ?? 'No output imported'}</span></article>;
          })}</div>
        </section>
        <div className="overview-bottom">
          <section className="mission-panel"><p className="mission-eyebrow">Next action</p><h2 className="mt-3 text-xl font-semibold">{selected ? 'Review the source before saving.' : 'Start with your source documents.'}</h2><p className="mt-3 text-sm leading-7 text-slate-400">{selected ? 'Explore the agent outputs, verify missing inputs and resolve conflicts. An accepted run plus all seven outputs is required before operational review; manual imports are not authenticated proof.' : 'Upload BRDs and transition inputs to Amplify. Our backend records the submission; review the cloud run and bring the result back explicitly.'}</p><button className="text-button mt-4" onClick={() => setView(selected ? 'results' : 'launch')}>{selected ? 'Open agent intelligence' : 'Open launch & import'} <ArrowRight size={14} /></button></section>
          <section className="mission-panel"><p className="mission-eyebrow">Data lineage</p><h2 className="mt-3 text-xl font-semibold">Traceable, not assumed.</h2><dl className="lineage-list"><div><dt>KT workspace</dt><dd>{transition.id}</dd></div><div><dt>Selected run</dt><dd>{selected?.run_id ?? 'None selected'}</dd></div><div><dt>Return channel</dt><dd>Manual Full JSON import / unverified</dd></div><div><dt>Planning dates</dt><dd>{transition.start_date} to {transition.end_date}</dd></div></dl></section>
        </div>
      </>}
      <div hidden={view !== 'results'}>{selected ? <AmplifyResults key={selected.run_id} run={selected} /> : emptyResults}</div>
      <div hidden={view !== 'launch'} className="space-y-6">
        <AmplifyJobs transitionId={transition.id} runs={runs} />
        <section className="mission-panel import-panel">
          <div className="section-heading"><div><p className="mission-eyebrow">Return channel / manual handoff</p><h2>Bring the reviewed result home.</h2><p>Copy Run History / Output / Full JSON from workflow 167 after the run and draft review finish.</p></div><FileSearch size={25} className="text-cyan-300" /></div>
          <p className="mission-notice">Imports are immutable, unverified snapshots, not live synchronization or release approval. Workflow 168 history is not accepted. Saving a snapshot does not execute services or send mail.</p>
          <form onSubmit={importSnapshot} className="mt-5 space-y-4">
            <label htmlFor="workflow-json" className="block text-sm text-slate-300">Full run JSON<textarea id="workflow-json" required disabled={importing} maxLength={1_000_000} value={input} onChange={event => setInput(event.target.value)} rows={8} className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 p-4 font-mono text-xs text-slate-200" placeholder='{"run_id":"...", "workflow_id":167, "project_id":77, "status":"...", "steps":[...]}' /></label>
            {importError && <p role="alert" className="break-words text-sm text-red-300">{importError}</p>}
            <button className="mission-button" disabled={importing || !input.trim()}>{importing ? 'Saving snapshot...' : 'Import reviewed snapshot'} <ArrowRight size={15} /></button>
          </form>
        </section>
        {selected && <section className="mission-panel"><div className="section-heading"><div><p className="mission-eyebrow">Run governance</p><h2>Human review &amp; exit</h2><p>Cloud draft review does not grant KT acceptance or permission to send.</p></div></div>{selected.snapshot.steps.filter(step => step.node_type !== 'agent').map(step => <details key={step.node_key} className="raw-output"><summary>{step.node_type}: {step.node_key} / {step.status}</summary><pre>{step.result ?? 'No output supplied'}</pre></details>)}</section>}
      </div>
      <div hidden={view !== 'operations'}><BackendPlanning key={transition.id} transitionId={transition.id} amplifyRunId={selected?.run_id ?? null} /></div>
      <div hidden={view !== 'connection'} className="space-y-6"><IntegrationMap /><AmplifyConnection /></div>
    </div>
  </div>;
}
