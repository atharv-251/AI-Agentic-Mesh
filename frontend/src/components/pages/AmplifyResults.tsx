import { useState } from 'react';
import { ArrowUpRight, Braces, CheckCircle2, FileSearch, Info } from 'lucide-react';
import { WorkflowRun } from '../../api/client';
import { fieldLabel, isRecord, orderedFields, parseOutput } from './amplifyPresentation';
import { StructuredOutput } from './StructuredOutput';
import { WorkflowReport } from './WorkflowReport';

export const RESULT_AGENTS = [
  { id: 165, name: 'Application brief', description: 'Application profile, scope, sources and transition settings', short: 'Profile', stages: '01-03' },
  { id: 166, name: 'People & knowledge', description: 'SMEs, receivers, curriculum, KT levels and learning outcomes', short: 'Knowledge', stages: '04-06' },
  { id: 167, name: 'Capacity & sessions', description: 'Effort worksheet, proposed sessions and availability checks', short: 'Sessions', stages: '07-10' },
  { id: 168, name: 'Readiness & handover', description: 'Validation checks, blockers and handover requirements', short: 'Readiness', stages: '11-12' },
  { id: 144, name: 'Communication drafts', description: 'Proposed invitations, recipients and delivery restrictions', short: 'Communications', stages: '13' },
  { id: 142, name: 'Tracking & evidence', description: 'Transcript findings, actual evidence and next-call questions', short: 'Evidence', stages: '14' },
  { id: 143, name: 'Executive report', description: 'Full reporting-agent deliverable, available as a Markdown download', short: 'Report', stages: '15' },
];

export function AmplifyResults({ run }: { run: WorkflowRun }) {
  const [agentId, setAgentId] = useState(165);
  const agent = RESULT_AGENTS.find(item => item.id === agentId)!;
  const step = run.snapshot.steps.find(item => item.node_type === 'agent' && item.agent_id === agentId);
  const output = parseOutput(step?.result);
  return <section className="space-y-5" aria-label="Amplify results explorer">
    <div className="section-heading"><div><p className="mission-eyebrow">Agent intelligence</p><h2>Every output. In context.</h2><p>Explore all seven agent responses, organized by their role in your transition.</p></div><span className="status-pill status-warning"><Info size={13} /> Imported draft</span></div>
    <nav className="result-tabs" aria-label="Agent output categories">{RESULT_AGENTS.map((item, index) => {
      const itemStep = run.snapshot.steps.find(entry => entry.node_type === 'agent' && entry.agent_id === item.id);
      return <button key={item.id} aria-pressed={agentId === item.id} onClick={() => setAgentId(item.id)} className={agentId === item.id ? 'is-active' : ''}>
        <span className="result-tab-index">{String(index + 1).padStart(2, '0')}</span><span>{item.short}</span>
        <span className={`agent-signal ${itemStep?.status === 'completed' && itemStep.result?.trim() ? 'has-output' : ''}`} aria-label={itemStep?.status ?? 'Not in snapshot'} />
      </button>;
    })}</nav>
    <div className="result-provenance"><FileSearch size={16} /><p>These are <strong>agent-reported proposals</strong> from a manually imported, unverified snapshot. “Completed” describes an agent step, not completed KT, verified calendar availability or release authorization.</p></div>
    <section className="mission-panel result-document" aria-label={agent.name}>
      <header className="result-document-heading"><div><p className="mission-eyebrow">Agent {agent.id} / stages {agent.stages}</p><h3>{agent.name}</h3><p>{agent.description}</p></div>
        <span className="status-pill">{step?.status ?? 'Not in snapshot'}</span></header>
      {output.kind === 'empty' && <div className="empty-state"><FileSearch size={30} /><h4>No output supplied</h4><p>This agent is missing from the snapshot or returned an empty result. Nothing has been generated to fill the gap.</p></div>}
      {output.kind === 'invalid' && <div className="mission-notice" role="alert">{output.message}</div>}
      {output.kind === 'text' && agentId !== 143 && <div className="output-prose">{output.text}</div>}
      {agentId === 143 && output.kind !== 'empty' && <WorkflowReport run={run} embedded />}
      {output.kind === 'json' && agentId !== 143 && <div className="result-sections">
        {isRecord(output.value) ? orderedFields(agentId, output.value).map(([key, value]) => <section key={key} className="result-section">
          <h4><span className="section-marker" />{fieldLabel(key)}{Array.isArray(value) && <span className="section-count">{value.length} items</span>}</h4>
          <StructuredOutput value={value} />
        </section>) : <StructuredOutput value={output.value} />}
      </div>}
      {step?.result && <details className="raw-output"><summary><Braces size={15} /> Original agent response <ArrowUpRight size={13} /></summary><p>Preserved as imported. Use this to check the formatted presentation against the source.</p><pre>{step.result}</pre></details>}
    </section>
    <div className="result-footer"><CheckCircle2 size={15} /><span>Formatting only. Viewing results does not execute agents, update operational records or send messages.</span></div>
  </section>;
}
