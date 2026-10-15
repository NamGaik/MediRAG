import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function UploadedReports({ patientId }) {
  const [reports, setReports] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.listUploadedReports(patientId)
      .then((data) => setReports(data.reports))
      .catch((err) => setError(err.message))
  }, [patientId])

  if (error) return <p className="error-text">{error}</p>
  if (!reports) return <p className="loading-text">Loading reports…</p>

  return (
    <div>
      <div className="report-context-toggle" style={{ marginBottom: 20 }}>
        ℹ Original source files, exactly as uploaded — click any report to view the real document
        and independently verify the extracted values shown in History.
      </div>

      {reports.length === 0 ? (
        <p className="empty-text">
          No original files on record yet. Files uploaded via "Upload File" appear here —
          reports added by pasting text have no original document to show.
        </p>
      ) : (
        <div className="ledger">
          <div className="ledger-header">
            <span>Month</span>
            <span>Original Filename</span>
            <span>Uploaded</span>
            <span></span>
          </div>
          {reports.map((r, i) => (
            <a
              key={i}
              className="ledger-row"
              href={api.getUploadedReportFileUrl(patientId, r.stored_filename)}
              target="_blank"
              rel="noopener noreferrer"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <span className="ledger-row-id">Month {r.month}</span>
              <span>{r.filename}</span>
              <span className="metric-label">{new Date(r.uploaded_at).toLocaleDateString()}</span>
              <span className="text-button">View →</span>
            </a>
          ))}
        </div>
      )}
    </div>
  )
}
