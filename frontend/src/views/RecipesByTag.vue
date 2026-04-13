<template>
  <div class="min-h-screen p-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/tags" class="text-orange-500 hover:text-orange-600 mb-4 inline-flex items-center">
          <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Назад к тегам
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">
          <span v-if="tagInfo">{{ tagInfo }}</span>
          <span v-else>Загрузка...</span>
        </h1>
        <p class="text-gray-600 mt-2">
          Найдено рецептов: {{ recipes.total }}
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-8">
        <p class="text-gray-500">Загрузка...</p>
      </div>

      <!-- No recipes -->
      <div v-else-if="recipes.items.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
        <p class="text-gray-500 mb-4">Рецептов с этим тегом не найдено</p>
        <router-link to="/recipes/new" class="text-orange-500 hover:text-orange-600 font-medium">
          Добавить рецепт →
        </router-link>
      </div>

      <!-- Recipes grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div 
          v-for="recipe in recipes.items" 
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

      <!-- Pagination -->
      <div v-if="recipes.total_pages > 1" class="flex justify-center gap-2">
        <button
          v-for="page in recipes.total_pages"
          :key="page"
          @click="loadPage(page)"
          :class="page === recipes.page ? 'bg-orange-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
          class="px-4 py-2 rounded-lg font-medium transition"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const tagName = route.params.tag
const recipes = ref({
  items: [],
  total: 0,
  page: 1,
  page_size: 12,
  total_pages: 1
})
const tagInfo = ref(tagName)
const loading = ref(true)
const activeMenuId = ref(null)

async function loadPage(page = 1) {
  loading.value = true
  try {
    const res = await api.get(`/recipes/tag/${encodeURIComponent(tagName)}`, {
      params: { page, page_size: 12 }
    })
    recipes.value = res.data
  } catch (error) {
    console.error('Ошибка загрузки рецептов:', error)
    recipes.value.items = []
  } finally {
    loading.value = false
  }
}

function toggleMenu(id) {
  activeMenuId.value = activeMenuId.value === id ? null : id
}

async function deleteRecipe(id) {
  activeMenuId.value = null
  if (confirm('Удалить рецепт?')) {
    try {
      await api.delete(`/recipes/${id}`)
      await loadPage(recipes.value.page)
    } catch (error) {
      console.error('Ошибка удаления:', error)
    }
  }
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

onMounted(() => {
  loadPage(1)
})
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
