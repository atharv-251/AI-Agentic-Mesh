import { ArrowRight, Database, GitBranch, HardDrive, Monitor, ShieldCheck } from 'lucide-react';

export function IntegrationMap() {
  return <section className="mission-panel integration-map" aria-label="How Amplify connects">
    <div className="section-heading"><div><p className="mission-eyebrow">System architecture / current connection</p><h2>One workflow. Clear boundaries.</h2><p>The app is your workspace. Amplify is the mandatory planning engine.</p></div><ShieldCheck className="text-cyan-300" size={25} /></div>
    <div className="integration-flow">
      <article><Monitor size={22} /><h3>Standalone app</h3><p>Upload sources, explore results and approve reviewed work.</p><span className="status-pill">Browser</span></article>
      <ArrowRight className="flow-arrow" size={18} />
      <article><HardDrive size={22} /><h3>Local backend</h3><p>Extracts documents and submits a token-authenticated API request.</p><span className="status-pill status-connected">Submission supported</span></article>
      <ArrowRight className="flow-arrow" size={18} />
      <article><GitBranch size={22} /><h3>Amplify / 167</h3><p>Seven connected agents analyze, plan and prepare outputs.</p><span className="status-pill">Mandatory execution</span></article>
    </div>
    <div className="integration-return"><span className="status-pill status-warning">Manual return today</span><p>Amplify Full JSON <ArrowRight size={13} /> explicit import <ArrowRight size={13} /> human review <ArrowRight size={13} /> backend <ArrowRight size={13} /> local database</p></div>
    <div className="grid gap-5 md:grid-cols-2">
      <div className="architecture-note"><Database size={20} /><div><h3>Can Amplify write to the database?</h3><p>Yes, in an architecture with an approved write-capable connector and a reachable database. The Amplify SQL tool inspected here is read-only, and workstation LocalDB is not reachable from the cloud. No direct database write connection is configured.</p></div></div>
      <div className="architecture-note"><ShieldCheck size={20} /><div><h3>Recommended automatic return</h3><p>An authenticated, hosted ingestion API: Amplify posts completed results; the backend validates run identity and stores them; this app fetches saved data. A shared SQL database is another option only if a supported write connector is provisioned. Both require approved hosting, access controls and connectivity.</p></div></div>
    </div>
    <p className="mission-notice">Automatic return is not active. No supported native result-retrieval contract was found. Neither an agent “completed” status nor a stored token proves database writes or live synchronization.</p>
  </section>;
}
