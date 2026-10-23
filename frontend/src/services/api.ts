import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')

  const url = (config.url ?? '').split('?')[0].replace(/\/+$/, '')
  const isPublicProductRead =
      config.method?.toLowerCase() === 'get' &&
      url.endsWith('/products')

  if (isPublicProductRead) {
    delete config.headers.Authorization
  } else if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export default api
