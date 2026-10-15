import { useState } from 'react'
import { api } from '../api.js'

export default function Login({ onLogin, onGoToSignup }) {
  const [role, setRole] = useState('doctor')
  const [patientId, setPatientId] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const result = await api.login(role, role === 'patient' ? patientId.trim() : null, password)
      onLogin(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-shell">
      <div className="login-hero">
        <div className="login-hero-brand">
          <div className="login-hero-mark">M</div>
          MediRAG
        </div>

        <div>
          <div className="login-hero-headline">Lab results, explained in plain language.</div>
          <p className="login-hero-sub" style={{ marginTop: 18 }}>
            MediRAG reads your diabetes lab reports, tracks how your numbers change over time,
            and answers your questions — every answer grounded in your own report and checked
            for accuracy before you see it.
          </p>

          <div className="login-hero-features" style={{ marginTop: 36 }}>
            <div className="login-hero-feature">
              <span className="login-hero-feature-dot" />
              Upload a report and get an instant, grounded summary
            </div>
            <div className="login-hero-feature">
              <span className="login-hero-feature-dot" />
              Ask questions about your results in plain English
            </div>
            <div className="login-hero-feature">
              <span className="login-hero-feature-dot" />
              See trends across visits, with a forecast for what's next
            </div>
            <div className="login-hero-feature">
              <span className="login-hero-feature-dot" />
              Every answer is checked against your actual report before it's shown
            </div>
          </div>
        </div>

        <div className="login-hero-foot">
          MediRAG is a decision-support tool, not a substitute for medical advice. Always confirm results with your doctor.
        </div>
      </div>

      <div className="login-form-side">
        <form className="login-card" onSubmit={handleSubmit}>
          <h1>Sign in</h1>
          <p className="login-sub">Continue as a doctor or a patient.</p>

          <div className="role-toggle">
            <button
              type="button"
              className={`role-option ${role === 'doctor' ? 'active' : ''}`}
              onClick={() => setRole('doctor')}
            >
              Doctor
            </button>
            <button
              type="button"
              className={`role-option ${role === 'patient' ? 'active' : ''}`}
              onClick={() => setRole('patient')}
            >
              Patient
            </button>
          </div>

          {role === 'patient' && (
            <>
              <label className="field-label" htmlFor="patientId">Patient ID</label>
              <input
                id="patientId"
                className="field-input"
                placeholder="e.g. P032"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
              />
            </>
          )}

          <label className="field-label" htmlFor="password">Password</label>
          <div className="password-field-wrapper">
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              className="field-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              className="password-toggle-btn"
              onClick={() => setShowPassword((v) => !v)}
              tabIndex={-1}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>

          {error && <div className="error-text">{error}</div>}

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Continue'}
          </button>

          {role === 'patient' && (
            <p className="login-sub" style={{ marginTop: 18, marginBottom: 0, textAlign: 'center' }}>
              New patient?{' '}
              <button type="button" className="text-button" onClick={onGoToSignup}>
                Create an account
              </button>
            </p>
          )}
        </form>
      </div>
    </div>
  )
}
