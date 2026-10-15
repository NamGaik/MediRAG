const API_BASE = 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export const api = {
  login: (role, patientId, password) =>
    request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ role, patient_id: patientId || null, password }),
    }),

  signup: (name, age, gender, password) =>
    request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, age: Number(age), gender, password }),
    }),

  listPatients: () => request('/patients'),

  getHistory: (patientId) => request(`/patients/${patientId}/history`),

  getTrend: (patientId) => request(`/patients/${patientId}/trend`),

  query: (patientId, queryText, language = 'English') =>
    request('/query', {
      method: 'POST',
      body: JSON.stringify({ patient_id: patientId, query_text: queryText, language }),
    }),

  uploadReport: async (patientId, file) => {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch(`${API_BASE}/patients/${patientId}/upload`, {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      throw new Error(body.detail || `Upload failed (${res.status})`)
    }
    return res.json()
  },

  uploadReportText: (patientId, text) =>
    request(`/patients/${patientId}/upload-text`, {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),

  listUploadedReports: (patientId) => request(`/patients/${patientId}/reports`),

  getUploadedReportFileUrl: (patientId, storedFilename) =>
    `${API_BASE}/patients/${patientId}/reports/${storedFilename}`,

  listTreatments: () => request('/treatments'),

  getTreatmentDetail: (categoryKey) => request(`/treatments/${categoryKey}`),
}