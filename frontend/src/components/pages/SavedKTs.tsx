import React, { useMemo, useState } from 'react';
import { ArrowRight, CalendarDays, Clock3, ExternalLink, FolderKanban, GitBranch, Layers, Plus, RefreshCw, Search } from 'lucide-react';
import { TransitionSummary } from '../../api/client';
import { AMPLIFY_WORKFLOW_URL, WORKFLOW_AGENTS } from './WorkflowRuns';

interface SavedKTsProps {
  transitions: TransitionSummary[];
  loading: boolean;
  error: string | null;
  onCreate: () => void;
  onRefresh: () => void;
}

export const SavedKTs: React.FC<SavedKTsProps> = ({ transitions, loading, error, onCreate, onRefresh }) => {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [sort, setSort] = useState('updated');
  const statuses = [...new Set(transitions.map(transition => transition.status))].sort();
  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    return transitions.filter(transition => (!status || transition.status === status) && `${transition.name} ${transition.id}`.toLowerCase().includes(query))
      .sort((a, b) => sort === 'name' ? a.name.localeCompare(b.name) : b.updated_at.localeCompare(a.updated_at));
  }, [transitions, search, status, sort]);

  return <div className="portfolio space-y-7">
    <div className="portfolio-heading"><div><p className="mission-eyebrow">Your transition command centre</p><h1>Transition portfolio<span>.</span></h1><p>Move knowledge with structure, evidence and human control.</p></div><button className="mission-button" onClick={onCreate}><Plus size={17} /> New transition</button></div>
    <section className="mission-hero portfolio-hero">
      <div><span className="status-pill"><GitBranch size={13} /> Mandatory Amplify orchestration</span><h2>From scattered knowledge<br />to a <span>connected transition.</span></h2><p>Seven agents. One clear workspace. Bring together application context, people, knowledge, sessions and handover evidence without losing sight of what needs review.</p>
        <a href={AMPLIFY_WORKFLOW_URL} target="_blank" rel="noreferrer" className="text-button mt-5">Explore workflow 167 <ExternalLink size={14} /></a></div>
      <div className="portfolio-flow" aria-label="Planning workflow"><span><Layers size={20} /><strong>Your sources</strong><small>BRDs &amp; transition inputs</small></span><ArrowRight size={17} /><span className="portfolio-flow-core"><GitBranch size={23} /><strong>Amplify</strong><small>7 connected agents</small></span><ArrowRight size={17} /><span><FolderKanban size={20} /><strong>Reviewed plan</strong><small>Manual return &amp; approval</small></span></div>
    </section>
    <div className="metric-grid">
      <article className="metric-card"><span><FolderKanban size={17} /> Saved transitions</span><strong>{error ? 'Unavailable' : loading ? 'Loading' : String(transitions.length).padStart(2, '0')}</strong><p>Records in the connected local database</p></article>
      <article className="metric-card"><span><GitBranch size={17} /> Orchestration coverage</span><strong>07<small> agents / 15 stages</small></strong><p>Intake through reporting / workflow 167</p></article>
      <article className="metric-card"><span><RefreshCw size={17} /> Integration mode</span><strong className="metric-text">API + manual return</strong><p>Live submission supported / no automatic result sync</p></article>
    </div>
    <section aria-label="Saved KT records" className="mission-panel portfolio-records">
      <div className="section-heading"><div><p className="mission-eyebrow">Workspaces</p><h2>Your transitions</h2><p>Open a workspace to launch, explore or review its planning results.</p></div><button className="icon-button" aria-label="Refresh KTs" disabled={loading} onClick={onRefresh}><RefreshCw size={17} /></button></div>
      <div className="portfolio-filters">
        <label className="portfolio-search"><span className="sr-only">Search KTs</span><Search size={17} /><input type="search" value={search} onChange={event => setSearch(event.target.value)} placeholder="Search application or KT ID" /></label>
        <label><span className="sr-only">Status</span><select aria-label="Status" value={status} onChange={event => setStatus(event.target.value)}><option value="">All statuses</option>{statuses.map(value => <option key={value} value={value}>{value.replace(/_/g, ' ')}</option>)}</select></label>
        <label><span className="sr-only">Sort by</span><select aria-label="Sort by" value={sort} onChange={event => setSort(event.target.value)}><option value="updated">Recently updated</option><option value="name">Application name</option></select></label>
      </div>
      {loading && <p role="status" className="py-5 text-sm text-slate-400">Loading saved transitions...</p>}
      {!loading && !error && <p role="status" className="mb-4 text-xs text-slate-400">{filtered.length} of {transitions.length} saved transitions</p>}
      {!loading && !error && !transitions.length && <div className="empty-state"><FolderKanban size={34} /><h2>Your next transition starts here.</h2><p>Create a workspace, then upload BRDs and transition inputs to Amplify.</p><button className="mission-button" onClick={onCreate}>Create first transition <Plus size={15} /></button></div>}
      {!loading && !error && transitions.length > 0 && !filtered.length && <div className="empty-state"><Search size={30} /><h2>No matching transitions</h2><p>Try another application name, KT ID or status filter.</p><button className="text-button" onClick={() => { setSearch(''); setStatus(''); }}>Clear filters</button></div>}
      <div className="transition-cards">{filtered.map((transition, index) => <article key={transition.id} className="transition-card">
        <div className="transition-card-top"><span className="project-avatar"><FolderKanban size={21} /></span><span className="status-pill">{transition.status.replace(/_/g, ' ')}</span></div>
        <p className="mission-eyebrow mt-5">Workspace {String(index + 1).padStart(2, '0')}</p><h3>{transition.name}</h3><p className="transition-card-id">{transition.id}</p>
        <div className="transition-card-facts"><div><CalendarDays size={15} /><span>Planning window<strong>{transition.start_date} <span className="text-slate-500">to</span> {transition.end_date}</strong></span></div><div><Clock3 size={15} /><span>Workspace capacity<strong>{transition.target_capacity_hours} hours / {transition.available_kt_days} KT days</strong></span></div></div>
        <footer><span>Updated {new Date(transition.updated_at).toLocaleDateString()}</span><a href={`#transition=${encodeURIComponent(transition.id)}&view=workflow`} aria-label={`Planning workspace for ${transition.name}`}>Open workspace <ArrowRight size={15} /></a></footer>
      </article>)}</div>
      <p className="portfolio-footnote">Shared local workspace, not a user-isolated portal. Record status is not proof of Amplify completion. Opening a workspace never starts agents or sends email.</p>
    </section>
    <section className="mission-panel">
      <div className="section-heading"><div><p className="mission-eyebrow">Planning architecture</p><h2>Designed around the transition.</h2></div><span className="status-pill status-warning">Results currently return by manual import</span></div>
      <div className="portfolio-agent-strip">{WORKFLOW_AGENTS.map((agent, index) => <div key={agent.id}><span>{String(index + 1).padStart(2, '0')}</span><strong>{agent.short}</strong><small>Stages {agent.stages}</small></div>)}</div>
    </section>
  </div>;
};
