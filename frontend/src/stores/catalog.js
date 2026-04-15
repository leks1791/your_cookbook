import { defineStore } from 'pinia'
import api from '../api'

export const useCatalogStore = defineStore('catalog', {
  state: () => ({
    recipes: [],
    currentRecipe: null,
    loading: false,
    home: {
      admin: [],
      community: [],
    },
    pagination: {
      page: 1,
      pageSize: 10,
      total: 0,
      totalPages: 0,
    },
  }),

  actions: {
    async fetchCatalog(page = 1, pageSize = 12, source = null) {
      this.loading = true
      try {
        const params = { page, page_size: pageSize }
        if (source) params.source = source
        const res = await api.get('/catalog', { params })
        this.recipes = res.data.items
        this.pagination = {
          page: res.data.page,
          pageSize: res.data.page_size,
          total: res.data.total,
          totalPages: res.data.total_pages,
        }
        return res.data
      } finally {
        this.loading = false
      }
    },

    async fetchRecipe(id) {
      this.loading = true
      try {
        const res = await api.get(`/catalog/${id}`)
        this.currentRecipe = res.data
        return res.data
      } finally {
        this.loading = false
      }
    },

    async cloneRecipe(id) {
      const res = await api.post(`/catalog/${id}/clone`)
      return res.data
    },

    async fetchHomeCatalog() {
      const [adminRes, communityRes] = await Promise.all([
        api.get('/catalog', { params: { page: 1, page_size: 4, source: 'admin' } }),
        api.get('/catalog', { params: { page: 1, page_size: 4, source: 'community' } }),
      ])

      this.home = {
        admin: adminRes.data.items,
        community: communityRes.data.items,
      }

      return this.home
    },
  },
})
