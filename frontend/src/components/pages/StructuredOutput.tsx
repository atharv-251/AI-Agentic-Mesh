import { OutputValue, fieldLabel, isRecord, recordTitle } from './amplifyPresentation';

export function StructuredOutput({ value }: { value: OutputValue }) {
  if (value === null) return <span className="output-absent">Not supplied</span>;
  if (typeof value === 'boolean') return <span className="output-boolean">{value ? 'Yes' : 'No'}</span>;
  if (typeof value === 'number') return <span className="output-number">{value}</span>;
  if (typeof value === 'string') return value.trim()
    ? <span className="output-text">{value}</span>
    : <span className="output-absent">Empty value</span>;
  if (Array.isArray(value)) {
    if (!value.length) return <span className="output-absent">No items reported</span>;
    if (value.every(item => item === null || typeof item !== 'object')) {
      return <ul className="output-list">{value.map((item, index) => <li key={index}><StructuredOutput value={item} /></li>)}</ul>;
    }
    return <div className="output-records">{value.map((item, index) => <article key={index} className="output-record">
      <header><span className="output-index">{String(index + 1).padStart(2, '0')}</span><h4>{isRecord(item) ? recordTitle(item, index) : `Item ${index + 1}`}</h4></header>
      <StructuredOutput value={item} />
    </article>)}</div>;
  }
  if (!Object.keys(value).length) return <span className="output-absent">No fields reported</span>;
  if ('value' in value && Object.keys(value).every(key => ['value', 'citation', 'source_ref'].includes(key))) {
    return <div className="output-fact"><StructuredOutput value={value.value} />
      {value.citation !== undefined && <div className="output-citation"><span>Source</span><StructuredOutput value={value.citation} /></div>}
      {value.source_ref !== undefined && <div className="output-citation"><span>Reference</span><StructuredOutput value={value.source_ref} /></div>}
    </div>;
  }
  return <dl className="output-fields">{Object.entries(value).map(([key, item]) => <div key={key} className={`output-field ${item !== null && typeof item === 'object' ? 'output-field-nested' : ''}`}>
    <dt>{fieldLabel(key)}</dt><dd><StructuredOutput value={item} /></dd>
  </div>)}</dl>;
}
