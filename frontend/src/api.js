const BASE = '/api'

async function request(url, options) {
  const response = await fetch(`${BASE}${url}`, options)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return response.json()
}

export function listSessions() {
  return request('/sessions/')
}

export function createSession(title, workspace) {
  const params = new URLSearchParams({ title, workspace })
  return request(`/sessions/?${params}`, { method: 'POST' })
}

export function getSession(sessionId) {
  return request(`/sessions/${sessionId}`)
}

export function sendMessage(sessionId, message) {
  return request(`/sessions/${sessionId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })
}

export function deactivateSession(sessionId) {
  return request(`/sessions/${sessionId}`, { method: 'DELETE' })
}
