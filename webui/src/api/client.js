import axios from 'axios'
import { API_BASE_URL, getApiKey } from './config'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add API key to every request (reads from localStorage)
client.interceptors.request.use((config) => {
  const apiKey = getApiKey()
  if (apiKey) {
    config.headers['X-API-Key'] = apiKey
  }
  return config
})

// Response interceptor for error handling
client.interceptors.response.use(
  response => response,
  error => {
    const message = error.response?.data?.detail || error.message
    console.error('API Error:', message)
    return Promise.reject(error)
  }
)

export default client
