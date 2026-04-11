import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    username: null,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    displayName: (state) => state.username ?? 'Гость',
  },
  
  actions: {
    async register(username, email, password) {
      const res = await api.post('/auth/register', {
        username,
        email,
        password,
      })
      this.token = res.data.access_token || null
      if (this.token) {
        localStorage.setItem('token', this.token)
      }
      // try to fetch current user after registration
      try {
        await this.fetchMe()
      } catch {
        // ignore
      }
      return res.data
    },
    
    async login(emailOrUsername, password) {
      const res = await api.post('/auth/login', {
        email: emailOrUsername,
        email_or_username: emailOrUsername,
        password,
      })
      this.token = res.data.access_token
      localStorage.setItem('token', res.data.access_token)
      // fetch current user after login
      try {
        await this.fetchMe()
      } catch {
        // ignore
      }
    },
    
    logout() {
      this.token = null
      this.user = null
      this.username = null
      localStorage.removeItem('token')
    },
    
    init() {
      if (this.token) {
        this.fetchMe().catch(() => {})
      }
    },

    async fetchMe() {
      try {
        const res = await api.get('/auth/me')
        this.username = res.data?.username ?? null
        this.user = res.data ?? null
        return res.data
      } catch (e) {
        throw e
      }
    },
    setUsername(name) {
      this.username = name
    },
  },
})
