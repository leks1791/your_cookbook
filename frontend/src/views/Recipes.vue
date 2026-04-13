<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Мои рецепты</h1>
      <router-link
        to="/recipes/new"
        class="px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition flex items-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Добавить рецепт
      </router-link>
    </div>
    
    <div v-if="loading" class="text-center py-16 text-gray-500">Загрузка...</div>
    
    <div v-else-if="recipes.length === 0" class="text-center py-16 bg-white rounded-2xl shadow-sm">
      <div class="text-6xl mb-4">📖</div>
      <p class="text-xl text-gray-600 mb-4">У вас пока нет рецептов</p>
      <router-link
        to="/recipes/new"
        class="inline-block px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition"
      >
        Добавить первый рецепт
      </router-link>
    </div>
    
    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="recipe in recipes"
        :key="recipe.id"
        class="bg-white rounded-2xl shadow-sm border border-gray-200 hover:shadow-lg transition cursor-pointer group relative"
        @click="$router.push(`/recipes/${recipe.id}`)"
      >
        <!-- Карточка рецепта -->
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-800 mb-2 group-hover:text-orange-500 transition">{{ recipe.title }}</h3>
          <p class="text-gray-600 mb-4 line-clamp-2 text-sm">{{ recipe.description || 'Нет описания' }}</p>
          
          <!-- Теги -->
          <div v-if="recipe.tags && recipe.tags.length" class="flex flex-wrap gap-1 mb-4">
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
          
          <!-- Мета информация -->
          <div class="flex items-center gap-4 text-xs text-gray-500 mb-4">
            <div v-if="recipe.prep_time" class="flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              <span>{{ recipe.prep_time }} мин</span>
            </div>
            <div v-if="recipe.servings" class="flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
              </svg>
              <span>{{ recipe.servings }} порц.</span>
            </div>
          </div>
          
          <div class="text-xs text-gray-400">
            {{ formatDate(recipe.created_at) }}
          </div>
        </div>
        
        <!-- Меню действий -->
        <div class="absolute top-4 right-4">
          <div class="relative" @click.stop>
            <button
              @click="toggleMenu(recipe.id)"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition"
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
    
    <!-- Пагинация -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-10">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="changePage(page)"
        :class="[
          'px-4 py-2 rounded-lg transition',
          page === currentPage
            ? 'bg-orange-500 text-white'
            : 'bg-white text-gray-700 hover:bg-orange-50 border border-orange-100'
        ]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRecipeStore } from '../stores/recipes'

const recipeStore = useRecipeStore()

const recipes = computed(() => recipeStore.recipes)
const loading = computed(() => recipeStore.loading)
const pagination = computed(() => recipeStore.pagination)
const currentPage = computed(() => pagination.value.page)
const totalPages = computed(() => pagination.value.totalPages)
const activeMenuId = ref(null)

onMounted(() => {
  recipeStore.fetchRecipes()
})

async function deleteRecipe(id) {
  activeMenuId.value = null
  if (confirm('Удалить рецепт?')) {
    await recipeStore.deleteRecipe(id)
    await recipeStore.fetchRecipes(currentPage.value)
  }
}

function changePage(page) {
  recipeStore.fetchRecipes(page)
}

function toggleMenu(id) {
  activeMenuId.value = activeMenuId.value === id ? null : id
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
