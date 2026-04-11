<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Мои рецепты</h1>
      <router-link
        to="/recipes/new"
        class="px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition"
      >
        + Добавить рецепт
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
        class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition"
      >
        <h3 class="text-xl font-bold text-gray-800 mb-2">{{ recipe.title }}</h3>
        <p class="text-gray-600 mb-4 line-clamp-2">{{ recipe.description || 'Нет описания' }}</p>
        <div class="text-sm text-gray-500 mb-4">
          <span class="font-medium">Ингредиенты:</span> {{ recipe.ingredients }}
        </div>
        <div class="flex space-x-3">
          <router-link
            :to="`/recipes/${recipe.id}/edit`"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
          >
            Редактировать
          </router-link>
          <button
            @click="deleteRecipe(recipe.id)"
            class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
    
    <!-- Пагинация -->
    <div v-if="totalPages > 1" class="flex justify-center space-x-2 mt-10">
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
import { computed, onMounted } from 'vue'
import { useRecipeStore } from '../stores/recipes'

const recipeStore = useRecipeStore()

const recipes = computed(() => recipeStore.recipes)
const loading = computed(() => recipeStore.loading)
const pagination = computed(() => recipeStore.pagination)
const currentPage = computed(() => pagination.value.page)
const totalPages = computed(() => pagination.value.totalPages)

onMounted(() => {
  recipeStore.fetchRecipes()
})

async function deleteRecipe(id) {
  if (confirm('Удалить рецепт?')) {
    await recipeStore.deleteRecipe(id)
    await recipeStore.fetchRecipes(currentPage.value)
  }
}

function changePage(page) {
  recipeStore.fetchRecipes(page)
}
</script>
