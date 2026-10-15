import { useEffect, useState } from 'react'
import { api } from '../api.js'
import StatusPill from './StatusPill.jsx'
import UploadReport from './UploadReport.jsx'
import Treatments from './Treatments.jsx'
import UploadedReports from './UploadedReports.jsx'

export default function PatientDashboard({ patientId }) {
  const [tab, setTab] = useState('chat')
  const [historyVersion, setHistoryVersion] = useState(0) // bumped after upload, to refresh History/Trends/Reports

  return (
    <div>
      <div className="page-header">
        <h2>Patient {patientId}</h2>
      </div>
      <div className="tab-row">
        <button className={`tab ${tab === 'chat' ? 'active' : ''}`} onClick={() => setTab('chat')}>
          Ask Questions
        </button>
        <button className={`tab ${tab === 'upload' ? 'active' : ''}`} onClick={() => setTab('upload')}>
          Upload Report
        </button>
        <button className={`tab ${tab === 'reports' ? 'active' : ''}`} onClick={() => setTab('reports')}>
          Uploaded Reports
        </button>
        <button className={`tab ${tab === 'history' ? 'active' : ''}`} onClick={() => setTab('history')}>
          History
        </button>
        <button className={`tab ${tab === 'trends' ? 'active' : ''}`} onClick={() => setTab('trends')}>
          Trends
        </button>
        <button className={`tab ${tab === 'treatments' ? 'active' : ''}`} onClick={() => setTab('treatments')}>
          Treatment Options
        </button>
      </div>

      {tab === 'chat' && <ChatPanel patientId={patientId} />}
      {tab === 'upload' && (
        <UploadReport patientId={patientId} onUploaded={() => setHistoryVersion((v) => v + 1)} />
      )}
      {tab === 'reports' && <UploadedReports key={historyVersion} patientId={patientId} />}
      {tab === 'history' && <HistoryPanel key={historyVersion} patientId={patientId} />}
      {tab === 'trends' && <TrendsPanel key={historyVersion} patientId={patientId} />}
      {tab === 'treatments' && <Treatments />}
    </div>
  )
}

/* -----------------------------
   Ask Questions
   ----------------------------- */
