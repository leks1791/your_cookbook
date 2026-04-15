<template>
  <div v-if="recipe" class="max-w-4xl mx-auto p-6 space-y-6">
    <div class="flex items-start justify-between gap-4">
      <div>
        <div class="flex gap-2 mb-3">
          <span
            class="px-2.5 py-1 rounded-full text-xs font-semibold"
            :class="recipe.is_admin_recipe ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'"
          >
            {{ recipe.is_admin_recipe ? 'Рецепт от админа' : 'Рецепт сообщества' }}
          </span>
        </div>
        <h1 class="text-3xl font-bold text-stone-800">{{ recipe.title }}</h1>
        <p v-if="recipe.description" class="mt-3 text-stone-600">{{ recipe.description }}</p>
      </div>

      <button
        v-if="auth.isAuthenticated"
        class="px-5 py-2.5 rounded-xl bg-orange-500 text-white font-medium hover:bg-orange-600 transition"
        @click="cloneRecipe"
      >
        Добавить в мою книгу
      </button>
    </div>

    <div class="grid sm:grid-cols-3 gap-4 text-sm text-stone-600">
      <div class="bg-white border border-stone-200 rounded-2xl p-4">Подготовка: {{ recipe.prep_time || 0 }} мин</div>
      <div class="bg-white border border-stone-200 rounded-2xl p-4">Готовка: {{ recipe.cook_time || 0 }} мин</div>
      <div class="bg-white border border-stone-200 rounded-2xl p-4">Порций: {{ recipe.servings || 0 }}</div>
    </div>

    <div class="bg-white border border-stone-200 rounded-2xl p-6">
      <h2 class="text-xl font-bold text-stone-800 mb-4">Ингредиенты</h2>
      <pre class="whitespace-pre-wrap text-stone-700">{{ recipe.ingredients }}</pre>
    </div>

    <div v-if="recipe.steps" class="bg-white border border-stone-200 rounded-2xl p-6">
      <h2 class="text-xl font-bold text-stone-800 mb-4">Шаги</h2>
      <pre class="whitespace-pre-wrap text-stone-700">{{ recipe.steps }}</pre>
    </div>
  </div>
  <div v-else class="max-w-4xl mx-auto p-6 text-stone-500">Загрузка рецепта...</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCatalogStore } from '../stores/catalog'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const catalogStore = useCatalogStore()
const recipe = ref(null)

async function loadRecipe() {
  recipe.value = await catalogStore.fetchRecipe(route.params.id)
}

async function cloneRecipe() {
  const created = await catalogStore.cloneRecipe(route.params.id)
  router.push(`/recipes/${created.id}`)
}

onMounted(() => {
  loadRecipe()
})
</script>
