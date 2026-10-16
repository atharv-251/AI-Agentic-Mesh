import { Fragment, ReactNode } from 'react';
import { Download, FileText } from 'lucide-react';
import { WorkflowRun } from '../../api/client';

function inline(text: string): ReactNode {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2, -2)}</strong>;
    if (part.startsWith('`') && part.endsWith('`')) return <code key={index}>{part.slice(1, -1)}</code>;
    return <Fragment key={index}>{part}</Fragment>;
  });
}

function markdownBlocks(text: string): ReactNode[] {
  const lines = text.split(/\r?\n/);
  const blocks: ReactNode[] = [];
  const cells = (line: string) => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(cell => cell.trim());
  for (let index = 0; index < lines.length;) {
    const line = lines[index];
    const key = index;
    if (!line.trim()) { index++; continue; }
    if (line.trim().startsWith('```')) {
      const code: string[] = [];
      index++;
      while (index < lines.length && !lines[index].trim().startsWith('```')) code.push(lines[index++]);
      if (index < lines.length) index++;
      blocks.push(<pre key={key}><code>{code.join('\n')}</code></pre>);
      continue;
    }
    if (line.includes('|') && index + 1 < lines.length && /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(lines[index + 1].trim())) {
      const headers = cells(line);
      const rows: string[][] = [];
      index += 2;
      while (index < lines.length && lines[index].trim() && lines[index].includes('|')) rows.push(cells(lines[index++]));
      blocks.push(<div className="report-table-wrap" tabIndex={0} role="region" aria-label={`Report table: ${headers.join(', ')}`} key={key}><table>
        <thead><tr>{headers.map((header, column) => <th key={column} scope="col">{inline(header)}</th>)}</tr></thead>
        <tbody>{rows.map((row, rowIndex) => <tr key={rowIndex}>{row.map((cell, column) => <td key={column}>{inline(cell)}</td>)}</tr>)}</tbody>
      </table></div>);
      continue;
    }
    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      blocks.push(heading[1].length <= 2 ? <h3 key={key}>{inline(heading[2])}</h3> : <h4 key={key}>{inline(heading[2])}</h4>);
      index++; continue;
    }
    if (/^\s*[-*]\s+/.test(line)) {
      const items: string[] = [];
      while (index < lines.length && /^\s*[-*]\s+/.test(lines[index])) items.push(lines[index++].replace(/^\s*[-*]\s+/, ''));
      blocks.push(<ul key={key}>{items.map((item, itemIndex) => <li key={itemIndex}>{inline(item)}</li>)}</ul>);
      continue;
    }
    if (/^\s*\d+\.\s+/.test(line)) {
      const items: string[] = [];
      const start = Number(line.trim().split('.')[0]);
      while (index < lines.length && /^\s*\d+\.\s+/.test(lines[index])) items.push(lines[index++].replace(/^\s*\d+\.\s+/, ''));
      blocks.push(<ol key={key} start={start}>{items.map((item, itemIndex) => <li key={itemIndex}>{inline(item)}</li>)}</ol>);
      continue;
    }
    if (/^\s*([-*_])(?:\s*\1){2,}\s*$/.test(line)) blocks.push(<hr key={key} />);
    else blocks.push(<p key={key}>{inline(line)}</p>);
    index++;
  }
  return blocks;
}

export function WorkflowReport({ run, embedded = false }: { run: WorkflowRun; embedded?: boolean }) {
  const report = run.snapshot.steps.find(step => step.agent_id === 143 && step.node_type === 'agent')?.result;
  if (!report) return null;
  return <section className={embedded ? 'report-embedded' : 'mission-panel'} aria-label="KT transition report">
    <div className="report-toolbar"><div><FileText size={20} /><span>Full agent deliverable<span className="block text-xs text-slate-400">Readable preview / original Markdown download</span></span></div>
      <a className="mission-button mission-button-secondary" href={`/api/v1/transitions/${encodeURIComponent(run.transition_id)}/workflow-runs/${encodeURIComponent(run.run_id)}/report`} download><Download size={15} /> Download .md</a>
    </div>
    <p className="mission-notice">Manually imported agent draft. Report statements are not independently verified; draft review is not operational release or evidence of KT completion.</p>
    <div className="report-prose">{markdownBlocks(report)}</div>
  </section>;
}
