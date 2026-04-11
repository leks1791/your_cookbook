import { defineStore } from 'pinia'
import api from '../api'

const API_URL = '/recipes/'

export const useRecipeStore = defineStore('recipes', {
  state: () => ({
    recipes: [],
    currentRecipe: null,
    loading: false,
    pagination: {
      page: 1,
      pageSize: 10,
      total: 0,
      totalPages: 0,
    },
  }),
  
  actions: {
    async fetchRecipes(page = 1, pageSize = 10) {
      this.loading = true
      try {
        const res = await api.get(API_URL, {
          params: { page, page_size: pageSize },
        })
        this.recipes = res.data.items
        this.pagination = {
          page: res.data.page,
          pageSize: res.data.page_size,
          total: res.data.total,
          totalPages: res.data.total_pages,
        }
      } finally {
        this.loading = false
      }
    },
    
    async fetchRecipe(id) {
      this.loading = true
      try {
        const res = await api.get(`${API_URL}/${id}`)
        this.currentRecipe = res.data
        return res.data
      } finally {
        this.loading = false
      }
    },
    
    async createRecipe(data) {
      const res = await api.post(API_URL, data)
      return res.data
    },
    
    async updateRecipe(id, data) {
      const res = await api.put(`${API_URL}/${id}`, data)
      return res.data
    },
    
    async deleteRecipe(id) {
      await api.delete(`${API_URL}/${id}`)
    },
  },
})