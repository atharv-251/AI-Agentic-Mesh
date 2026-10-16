import { useEffect, useRef, useState } from 'react';
import { ExternalLink, FileText, Play, RefreshCw } from 'lucide-react';
import { AmplifyJob, api, WorkflowRun } from '../../api/client';

const ORIGIN = 'https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io';
export function AmplifyJobs({ transitionId, runs }: { transitionId: string; runs: WorkflowRun[] }) {
  const [jobs, setJobs] = useState<AmplifyJob[]>([]);
  const [files, setFiles] = useState<File[]>([]);
  const [instructions, setInstructions] = useState('');
  const [consent, setConsent] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [requestId, setRequestId] = useState(() => crypto.randomUUID());
  const [error, setError] = useState<string | null>(null);
  const [launchError, setLaunchError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [revision, setRevision] = useState(0);
  const fileInput = useRef<HTMLInputElement>(null);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => { mounted.current = false; };
  }, []);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    api.listAmplifyJobs(transitionId, controller.signal)
      .then((data) => { if (!controller.signal.aborted) setJobs(data); })
      .catch((err: unknown) => {
        if (!controller.signal.aborted) {
          console.error('Amplify job history failed', err);
          setError(err instanceof Error ? err.message : 'Could not load jobs');
        }
      }).finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [transitionId, revision]);

  return <section className="mission-panel space-y-6" aria-label="Live Amplify planning">
    <div><p className="mission-eyebrow">01 Upload → 02 Run → 03 Review → 04 Import</p>
      <h2 className="mt-2 text-2xl font-semibold">Start your KT plan</h2>
      <p className="mt-3 text-sm leading-relaxed text-slate-300">Your backend extracts the selected documents and sends their text to Retired - Workflow 2. Seven Amplify agents prepare the draft. Review it in Amplify, then import its Full JSON below to view the outputs here.</p>
      <p className="mission-notice mt-4">Submission is live. Automatic status/results are not connected. “Accepted” never means the plan is complete. No emails or meetings are sent by this workflow.</p>
    </div>
    <form className="space-y-4" onSubmit={async (event) => {
      event.preventDefault();
      setSubmitting(true);
      setLaunchError(null);
      try {
        const job = await api.startAmplifyJob(transitionId, files, instructions, requestId);
        if (!mounted.current) return;
        setJobs((existing) => [job, ...existing.filter((item) => item.id !== job.id)]);
        setRequestId(crypto.randomUUID());
        setFiles([]);
        setConsent(false);
        if (fileInput.current) fileInput.current.value = '';
      } catch (err) {
        if (!mounted.current) return;
        console.error('Amplify submission failed', err);
        setLaunchError(`${err instanceof Error ? err.message : 'Submission failed'}. Refresh job history before trying again; the same request ID is retained to avoid a duplicate run.`);
      } finally {
        if (mounted.current) setSubmitting(false);
      }
    }}>
      <label className="block rounded-xl border border-dashed border-slate-500 bg-slate-950/50 p-5 text-sm">
        <span className="flex items-center gap-2 font-semibold"><FileText size={18} className="text-cyan-300" /> Source documents / BRDs</span>
        <input ref={fileInput} type="file" multiple required disabled={submitting} accept=".txt,.md,.json,.csv,.vtt,.docx,.xlsx,.pdf" className="mt-4 block w-full text-xs file:mr-3 file:rounded-lg file:border-0 file:bg-cyan-100 file:px-3 file:py-2 file:text-slate-900" onChange={(event) => {
          setFiles(Array.from(event.target.files ?? []));
          setRequestId(crypto.randomUUID());
          setLaunchError(null);
        }} />
        <span className="mt-3 block text-xs text-slate-400">1-10 files, 5 MB each, 80,000 extracted characters combined. Text-based PDF, Word, Excel, TXT, Markdown, JSON, CSV and VTT. Scanned PDFs require OCR. Excel formula values must be saved in the workbook.</span>
      </label>
      {files.length > 0 && <ul className="space-y-1 text-xs text-cyan-200">{files.map((file, index) => <li key={`${file.name}-${index}`} className="break-words">{file.name} / {(file.size / 1024).toFixed(1)} KB</li>)}</ul>}
      <label className="block text-sm">Planning instructions <span className="text-slate-400">(optional)</span>
        <textarea disabled={submitting} maxLength={5000} value={instructions} onChange={(event) => { setInstructions(event.target.value); setRequestId(crypto.randomUUID()); }} rows={3} placeholder="Describe the transition scope, planning reference, constraints and any missing inputs. Put dates, people and estimates in your source documents." className="mt-2 block w-full rounded-xl border border-slate-600 bg-slate-950 p-3 text-sm" />
      </label>
      <label className="flex items-start gap-3 text-sm text-slate-300"><input type="checkbox" required disabled={submitting} checked={consent} onChange={(event) => setConsent(event.target.checked)} className="mt-1" /> I confirm these documents may be sent to Amplify for analysis. This starts a real AI workflow and may incur model usage.</label>
      {launchError && <p role="alert" className="break-words text-sm text-red-300">{launchError}</p>}
      <button disabled={submitting || !consent || files.length === 0 || files.length > 10} className="mission-button"><Play size={16} /> {submitting ? 'Submitting to Amplify...' : 'Start planning in Amplify'}</button>
      {submitting && <p role="status" className="text-xs text-amber-200">Keep this page open until submission finishes. A saved job remains available if you navigate away.</p>}
    </form>
    <div className="border-t border-slate-700 pt-5">
      <div className="flex items-center justify-between gap-3"><h3 className="font-semibold">Submitted jobs</h3><button disabled={loading || submitting} onClick={() => setRevision((value) => value + 1)} className="inline-flex items-center gap-2 rounded-lg border border-slate-600 px-3 py-2 text-xs"><RefreshCw size={14} /> Refresh saved jobs</button></div>
      <p className="mt-2 text-xs text-slate-400">Refresh reads your local database only, not live Amplify execution status.</p>
      {loading && <p role="status" className="mt-3 text-sm text-slate-400">Loading saved jobs...</p>}
      {error && <p role="alert" className="mt-3 text-sm text-red-300">{error}</p>}
      {!loading && !error && jobs.length === 0 && <p className="mt-4 text-sm text-slate-400">No jobs submitted for this KT yet.</p>}
      <div className="mt-4 space-y-3">{jobs.map((job) => {
        const saved = runs.find((run) => run.run_id === job.remote_run_id);
        return <article className="rounded-xl border border-slate-700 bg-slate-950/50 p-4" key={job.id}>
          <div className="flex flex-wrap items-center justify-between gap-3"><h4 className="text-sm font-semibold text-cyan-200">{job.status === 'accepted' ? 'Accepted by Amplify / execution status not synced' : job.status.replace(/_/g, ' ')}</h4><time className="text-xs text-slate-400">{new Date(job.created_at).toLocaleString()}</time></div>
          <p className="mt-3 break-all font-mono text-xs text-slate-400">Job {job.id}</p>
          {job.remote_run_id && <p className="mt-1 break-all font-mono text-xs text-slate-400">Amplify run {job.remote_run_id}</p>}
          <p className="mt-3 break-words text-xs text-slate-300">{job.source_files.map((source) => `${source.filename} (${source.characters.toLocaleString()} chars)`).join(' · ')}</p>
          {job.error && <p role="alert" className="mt-3 text-sm text-red-300">{job.error}</p>}
          {saved && <p className="mt-3 text-sm text-cyan-200">Manually imported snapshot reports: {saved.status}. Not live-synchronized.</p>}
          <div className="mt-4 flex flex-wrap gap-4 text-sm">
            {job.remote_run_id && <a href={`${ORIGIN}/workflows/167/runs?projectId=77&runId=${encodeURIComponent(job.remote_run_id)}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-cyan-200">Review run in Amplify <ExternalLink size={14} /></a>}
            {saved && <a className="text-cyan-200 underline" href={`#transition=${encodeURIComponent(transitionId)}&view=workflow&run=${encodeURIComponent(saved.run_id)}`}>View manually imported result</a>}
          </div>
          {!saved && job.remote_run_id && <p className="mt-3 text-xs text-amber-200">Result not imported. Copy this run's Output → Full JSON from Amplify into the import form below.</p>}
          {job.error && <details className="mt-3 text-xs"><summary className="cursor-pointer">Submission response details</summary><pre className="mt-2 max-h-60 overflow-auto whitespace-pre-wrap break-words">{JSON.stringify(job.response, null, 2)}</pre></details>}
        </article>;
      })}</div>
    </div>
  </section>;
}
