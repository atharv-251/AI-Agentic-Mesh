export type OutputValue = null | boolean | number | string | OutputValue[] | { [key: string]: OutputValue };

export type ParsedOutput =
  | { kind: 'json'; value: OutputValue }
  | { kind: 'text'; text: string }
  | { kind: 'invalid'; text: string; message: string }
  | { kind: 'empty' };

export function parseOutput(result: string | null | undefined): ParsedOutput {
  if (!result?.trim()) return { kind: 'empty' };
  const text = result.trim();
  const fenced = text.match(/^```(?:json)?\s*\n([\s\S]*?)\n```$/i);
  const candidate = fenced ? fenced[1].trim() : text;
  if (!/^[{\[]/.test(candidate)) return { kind: 'text', text: result };
  try {
    return { kind: 'json', value: JSON.parse(candidate) as OutputValue };
  } catch {
    return { kind: 'invalid', text: result, message: 'This output looks like JSON but could not be parsed. The original response is preserved below; no fields have been inferred.' };
  }
}

export function isRecord(value: OutputValue): value is { [key: string]: OutputValue } {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

export function fieldLabel(key: string): string {
  return key.replace(/[_-]+/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/\b\w/g, letter => letter.toUpperCase());
}

export function recordTitle(value: { [key: string]: OutputValue }, index: number): string {
  for (const key of ['name', 'topic', 'title', 'check', 'source_name', 'kt_level', 'local_session_id', 'stakeholder_id']) {
    if (typeof value[key] === 'string' && value[key].trim()) return value[key];
  }
  return `Item ${index + 1}`;
}

const FIELD_ORDER: Record<number, string[]> = {
  165: ['project_profile', 'settings', 'source_register', 'stakeholder_candidates', 'knowledge_candidates', 'proposed_slots', 'missing_inputs', 'source_conflicts'],
  166: ['stakeholders', 'knowledge_plan', 'level_matrix', 'missing_inputs', 'assumptions', 'source_refs'],
  167: ['capacity_worksheet', 'proposed_sessions', 'availability_checklist', 'missing_inputs', 'assumptions'],
  168: ['release_status', 'check_results', 'blockers', 'proposed_corrections', 'handover_outline', 'missing_inputs'],
  144: ['draft_subject', 'draft_body', 'proposed_recipients', 'proposed_sessions', 'delivery_blockers', 'delivery_results'],
  142: ['status', 'evidence_scope', 'tracking_template', 'findings', 'resolved_items', 'next_call_questions', 'missing_inputs'],
};

export function orderedFields(agentId: number, value: { [key: string]: OutputValue }): [string, OutputValue][] {
  const priority = FIELD_ORDER[agentId] ?? [];
  const entries = Object.entries(value);
  return [
    ...priority.filter(key => Object.prototype.hasOwnProperty.call(value, key)).map((key): [string, OutputValue] => [key, value[key]]),
    ...entries.filter(([key]) => !priority.includes(key)),
  ];
}
