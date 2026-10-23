import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import api from '@/services/api'

type User = { id: number; username: string; display_name?: string; is_staff?: boolean }

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(JSON.parse(localStorage.getItem('current_user') || 'null'))
  const isLoggedIn = computed(() => !!localStorage.getItem('access_token'))
  const isStaff = computed(() => !!user.value?.is_staff)

  async function login(username: string, password: string) {
    const response = await api.post('/token/', { username, password })
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    const me = await api.get('/auth/me/')
    user.value = me.data
    localStorage.setItem('current_user', JSON.stringify(me.data))
  }

  async function register(username: string, password: string, display_name: string) {
    await api.post('/auth/register/', { username, password, display_name })
    await login(username, password)
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('current_user')
    user.value = null
  }

  return { user, isLoggedIn, isStaff, login, register, logout }
})
