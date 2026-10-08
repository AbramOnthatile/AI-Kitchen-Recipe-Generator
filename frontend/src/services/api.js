const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  const responseText = await response.text()
  let data = {}
  try {
    data = responseText ? JSON.parse(responseText) : {}
  } catch {
    data = { error: responseText || 'The backend returned an invalid response.' }
  }
  if (!response.ok) {
    const detail = data.detail || data.error || data.message
    throw new Error(`API error ${response.status}: ${detail || 'The request could not be completed.'}`)
  }
  return data
}

export const api = {
  generate: (ingredients, platform = 'Instagram') => request('/api/recipes/generate-all/', { method: 'POST', body: JSON.stringify({ ingredients, platform }) }),
  getPrompts: () => request('/api/prompts/'),
  createPrompt: (prompt) => request('/api/prompts/', { method: 'POST', body: JSON.stringify(prompt) }),
  updatePrompt: (id, prompt) => request(`/api/prompts/${id}/`, { method: 'PUT', body: JSON.stringify(prompt) }),
  deletePrompt: (id) => request(`/api/prompts/${id}/`, { method: 'DELETE' }),
  optimizePrompt: (prompt, goal = '') => request('/api/prompts/optimize/', { method: 'POST', body: JSON.stringify({ prompt, goal }) }),
  analysePrompt: (prompt) => request('/api/prompts/analyse/', { method: 'POST', body: JSON.stringify({ prompt }) }),
  getHistory: () => request('/api/history/'),
  deleteHistory: (id) => request(`/api/history/${id}/`, { method: 'DELETE' }),
  health: () => request('/api/health/'),
}
