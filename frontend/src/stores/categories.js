import { defineStore } from 'pinia'
import api from '../api'

const API_URL = '/categories/'

export const useCategoryStore = defineStore('categories', {
  state: () => ({
    categories: [],
    loading: false,
  }),
  
  actions: {
    async fetchCategories() {
      this.loading = true
      try {
        const res = await api.get(API_URL)
        this.categories = res.data
        return res.data
      } finally {
        this.loading = false
      }
    },
    
    async createCategory(data) {
      const res = await api.post(API_URL, data)
      this.categories.push(res.data)
      return res.data
    },
    
    async updateCategory(id, data) {
      const res = await api.put(`${API_URL}/${id}`, data)
      const index = this.categories.findIndex(c => c.id === id)
      if (index !== -1) {
        this.categories[index] = res.data
      }
      return res.data
    },
    
    async deleteCategory(id) {
      await api.delete(`${API_URL}/${id}`)
      this.categories = this.categories.filter(c => c.id !== id)
    },
  },
})
