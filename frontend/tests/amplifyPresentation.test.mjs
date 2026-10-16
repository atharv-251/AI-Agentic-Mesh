import assert from 'node:assert/strict';
import test from 'node:test';
import { fieldLabel, isRecord, orderedFields, parseOutput, recordTitle } from '../src/components/pages/amplifyPresentation.ts';

test('structured agent output is preserved, including unknown fields, false, zero and null', () => {
  const value = {
    profile: { value: 'Synthetic application', citation: 'source.txt section 1' },
    messages_sent: false, actual_hours: 0, transcript_id: null, findings: [],
    future_contract: { nested: [{ text: '<script>not executable</script>', empty: '' }] },
  };
  assert.deepEqual(parseOutput(JSON.stringify(value)), { kind: 'json', value });
});

test('fenced JSON and array output are presented without replacing their fields', () => {
  assert.deepEqual(parseOutput('```json\n{"people":[{"name":"SME"}]}\n```'), {
    kind: 'json', value: { people: [{ name: 'SME' }] },
  });
  assert.deepEqual(parseOutput('[{"name":"SME"},null,false]'), {
    kind: 'json', value: [{ name: 'SME' }, null, false],
  });
});

test('missing outputs do not become successful empty plans', () => {
  for (const value of [undefined, null, '', ' \n\t']) assert.deepEqual(parseOutput(value), { kind: 'empty' });
});

test('malformed structured output is explicit and preserves original content', () => {
  const original = '  {"broken": \n';
  const parsed = parseOutput(original);
  assert.equal(parsed.kind, 'invalid');
  assert.equal(parsed.text, original);
  assert.match(parsed.message, /could not be parsed/);
  assert.match(parsed.message, /no fields have been inferred/);
});

test('text and Markdown reports are not rewritten as structured facts', () => {
  const report = '# Draft report\n\n**No messages sent**\n| State | Value |\n| --- | --- |\n| Draft | Yes |';
  assert.deepEqual(parseOutput(report), { kind: 'text', text: report });
});

test('record labels use supplied content, with clear fallback labels', () => {
  assert.equal(fieldLabel('calendar_availability_checked'), 'Calendar Availability Checked');
  assert.equal(fieldLabel('sourceRef'), 'Source Ref');
  assert.equal(recordTitle({ topic: 'Feed operations', local_session_id: 'T1' }, 0), 'Feed operations');
  assert.equal(recordTitle({ check: 'Source completeness' }, 0), 'Source completeness');
  assert.equal(recordTitle({ unknown: false }, 2), 'Item 3');
  assert.equal(isRecord(null), false);
  assert.equal(isRecord([]), false);
  assert.equal(isRecord({}), true);
});

test('business content is presented before metadata without losing unknown fields', () => {
  const original = { human_review_required: true, future_field: { unknown: false }, settings: {}, project_profile: { name: 'Synthetic' } };
  const ordered = orderedFields(165, original);
  assert.deepEqual(ordered.map(([key]) => key), ['project_profile', 'settings', 'human_review_required', 'future_field']);
  assert.deepEqual(Object.fromEntries(ordered), original);
  assert.deepEqual(orderedFields(999, original), Object.entries(original));
});
