<template>
  <div class="min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Добро пожаловать в твою кулинарную книгу!</h1>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-orange-100 rounded-md p-3">
              <svg class="h-6 w-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Всего рецептов</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalRecipes }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-blue-100 rounded-md p-3">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Категории</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalCategories }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Создано за неделю</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.weeklyRecipes }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Быстрые действия</h2>
        <div class="flex flex-wrap gap-4">
          <router-link 
            to="/recipes/new" 
            class="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Добавить рецепт
          </router-link>
          <router-link 
            to="/categories" 
            class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
            </svg>
            Управлять категориями
          </router-link>
          <router-link 
            to="/recipes" 
            class="bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
            </svg>
            Все рецепты
          </router-link>
        </div>
      </div>

      <!-- Categories on Dashboard -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Ваши категории</h2>
        <div v-if="categories.length === 0" class="p-4 text-gray-500">У вас ещё нет категорий. Вы можете создать первую категорию в разделе Категории.</div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          <div v-for="cat in categories" :key="cat.id" class="flex items-center justify-between gap-3 p-4 rounded-xl border border-gray-200 bg-white">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-full" :style="{ backgroundColor: cat.color }"></span>
              <span class="text-lg font-medium text-gray-700">{{ cat.name }}</span>
            </div>
            <span class="text-lg font-semibold text-gray-700">{{ cat.recipe_count ?? 0 }}</span>
          </div>
        </div>
      </section>

      <!-- Recent Recipes -->
      <div>
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">Последние рецепты</h2>
          <router-link to="/recipes" class="text-orange-500 hover:text-orange-600">Все рецепты →</router-link>
        </div>
        
        <div v-if="loading" class="text-center py-8">
          <p class="text-gray-500">Загрузка...</p>
        </div>
        
        <div v-else-if="recentRecipes.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
          <p class="text-gray-500 mb-4">У вас ещё нет рецептов</p>
          <router-link to="/recipes/new" class="text-orange-500 hover:text-orange-600 font-medium">
            Создать первый рецепт →
          </router-link>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="recipe in recentRecipes" 
            :key="recipe.id" 
            class="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer"
            @click="$router.push(`/recipes/${recipe.id}`)"
          >
            <div class="p-4">
              <h3 class="font-semibold text-gray-900 mb-2">{{ recipe.title }}</h3>
              <p class="text-sm text-gray-600 line-clamp-2">{{ recipe.description }}</p>
              <div class="mt-4 flex items-center justify-between">
                <span class="text-xs text-gray-500">
                  {{ formatDate(recipe.created_at) }}
                </span>
                <router-link 
                  :to="`/recipes/${recipe.id}/edit`"
                  class="text-orange-500 hover:text-orange-600 text-sm"
                  @click.stop
                >
                  Редактировать
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import api from '../api'

export default {
  name: 'Dashboard',
  setup() {
    const auth = useAuthStore()
    return { auth }
  },
  data() {
    return {
      recentRecipes: [],
      categories: [],
      stats: {
        totalRecipes: 0,
        totalCategories: 0,
        weeklyRecipes: 0
      },
      loading: true
    }
  },
  async mounted() {
    await this.loadDashboard()
    if (this.auth?.isAuthenticated) {
      await this.loadCategories()
    }
    // Fallback: retry once after a short delay in case auth state propagates a bit later
    if (this.auth?.isAuthenticated) {
      setTimeout(() => this.loadCategories(), 500)
    }
    window.addEventListener('category_updated', this.loadCategories)
  },
  methods: {
    async loadDashboard() {
      try {
        this.loading = true
        const [recipesRes, statsRes] = await Promise.all([
          api.get('/recipes/', { params: { page: 1, page_size: 6 } }),
          api.get('/recipes/stats')
        ])
        
        this.recentRecipes = recipesRes.data.items || recipesRes.data || []
        this.stats = statsRes.data
      } catch (error) {
        console.error('Ошибка загрузки дашборда:', error)
      } finally {
        this.loading = false
      }
    },
  beforeUnmount() {
      window.removeEventListener('category_updated', this.loadCategories)
    },
    async loadCategories() {
      try {
        const res = await api.get('/categories')
        const data = res.data ?? []
        if (Array.isArray(data)) {
          this.categories = data
        } else if (data?.items) {
          this.categories = data.items
        } else {
          this.categories = data
        }
      } catch (e) {
        console.error('Ошибка загрузки категорий на дашборде:', e)
        this.categories = []
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
