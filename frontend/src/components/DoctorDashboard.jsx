import { useEffect, useState } from 'react'
import { api } from '../api.js'
import StatusPill from './StatusPill.jsx'

export default function DoctorDashboard({ onSelectPatient }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.listPatients()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <p className="error-text">{error}</p>
  if (!data) return <p className="loading-text">Loading patients…</p>

  return (
    <div>
      <div className="page-header">
        <h2>Original Cohort ({data.original_patients.length})</h2>
      </div>
      <div className="ledger">
        <div className="ledger-header">
          <span>Patient ID</span>
          <span>Latest HbA1c</span>
          <span>Status</span>
          <span>Months on record</span>
        </div>
        {data.original_patients.map((p) => (
          <button key={p.patient_id} className="ledger-row" onClick={() => onSelectPatient(p.patient_id)}>
            <span className="ledger-row-id">{p.patient_id}</span>
            <span>{p.latest_hba1c}%</span>
            <span><StatusPill status={p.latest_status} /></span>
            <span>{p.months_on_record}</span>
          </button>
        ))}
      </div>

      <div className="page-header" style={{ marginTop: 40 }}>
        <h2>Newly Registered ({data.newly_registered_patients.length})</h2>
      </div>
      {data.newly_registered_patients.length === 0 ? (
        <p className="empty-text">No patients have signed up yet.</p>
      ) : (
        <div className="ledger">
          <div className="ledger-header">
            <span>Patient ID</span>
            <span>Name</span>
            <span>Status</span>
            <span>Months on record</span>
          </div>
          {data.newly_registered_patients.map((p) => (
            <button key={p.patient_id} className="ledger-row" onClick={() => onSelectPatient(p.patient_id)}>
              <span className="ledger-row-id">{p.patient_id}</span>
              <span>{p.name}</span>
              <span>{p.latest_status !== 'No reports yet' ? <StatusPill status={p.latest_status} /> : <span className="metric-label">No reports yet</span>}</span>
              <span>{p.months_on_record}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
