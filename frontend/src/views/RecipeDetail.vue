<template>
  <div v-if="recipe" class="p-4 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-2 text-gray-800">{{ recipe.title }}</h2>
    <p class="mb-4 text-gray-600" v-if="recipe.description">{{ recipe.description }}</p>
    
    <!-- Мета информация -->
    <div class="flex flex-wrap gap-4 mb-6 text-sm text-gray-600">
      <div v-if="recipe.prep_time" class="flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
        </svg>
        <span>Подготовка: {{ recipe.prep_time }} мин</span>
      </div>
      <div v-if="recipe.cook_time" class="flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
        </svg>
        <span>Приготовление: {{ recipe.cook_time }} мин</span>
      </div>
      <div v-if="recipe.servings" class="flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
        </svg>
        <span>{{ recipe.servings }} порции</span>
      </div>
      <div v-if="recipe.difficulty" class="flex items-center gap-1">
        <span class="font-medium">Сложность:</span>
        <span :class="difficultyColor">{{ difficultyLabel }}</span>
      </div>
    </div>

    <!-- Теги -->
    <div v-if="recipe.tags && recipe.tags.length" class="flex flex-wrap gap-2 mb-6">
      <span 
        v-for="tag in recipe.tags" 
        :key="tag"
        class="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium"
      >
        {{ tag }}
      </span>
    </div>

    <!-- Ингредиенты -->
    <div class="mb-8">
      <h3 class="text-xl font-bold mb-4 text-gray-800">Ингредиенты</h3>
      <ul class="space-y-2">
        <li 
          v-for="(ingredient, index) in parsedIngredients" 
          :key="index"
          class="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
        >
          <span class="text-orange-500 font-bold w-6 flex-shrink-0">{{ index + 1 }}.</span>
          <span class="text-gray-700">
            <span v-if="ingredient.amount" class="font-semibold">{{ ingredient.amount }} </span>
            <span v-if="ingredient.unit" class="text-gray-500">{{ ingredient.unit }} </span>
            <span class="font-medium">{{ ingredient.name }}</span>
          </span>
        </li>
      </ul>
    </div>

    <!-- Шаги приготовления -->
    <div class="mb-8">
      <h3 class="text-xl font-bold mb-4 text-gray-800">Приготовление</h3>
      <ol class="space-y-4">
        <li 
          v-for="step in parsedSteps" 
          :key="step.order"
          class="flex gap-4"
        >
          <span 
            class="flex-shrink-0 w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold"
          >
            {{ step.order }}
          </span>
          <div class="flex-1">
            <p class="text-gray-700">{{ step.description }}</p>
            <div v-if="step.timer_seconds" class="mt-2 text-sm text-gray-500 flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              Таймер: {{ formatTimer(step.timer_seconds) }}
            </div>
          </div>
        </li>
      </ol>
    </div>

    <!-- Заметки -->
    <div v-if="recipe.notes" class="mb-8 p-4 bg-blue-50 border-l-4 border-blue-400 rounded-lg">
      <h3 class="font-bold mb-2 text-gray-800">Заметки</h3>
      <p class="text-gray-700">{{ recipe.notes }}</p>
    </div>
  </div>
  <div v-else class="p-4 text-gray-500">Загрузка рецепта...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const id = route.params.id
const recipe = ref(null)

const parsedIngredients = computed(() => {
  if (!recipe.value?.ingredients) return []
  try {
    const parsed = typeof recipe.value.ingredients === 'string' 
      ? JSON.parse(recipe.value.ingredients) 
      : recipe.value.ingredients
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
})

const parsedSteps = computed(() => {
  if (!recipe.value?.steps) return []
  try {
    const parsed = typeof recipe.value.steps === 'string'
      ? JSON.parse(recipe.value.steps)
      : recipe.value.steps
    return Array.isArray(parsed) ? parsed.sort((a, b) => a.order - b.order) : []
  } catch {
    return []
  }
})

const difficultyLabel = computed(() => {
  if (!recipe.value?.difficulty) return ''
  const labels = {
    easy: 'Легко',
    medium: 'Средне',
    hard: 'Сложно'
  }
  return labels[recipe.value.difficulty] || recipe.value.difficulty
})

const difficultyColor = computed(() => {
  if (!recipe.value?.difficulty) return ''
  const colors = {
    easy: 'text-green-600',
    medium: 'text-yellow-600',
    hard: 'text-red-600'
  }
  return colors[recipe.value.difficulty] || ''
})

function formatTimer(seconds) {
  if (!seconds) return ''
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  if (minutes > 0) {
    return secs > 0 ? `${minutes} мин ${secs} сек` : `${minutes} мин`
  }
  return `${secs} сек`
}

onMounted(async () => {
  try {
    const res = await api.get(`/recipes/${id}`)
    recipe.value = res.data
  } catch {
    recipe.value = null
  }
})
</script>
