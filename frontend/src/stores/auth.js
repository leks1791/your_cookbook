import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    username: null,
    role: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin',
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
      this.role = null
      localStorage.removeItem('token')
    },

    init() {
      if (this.token) {
        this.fetchMe().catch(() => {})
      }
    },

    async fetchMe() {
      const res = await api.get('/auth/me')
      this.username = res.data?.username ?? null
      this.role = res.data?.role ?? null
      this.user = res.data ?? null
      return res.data
    },

    setUsername(name) {
      this.username = name
    },

    async signInWithGoogle() {
      window.location.href = '/auth/google'
    },
  },
})
