import { useState } from 'react'
import Login from './components/Login.jsx'
import Signup from './components/Signup.jsx'
import DoctorDashboard from './components/DoctorDashboard.jsx'
import PatientDashboard from './components/PatientDashboard.jsx'

export default function App() {
  const [authView, setAuthView] = useState('login') // 'login' | 'signup'
  const [session, setSession] = useState(null)
  const [viewingPatientId, setViewingPatientId] = useState(null)
  const [justSignedUpId, setJustSignedUpId] = useState(null)

  function handleLogout() {
    setSession(null)
    setViewingPatientId(null)
    setAuthView('login')
  }

  function handleSignedUp(result) {
    setJustSignedUpId(result.patient_id)
    setSession(result)
  }

  if (!session) {
    if (authView === 'signup') {
      return <Signup onSignedUp={handleSignedUp} onBackToLogin={() => setAuthView('login')} />
    }
    return <Login onLogin={setSession} onGoToSignup={() => setAuthView('signup')} />
  }

  const activePatientId = session.role === 'patient' ? session.patient_id : viewingPatientId

  return (
    <div className="app-shell">
      <div className="topbar">
        <div className="topbar-left">
          <div className="topbar-title">
            <div className="topbar-mark">M</div>
            MediRAG
          </div>
          {session.role === 'doctor' && (
            <div className="topbar-nav">
              <button
                className={`topbar-nav-link ${!activePatientId ? 'active' : ''}`}
                onClick={() => setViewingPatientId(null)}
              >
                All Patients
              </button>
              {activePatientId && (
                <span className="topbar-nav-link active">Patient {activePatientId}</span>
              )}
            </div>
          )}
        </div>
        <div className="topbar-meta">
          <span className="pill-button">
            {session.role === 'doctor' ? 'Doctor' : `Patient ${session.patient_id}`}
          </span>
          <button className="text-button" onClick={handleLogout}>Log out</button>
        </div>
      </div>

      <div className="main-area">
        {justSignedUpId && session.role === 'patient' && (
          <div className="report-context-toggle" style={{ marginBottom: 24 }}>
            ✓ Account created! Your patient ID is <strong>&nbsp;{justSignedUpId}&nbsp;</strong> —
            save this to log in next time. Upload your first report below to get started.
            <button
              className="text-button"
              style={{ marginLeft: 'auto' }}
              onClick={() => setJustSignedUpId(null)}
            >
              Dismiss
            </button>
          </div>
        )}

        {session.role === 'doctor' && !activePatientId && (
          <DoctorDashboard onSelectPatient={setViewingPatientId} />
        )}
        {activePatientId && <PatientDashboard patientId={activePatientId} />}
      </div>
    </div>
  )
}
