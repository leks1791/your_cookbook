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
              <p class="text-sm font-medium text-gray-500">Теги</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalTags }}</p>
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
            to="/tags" 
            class="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
            </svg>
            Все теги
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

      <!-- Tags on Dashboard -->
      <section class="mb-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">Ваши теги</h2>
          <router-link to="/tags" class="text-orange-500 hover:text-orange-600 text-sm">Все теги →</router-link>
        </div>
        <div v-if="tags.length === 0" class="p-4 text-gray-500">У вас ещё нет тегов. Добавьте теги к своим рецептам.</div>
        <div v-else class="flex flex-wrap gap-3">
          <router-link 
            v-for="tag in tags" 
            :key="tag.name"
            :to="`/tags/${encodeURIComponent(tag.name)}`"
            class="flex items-center gap-2 px-4 py-2 bg-orange-50 hover:bg-orange-100 text-orange-700 rounded-full transition border border-orange-200"
          >
            <span class="font-medium">{{ tag.name }}</span>
            <span class="bg-orange-200 text-orange-800 text-xs font-semibold px-2 py-0.5 rounded-full">
              {{ tag.count }}
            </span>
          </router-link>
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
            class="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer group relative"
            @click="$router.push(`/recipes/${recipe.id}`)"
          >
            <div class="p-4">
              <h3 class="font-semibold text-gray-900 mb-2 group-hover:text-orange-500 transition">{{ recipe.title }}</h3>
              <p class="text-sm text-gray-600 line-clamp-2 mb-3">{{ recipe.description }}</p>
              
              <!-- Теги -->
              <div v-if="recipe.tags && recipe.tags.length" class="flex flex-wrap gap-1 mb-3">
                <span 
                  v-for="tag in recipe.tags.slice(0, 3)" 
                  :key="tag"
                  class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full text-xs font-medium"
                >
                  {{ tag }}
                </span>
                <span v-if="recipe.tags.length > 3" class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full text-xs">
                  +{{ recipe.tags.length - 3 }}
                </span>
              </div>
              
              <div class="text-xs text-gray-400">
                {{ formatDate(recipe.created_at) }}
              </div>
            </div>
            
            <!-- Меню действий -->
            <div class="absolute top-2 right-2">
              <div class="relative" @click.stop>
                <button
                  @click="toggleMenu(recipe.id)"
                  class="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                  </svg>
                </button>
                
                <!-- Выпадающее меню -->
                <div 
                  v-if="activeMenuId === recipe.id"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 z-10"
                >
                  <router-link
                    :to="`/recipes/${recipe.id}/edit`"
                    class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 hover:text-orange-600 transition"
                    @click.stop
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                    Редактировать
                  </router-link>
                  <button
                    @click="deleteRecipe(recipe.id)"
                    class="flex items-center gap-2 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                    Удалить
                  </button>
                </div>
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
import { ref } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const auth = useAuthStore()
    const activeMenuId = ref(null)
    
    function toggleMenu(id) {
      activeMenuId.value = activeMenuId.value === id ? null : id
    }
    
    async function deleteRecipe(id) {
      activeMenuId.value = null
      if (confirm('Удалить рецепт?')) {
        try {
          await api.delete(`/recipes/${id}`)
          await this.loadDashboard()
        } catch (error) {
          console.error('Ошибка удаления:', error)
        }
      }
    }
    
    return { auth, activeMenuId, toggleMenu, deleteRecipe }
  },
  data() {
    return {
      recentRecipes: [],
      tags: [],
      stats: {
        totalRecipes: 0,
        totalTags: 0,
        weeklyRecipes: 0
      },
      loading: true
    }
  },
  async mounted() {
    await this.loadDashboard()
    if (this.auth?.isAuthenticated) {
      await this.loadTags()
    }
    // Fallback: retry once after a short delay in case auth state propagates a bit later
    if (this.auth?.isAuthenticated) {
      setTimeout(() => this.loadTags(), 500)
    }
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
    async loadTags() {
      try {
        const res = await api.get('/recipes/tags')
        const data = res.data ?? []
        if (Array.isArray(data)) {
          this.tags = data
        } else if (data?.items) {
          this.tags = data.items
        } else {
          this.tags = data
        }
      } catch (e) {
        console.error('Ошибка загрузки тегов на дашборде:', e)
        this.tags = []
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
