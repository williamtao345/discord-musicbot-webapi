// API Configuration
export const API_BASE_URL = '/api'

// Read API key from localStorage (set in Settings page)
export const getApiKey = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('musicbot_api_key') || ''
  }
  return ''
}
