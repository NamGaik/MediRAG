import { useState, useRef } from 'react'
import { api } from '../api.js'

export default function UploadReport({ patientId, onUploaded }) {
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [mode, setMode] = useState('file') // 'file' | 'paste'
  const [pastedText, setPastedText] = useState('')
  const inputRef = useRef(null)

  async function handleFile(file) {
    if (!file) return
    setError('')
    setUploading(true)
    setResult(null)
    try {
      const data = await api.uploadReport(patientId, file)
      setResult(data)
      if (onUploaded) onUploaded()
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  async function handlePasteSubmit() {
    if (!pastedText.trim()) return
    setError('')
    setUploading(true)
    setResult(null)
    try {
      const data = await api.uploadReportText(patientId, pastedText)
      setResult(data)
      setPastedText('')
      if (onUploaded) onUploaded()
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files?.[0]
    handleFile(file)
  }

  return (
    <div>
      <div className="tab-row" style={{ marginBottom: 20, borderBottom: 'none' }}>
        <button className={`tab ${mode === 'file' ? 'active' : ''}`} onClick={() => setMode('file')}>
          Upload File
        </button>
        <button className={`tab ${mode === 'paste' ? 'active' : ''}`} onClick={() => setMode('paste')}>
          Paste Text
        </button>
      </div>

      {mode === 'file' ? (
        <div
          className={`upload-zone ${dragging ? 'dragging' : ''}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          <div className="upload-zone-icon">📄</div>
          <div className="upload-zone-title">
            {uploading ? 'Reading report…' : 'Drop a lab report here, or click to browse'}
          </div>
          <div className="upload-zone-sub">Supports PDF, JPG, PNG, or TXT — saved permanently as a new visit</div>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png,.txt"
            style={{ display: 'none' }}
            onChange={(e) => handleFile(e.target.files?.[0])}
          />
        </div>
      ) : (
        <div>
          <textarea
            className="field-input"
            style={{ minHeight: 180, fontFamily: 'var(--font-sans)', resize: 'vertical' }}
            placeholder={'Paste report text here, e.g.:\nHbA1c: 7.2% (Classification: Diabetic)\nFasting Blood Sugar (FBS): 138 mg/dL (Classification: Diabetic)'}
            value={pastedText}
            onChange={(e) => setPastedText(e.target.value)}
          />
          <button className="primary-button" onClick={handlePasteSubmit} disabled={uploading || !pastedText.trim()}>
            {uploading ? 'Saving…' : 'Save as new visit'}
          </button>
        </div>
      )}

      {error && <div className="error-text" style={{ marginTop: 16 }}>{error}</div>}

      {result && (
        <div className="upload-result">
          <div className="report-context-toggle" style={{ marginBottom: 20 }}>
            ✓ {result.message}
          </div>

          <div className="upload-result-header">
            <h3 className="section-heading" style={{ marginBottom: 0 }}>
              Extracted from {result.filename}
            </h3>
          </div>

          {result.structured_values.length > 0 ? (
            <div className="upload-values-grid">
              {result.structured_values.map((v, i) => (
                <div className="upload-value-card" key={i}>
                  <div className="upload-value-marker">{v.marker}</div>
                  <div className="upload-value-number">{v.value}{v.unit}</div>
                  {v.label && <div className="metric-label">{v.label}</div>}
                </div>
              ))}
            </div>
          ) : (
            <p className="empty-text" style={{ marginBottom: 20 }}>
              No structured biomarker values were automatically recognized — the raw extracted text is shown below.
            </p>
          )}

          <h3 className="section-heading">Raw extracted text</h3>
          <div className="upload-raw-text">{result.extracted_text}</div>
        </div>
      )}
    </div>
  )
}
