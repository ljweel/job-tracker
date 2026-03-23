import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true
      const auth = useAuthStore()
      const refreshed = await auth.refresh()
      if (refreshed) {
        error.config.headers.Authorization = `Bearer ${auth.accessToken}`
        return api(error.config)
      }
    }
    return Promise.reject(error)
  }
)

export default api
