import { useEffect, useState } from 'react';
import { request } from '../../api/client';

export function AmplifyConnection() {
  const [configured, setConfigured] = useState<boolean | null>(null);
  const [token, setToken] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [revision, setRevision] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    request<{ configured: boolean }>('/amplify/connection', { signal: controller.signal })
      .then((value) => { if (!controller.signal.aborted) setConfigured(value.configured); })
      .catch((err: unknown) => {
        if (!controller.signal.aborted) {
          console.error('Amplify connection status failed', err);
          setError(err instanceof Error ? err.message : 'Connection status failed');
        }
      });
    return () => controller.abort();
  }, [revision]);
  return <section className="mission-panel">
    <p className="mission-eyebrow">Backend → Amplify / local setup</p>
    <h2 className="mt-2 text-lg font-semibold">Workflow connection</h2>
    <p role="status" className="mt-2 text-sm text-slate-300">{configured === null ? 'Checking credentials...' : configured ? 'Token stored in backend. This alone does not confirm workflow execution.' : 'Add a Workflow access token to enable backend requests.'}</p>
    <p className="mt-2 text-xs text-slate-400">Create a token under Amplify → Profile → Workflow access token. It acts as your user. The local backend encrypts it with Windows user protection; it is never returned to the browser or stored in frontend storage. Keep this service local.</p>
    <form className="mt-4 flex flex-wrap items-end gap-3" onSubmit={async (event) => {
      event.preventDefault();
      setSaving(true);
      setError(null);
      try {
        await request('/amplify/connection', { method: 'PUT', body: JSON.stringify({ token }) });
        setToken('');
        setConfigured(true);
      } catch (err) {
        console.error('Amplify connection setup failed', err);
        setError(err instanceof Error ? err.message : 'Connection setup failed');
      } finally { setSaving(false); }
    }}>
      <label className="min-w-0 flex-1 text-sm">Workflow access token
        <input type="password" required minLength={20} maxLength={4096} autoComplete="off" value={token} onChange={(event) => setToken(event.target.value)} className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-3" />
      </label>
      <button disabled={saving || !token} className="mission-button">{saving ? 'Saving...' : 'Save backend token'}</button>
    </form>
    {error && <div role="alert" className="mt-3 text-sm text-red-300">{error}<button className="ml-2 underline" onClick={() => { setError(null); setRevision((value) => value + 1); }}>Retry status</button></div>}
  </section>;
}
