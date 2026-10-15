import { useState } from 'react'
import { api } from '../api.js'

export default function Signup({ onSignedUp, onBackToLogin }) {
  const [name, setName] = useState('')
  const [age, setAge] = useState('')
  const [gender, setGender] = useState('Female')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!name.trim() || !age || !password) {
      setError('Please fill in all fields.')
      return
    }
    setLoading(true)
    try {
      const result = await api.signup(name.trim(), age, gender, password)
      onSignedUp(result)
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
          <div className="login-hero-headline">Get started in under a minute.</div>
          <p className="login-hero-sub" style={{ marginTop: 18 }}>
            Create an account, then upload your first lab report — MediRAG will extract your
            results automatically and you can start asking questions right away.
          </p>
        </div>
        <div className="login-hero-foot">
          MediRAG is a decision-support tool, not a substitute for medical advice.
        </div>
      </div>

      <div className="login-form-side">
        <form className="login-card" onSubmit={handleSubmit}>
          <h1>Create your account</h1>
          <p className="login-sub">You'll be assigned a patient ID once you sign up.</p>

          <label className="field-label" htmlFor="name">Full name</label>
          <input
            id="name"
            className="field-input"
            placeholder="e.g. Anjali Desai"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <label className="field-label" htmlFor="age">Age</label>
          <input
            id="age"
            type="number"
            className="field-input"
            placeholder="e.g. 36"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />

          <label className="field-label" htmlFor="gender">Gender</label>
          <select
            id="gender"
            className="field-input"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
          >
            <option>Female</option>
            <option>Male</option>
            <option>Other</option>
          </select>

          <label className="field-label" htmlFor="signupPassword">Create a password</label>
          <div className="password-field-wrapper">
            <input
              id="signupPassword"
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
            {loading ? 'Creating account...' : 'Create account'}
          </button>

          <p className="login-sub" style={{ marginTop: 18, marginBottom: 0, textAlign: 'center' }}>
            Already have an account?{' '}
            <button type="button" className="text-button" onClick={onBackToLogin}>
              Sign in
            </button>
          </p>
        </form>
      </div>
    </div>
  )
}
