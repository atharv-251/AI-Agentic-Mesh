import React, { useCallback, useEffect, useState } from 'react';
import { GitBranch, PlusCircle, RefreshCw } from 'lucide-react';
import { api, TransitionSummary } from './api/client';
import { SavedKTs } from './components/pages/SavedKTs';
import { WorkflowRuns } from './components/pages/WorkflowRuns';

function readLocation() {
  const params = new URLSearchParams(window.location.hash.slice(1));
  return { transitionId: params.get('transition'), runId: params.get('run'), retiredStep: params.has('step') };
}

export function App() {
  const [transitions, setTransitions] = useState<TransitionSummary[]>([]);
  const [location, setLocation] = useState(readLocation);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [shadowDays, setShadowDays] = useState(0);
  const [reverseDays, setReverseDays] = useState(0);
  const [dailyHours, setDailyHours] = useState(2);
  const [category, setCategory] = useState('development_and_ams');
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);
  const active = transitions.find(item => item.id === location.transitionId);
  const refresh = useCallback(async () => {
    setLoading(true);
    setLoadError(null);
    try {
      setTransitions(await api.listTransitions());
    } catch (error) {
      console.error('Transition list failed', error);
      setLoadError(error instanceof Error ? error.message : 'Could not load transitions');
    } finally {
      setLoading(false);
    }
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);
  useEffect(() => {
    const changed = () => setLocation(readLocation());
    window.addEventListener('hashchange', changed);
    return () => window.removeEventListener('hashchange', changed);
  }, []);
  useEffect(() => {
    if (location.retiredStep && location.transitionId) {
      const hash = `#transition=${encodeURIComponent(location.transitionId)}&view=workflow`;
      window.history.replaceState(null, '', hash);
      setLocation(readLocation());
    }
  }, [location.retiredStep, location.transitionId]);
  const create = async (event: React.FormEvent) => {
    event.preventDefault();
    setCreating(true);
    setCreateError(null);
    try {
      const duration = (Date.parse(end) - Date.parse(start)) / 86400000 + 1;
      if (!name.trim() || !Number.isFinite(duration) || duration < 1) throw new Error('Enter a name and valid date range.');
      if (!Number.isInteger(shadowDays) || !Number.isInteger(reverseDays) || shadowDays < 0 || reverseDays < 0 || shadowDays + reverseDays >= duration || !Number.isFinite(dailyHours) || dailyHours <= 0 || dailyHours > 24) throw new Error('Use nonnegative whole shadow days, leave at least one KT day, and set daily KT hours between 0 and 24.');
      const record = await api.createTransition({
        name: name.trim(), category, start_date: start, end_date: end,
        total_duration_days: duration, shadow_days: shadowDays, reverse_shadow_days: reverseDays,
        daily_kt_hours: dailyHours, primary_country: 'India',
      });
      await refresh();
      setShowCreate(false);
      setName('');
      window.location.hash = `transition=${record.id}&view=workflow`;
    } catch (error) {
      console.error('Workspace creation failed', error);
      setCreateError(error instanceof Error ? error.message : 'Could not create workspace');
    } finally {
      setCreating(false);
    }
  };
  return <div className="app-shell min-h-screen text-slate-100">
    <header className="app-topbar">
      <div className="app-topbar-inner">
        <a href="#kts" className="app-brand"><span className="brand-mark"><GitBranch size={22} /></span><span>KT<span className="brand-light"> / NEXUS</span><small>TRANSITION INTELLIGENCE</small></span></a>
        <nav aria-label="Workspace navigation" className="flex flex-wrap items-center gap-4 text-sm">
          <span className="environment-tag"><span /> Local workspace</span>
          <a href="#kts" className="topbar-link">Portfolio</a>
          <button className="icon-button" disabled={loading} onClick={() => void refresh()} aria-label="Refresh transitions"><RefreshCw size={16} /></button>
          <button className="mission-button mission-button-secondary" onClick={() => setShowCreate(true)}><PlusCircle size={15} /> New transition</button>
        </nav>
      </div>
    </header>
    <main className="app-main">
      {loadError && <div role="alert" className="mb-5 rounded-xl border border-red-800 p-4 text-red-200">{loadError}. Previously loaded records may be stale. <button className="underline" onClick={() => void refresh()}>Retry</button></div>}
      {!location.transitionId
        ? <SavedKTs transitions={transitions} loading={loading} error={loadError} onCreate={() => setShowCreate(true)} onRefresh={refresh} />
        : active
          ? <WorkflowRuns key={active.id} transition={active} runId={location.runId} />
          : loading ? <p role="status">Loading transition...</p> : <section className="mission-panel"><h1 className="text-xl">Transition unavailable</h1><p className="mt-3">This record was not found in the connected database.</p><a href="#kts" className="mt-4 inline-block text-cyan-200">Return to transitions</a></section>}
    </main>
    {showCreate && <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
      <section role="dialog" aria-modal="true" aria-labelledby="new-transition-title" className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-2xl border border-slate-700 bg-slate-900 p-6">
        <h2 id="new-transition-title" className="text-xl font-semibold">Create a transition workspace</h2>
        <p className="mt-3 text-sm text-slate-400">Creating a workspace does not generate a plan. Amplify execution is mandatory.</p>
        <form onSubmit={create} className="mt-5 space-y-4">
          <label className="block text-sm">Application name<input required disabled={creating} maxLength={255} value={name} onChange={event => setName(event.target.value)} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-3" /></label>
          <div className="grid grid-cols-2 gap-3">
            <label className="text-sm">Start date<input type="date" required disabled={creating} value={start} onChange={event => setStart(event.target.value)} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-2" /></label>
            <label className="text-sm">End date<input type="date" required disabled={creating} min={start} value={end} onChange={event => setEnd(event.target.value)} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-2" /></label>
          </div>
          <label className="block text-sm">Transition category<select disabled={creating} value={category} onChange={event => setCategory(event.target.value)} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-2"><option value="development_and_ams">Development and AMS</option><option value="development">Development</option><option value="ams_operations">AMS operations</option></select></label>
          <div className="grid grid-cols-3 gap-3">
            <label className="text-sm">Shadow days<input type="number" min={0} step={1} required disabled={creating} value={shadowDays} onChange={event => setShadowDays(Number(event.target.value))} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-2" /></label>
            <label className="text-sm">Reverse shadow<input type="number" min={0} step={1} required disabled={creating} value={reverseDays} onChange={event => setReverseDays(Number(event.target.value))} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-2" /></label>
            <label className="text-sm">KT hours/day<input type="number" min={0.1} max={24} step={0.1} required disabled={creating} value={dailyHours} onChange={event => setDailyHours(Number(event.target.value))} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-2" /></label>
          </div>
          <p className="text-xs text-slate-400">Total days uses the inclusive date range. This workspace uses India timezones and default 08:00-17:00 shifts. Match capacity settings to your source documents. Agent facts and proposed slots still require review.</p>
          {createError && <p role="alert" className="text-red-300">{createError}</p>}
          <div className="flex justify-end gap-3"><button type="button" disabled={creating} onClick={() => setShowCreate(false)}>Cancel</button><button disabled={creating} className="mission-button">{creating ? 'Creating...' : 'Create workspace'}</button></div>
        </form>
      </section>
    </div>}
  </div>;
}

export default App;
