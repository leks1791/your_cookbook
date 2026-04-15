<template>
  <div v-if="recipe" class="p-4 max-w-4xl mx-auto space-y-6">
    <div class="flex items-start justify-between gap-4">
      <div>
        <div class="flex gap-2 mb-3">
          <span class="px-2.5 py-1 rounded-full text-xs font-semibold" :class="statusClass">
            {{ statusLabel }}
          </span>
        </div>
        <h2 class="text-2xl font-bold text-gray-800">{{ recipe.title }}</h2>
        <p class="mt-2 text-gray-600" v-if="recipe.description">{{ recipe.description }}</p>
      </div>

      <button
        v-if="recipe.publication_status !== 'pending_review'"
        class="px-4 py-2 rounded-xl bg-orange-500 text-white font-medium hover:bg-orange-600 transition"
        @click="submitForReview"
      >
        Отправить на модерацию
      </button>
    </div>

    <div v-if="recipe.rejection_reason" class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
      Причина отклонения: {{ recipe.rejection_reason }}
    </div>

    <div class="flex flex-wrap gap-4 text-sm text-gray-600">
      <div v-if="recipe.prep_time">Подготовка: {{ recipe.prep_time }} мин</div>
      <div v-if="recipe.cook_time">Приготовление: {{ recipe.cook_time }} мин</div>
      <div v-if="recipe.servings">Порции: {{ recipe.servings }}</div>
      <div v-if="recipe.difficulty">Сложность: {{ recipe.difficulty }}</div>
    </div>

    <div v-if="recipe.tags && recipe.tags.length" class="flex flex-wrap gap-2">
      <span
        v-for="tag in recipe.tags"
        :key="tag"
        class="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium"
      >
        {{ tag }}
      </span>
    </div>

    <div class="bg-white border border-stone-200 rounded-2xl p-6">
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

    <div v-if="parsedSteps.length" class="bg-white border border-stone-200 rounded-2xl p-6">
      <h3 class="text-xl font-bold mb-4 text-gray-800">Приготовление</h3>
      <ol class="space-y-4">
        <li v-for="step in parsedSteps" :key="step.order" class="flex gap-4">
          <span class="flex-shrink-0 w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold">
            {{ step.order }}
          </span>
          <div class="flex-1">
            <p class="text-gray-700">{{ step.description }}</p>
            <div v-if="step.timer_seconds" class="mt-2 text-sm text-gray-500">
              Таймер: {{ formatTimer(step.timer_seconds) }}
            </div>
          </div>
        </li>
      </ol>
    </div>

    <div v-if="recipe.notes" class="p-4 bg-blue-50 border-l-4 border-blue-400 rounded-lg">
      <h3 class="font-bold mb-2 text-gray-800">Заметки</h3>
      <p class="text-gray-700">{{ recipe.notes }}</p>
    </div>
  </div>
  <div v-else class="p-4 text-gray-500">Загрузка рецепта...</div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useRecipeStore } from '../stores/recipes'

const route = useRoute()
const recipeStore = useRecipeStore()
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

const statusLabel = computed(() => ({
  draft: 'Черновик',
  pending_review: 'На модерации',
  approved: 'Одобрен',
  rejected: 'Отклонён',
}[recipe.value?.publication_status] || recipe.value?.publication_status || 'Статус'))

const statusClass = computed(() => ({
  draft: 'bg-stone-100 text-stone-700',
  pending_review: 'bg-amber-100 text-amber-700',
  approved: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
}[recipe.value?.publication_status] || 'bg-stone-100 text-stone-700'))

function formatTimer(seconds) {
  if (!seconds) return ''
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  if (minutes > 0) {
    return secs > 0 ? `${minutes} мин ${secs} сек` : `${minutes} мин`
  }
  return `${secs} сек`
}

async function loadRecipe() {
  recipe.value = await recipeStore.fetchRecipe(route.params.id)
}

async function submitForReview() {
  await recipeStore.submitForReview(route.params.id)
  await loadRecipe()
}

onMounted(() => {
  loadRecipe()
})
</script>
