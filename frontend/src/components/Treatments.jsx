import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function Treatments() {
  const [categories, setCategories] = useState(null)
  const [selectedKey, setSelectedKey] = useState(null)
  const [detail, setDetail] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.listTreatments()
      .then((data) => {
        setCategories(data.categories)
        if (data.categories.length > 0) setSelectedKey(data.categories[0].key)
      })
      .catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    if (!selectedKey) return
    api.getTreatmentDetail(selectedKey).then(setDetail).catch((err) => setError(err.message))
  }, [selectedKey])

  if (error) return <p className="error-text">{error}</p>
  if (!categories) return <p className="loading-text">Loading…</p>

  return (
    <div>
      <div className="report-context-toggle" style={{ marginBottom: 24 }}>
        ℹ This is general educational information, not personalized medical advice. Always
        discuss any treatment approach — conventional or alternative — with your doctor first.
      </div>

      <div className="tab-row" style={{ flexWrap: 'wrap' }}>
        {categories.map((c) => (
          <button
            key={c.key}
            className={`tab ${selectedKey === c.key ? 'active' : ''}`}
            onClick={() => setSelectedKey(c.key)}
          >
            {c.title}
          </button>
        ))}
      </div>

      {detail && (
        <div>
          <h3 className="section-heading" style={{ fontSize: 20 }}>{detail.title}</h3>
          <p style={{ color: 'var(--ink-soft)', marginBottom: 20 }}>{detail.summary}</p>
          <div className="visit-list">
            {detail.points.map((point, i) => (
              <div key={i} style={{ padding: '14px 0', borderBottom: i < detail.points.length - 1 ? '1px solid var(--line)' : 'none', fontSize: 14.5 }}>
                {point}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
