import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access') || '')
  const refreshToken = ref(localStorage.getItem('refresh') || '')

  const isLoggedIn = computed(() => !!accessToken.value)

  async function login(username, password) {
    const res = await axios.post('/api/token/', { username, password })
    accessToken.value = res.data.access
    refreshToken.value = res.data.refresh
    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
  }

  async function refresh() {
    if (!refreshToken.value) return false
    try {
      const res = await axios.post('/api/token/refresh/', { refresh: refreshToken.value })
      accessToken.value = res.data.access
      localStorage.setItem('access', res.data.access)
      return true
    } catch {
      logout()
      return false
    }
  }

  function logout() {
    accessToken.value = ''
    refreshToken.value = ''
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
  }

  return { accessToken, refreshToken, isLoggedIn, login, refresh, logout }
})