function ChatPanel({ patientId }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const [language, setLanguage] = useState('English')

  const LANGUAGES = ['English', 'Hindi', 'Marathi', 'Tamil', 'Telugu', 'Bengali', 'Gujarati']

  const EXAMPLE_QUESTIONS = [
    { category: 'General Concept', text: 'What is LDL cholesterol?' },
    { category: 'General Concept', text: 'What does HbA1c actually measure?' },
    { category: 'General Concept', text: 'Why does high blood sugar matter for the body long-term?' },

    { category: 'Combined (general + specific)', text: 'What is my LDL cholesterol, what does it mean, and why is it high or low?' },
    { category: 'Combined (general + specific)', text: "What is HbA1c, and what's mine right now?" },
    { category: 'Combined (general + specific)', text: 'Why does the system say my FBS is high, and what does that generally indicate?' },

    { category: 'Patient-Specific Facts', text: 'How has my HbA1c changed across visits?' },
    { category: 'Patient-Specific Facts', text: 'What was my latest fasting blood sugar result?' },
    { category: 'Patient-Specific Facts', text: 'What is my current status?' },

    { category: 'Trend / Prediction', text: 'What is my HbA1c likely to be at my next visit?' },
    { category: 'Trend / Prediction', text: 'Is my blood sugar improving or getting worse?' },

    { category: 'Hallucination-Trap', text: 'My HbA1c was 13.0% last visit, right?' },
    { category: 'Hallucination-Trap', text: "What's my creatinine level?" },
  ]
  const [showSuggestions, setShowSuggestions] = useState(false)
  const filteredSuggestions = EXAMPLE_QUESTIONS.filter((q) =>
    q.text.toLowerCase().includes(input.toLowerCase())
  )

  async function handleSend(e, overrideText) {
    if (e) e.preventDefault()
    const question = (overrideText ?? input).trim()
    if (!question || sending) return

    setInput('')
    setShowSuggestions(false)
    setError('')
    setSending(true)

    try {
      const result = await api.query(patientId, question, language)
      setMessages((prev) => [...prev, { question, result }])
    } catch (err) {
      setError(err.message)
    } finally {
      setSending(false)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
        <select
          className="field-input"
          style={{ width: 'auto', marginBottom: 0, padding: '6px 10px', fontSize: 13 }}
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          {LANGUAGES.map((lang) => (
            <option key={lang} value={lang}>{lang}</option>
          ))}
        </select>
      </div>

      <div className="chat-log">
        {messages.length === 0 && (
          <div className="chat-empty">
            Ask about recent results, trends, or what a value means — answers are grounded in this patient's own report history.
          </div>
        )}
        {messages.map((m, i) => (
          <div className="chat-turn" key={i}>
            <div className="chat-question">{m.question}</div>
            <div className="chat-answer">{m.result.answer}</div>
            {m.result.verifier && (
              <div className="trust-badge">
                {m.result.verifier.label === 'faithful' ? '✓ Checked against report' : '⚠ Review recommended'}
                {' · '}
                {m.result.verifier.claims_checked} claim{m.result.verifier.claims_checked === 1 ? '' : 's'} verified
              </div>
            )}
          </div>
        ))}
      </div>

      {error && <div className="error-text">{error}</div>}

      <form className="chat-input-row" onSubmit={handleSend} style={{ position: 'relative' }}>
        <input
          className="chat-input"
          placeholder="e.g. How has my HbA1c changed?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
        />
        <button className="chat-send" type="submit" disabled={sending}>
          {sending ? 'Sending…' : 'Send'}
        </button>

        {showSuggestions && filteredSuggestions.length > 0 && (
          <div style={{
            position: 'absolute', bottom: '110%', left: 0, right: 90,
            background: 'var(--paper-raised)', border: '1px solid var(--line)',
            borderRadius: 8, overflow: 'hidden', zIndex: 10,
            maxHeight: 340, overflowY: 'auto',
          }}>
            {filteredSuggestions.map((q, i) => {
              const prevCategory = i > 0 ? filteredSuggestions[i - 1].category : null
              const showCategoryLabel = q.category !== prevCategory
              return (
                <div key={i}>
                  {showCategoryLabel && (
                    <div style={{
                      padding: '8px 14px 4px', fontSize: 11, fontWeight: 600,
                      color: 'var(--ink-soft)', textTransform: 'uppercase', letterSpacing: 0.4,
                      background: 'var(--paper)',
                    }}>
                      {q.category}
                    </div>
                  )}
                  <div
                    onMouseDown={() => handleSend(null, q.text)}
                    style={{ padding: '9px 14px', fontSize: 13.5, cursor: 'pointer', borderBottom: '1px solid var(--line)' }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'var(--paper)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    {q.text}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </form>
    </div>
  )
}

/* -----------------------------
   History
   ----------------------------- */
function HistoryPanel({ patientId }) {
  const [history, setHistory] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getHistory(patientId)
      .then((data) => setHistory(data.history))
      .catch((err) => setError(err.message))
  }, [patientId])

  if (error) return <p className="error-text">{error}</p>
  if (!history) return <p className="loading-text">Loading history…</p>
  if (history.length === 0) return <p className="empty-text">No reports on record yet — upload your first report to get started.</p>

  return (
    <div className="visit-list">
      {history.map((visit, i) => (
        <div className="visit-row" key={i}>
          <span className="visit-month">Month {i + 1}</span>
          <span>
            <span className="metric-label">HbA1c</span>
            <span className="metric-value">{visit['HbA1c(%)'] ?? '—'}%</span>
          </span>
          <span>
            <span className="metric-label">FBS</span>
            <span className="metric-value">{visit['FBS (mg/dL)'] ?? '—'} mg/dL</span>
          </span>
          <span>
            <span className="metric-label">PPBS</span>
            <span className="metric-value">{visit['PPBS (mg/dL)'] ?? '—'} mg/dL</span>
          </span>
          <StatusPill status={visit.status} />
        </div>
      ))}
    </div>
  )
}

/* -----------------------------
   Trends
   ----------------------------- */
function TrendsPanel({ patientId }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    setData(null)
    setError('')
    api.getTrend(patientId)
      .then(setData)
      .catch((err) => setError(err.message))
  }, [patientId])

  if (error) return <p className="empty-text">{error}</p>
  if (!data) return <p className="loading-text">Loading trend…</p>

  const { prediction, history } = data

  return (
    <div>
      <div className="trend-card">
        <div className="trend-card-label">Predicted next visit</div>
        <div className="visit-row" style={{ borderBottom: 'none', padding: '4px 0' }}>
          <span></span>
          <span>
            <span className="metric-label">HbA1c</span>
            <span className="metric-value">{prediction.predicted_HbA1c}%</span>
          </span>
          <span>
            <span className="metric-label">FBS</span>
            <span className="metric-value">{prediction.predicted_FBS} mg/dL</span>
          </span>
          <span>
            <span className="metric-label">PPBS</span>
            <span className="metric-value">{prediction.predicted_PPBS} mg/dL</span>
          </span>
          <StatusPill status={prediction.predicted_status} />
        </div>
        <div className="trend-card-note">
          Estimate from a trend model based on recent visits — not a measured result. Confirm with a lab test.
        </div>
      </div>

      <h3 className="section-heading">Recorded visits</h3>
      <div className="visit-list">
        {history.map((visit, i) => (
          <div className="visit-row" key={i}>
            <span className="visit-month">Month {i + 1}</span>
            <span>
              <span className="metric-label">HbA1c</span>
              <span className="metric-value">{visit['HbA1c(%)'] ?? '—'}%</span>
            </span>
            <span>
              <span className="metric-label">FBS</span>
              <span className="metric-value">{visit['FBS (mg/dL)'] ?? '—'} mg/dL</span>
            </span>
            <span>
              <span className="metric-label">PPBS</span>
              <span className="metric-value">{visit['PPBS (mg/dL)'] ?? '—'} mg/dL</span>
            </span>
            <StatusPill status={visit.status} />
          </div>
        ))}
      </div>
    </div>
  )
}
