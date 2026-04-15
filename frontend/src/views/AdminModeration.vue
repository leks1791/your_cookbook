<template>
  <div class="max-w-6xl mx-auto p-6 space-y-6">
    <div>
      <h1 class="text-3xl font-bold text-stone-800">Модерация рецептов</h1>
      <p class="text-stone-500 mt-2">Очередь рецептов, ожидающих одобрения.</p>
    </div>

    <div v-if="loading" class="py-12 text-center text-stone-500">Загрузка очереди...</div>

    <div v-else-if="recipes.length === 0" class="bg-white border border-stone-200 rounded-2xl p-10 text-center text-stone-500">
      На модерации сейчас ничего нет.
    </div>

    <div v-else class="space-y-4">
      <article
        v-for="recipe in recipes"
        :key="recipe.id"
        class="bg-white border border-stone-200 rounded-2xl p-6 space-y-4"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold text-stone-800">{{ recipe.title }}</h2>
            <p class="text-stone-600 mt-2">{{ recipe.description || 'Без описания' }}</p>
            <p class="text-xs text-stone-500 mt-3">Автор ID: {{ recipe.user_id }}</p>
          </div>
          <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-700">
            На модерации
          </span>
        </div>

        <div class="flex flex-wrap gap-3">
          <button
            class="px-4 py-2 rounded-xl bg-green-600 text-white font-medium hover:bg-green-700 transition"
            @click="approveRecipe(recipe.id)"
          >
            Одобрить
          </button>
          <button
            class="px-4 py-2 rounded-xl bg-red-600 text-white font-medium hover:bg-red-700 transition"
            @click="rejectRecipe(recipe.id)"
          >
            Отклонить
          </button>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../api'

const recipes = ref([])
const loading = ref(true)

async function loadPendingRecipes() {
  loading.value = true
  try {
    const res = await api.get('/admin/recipes/pending')
    recipes.value = res.data
  } finally {
    loading.value = false
  }
}

async function approveRecipe(id) {
  await api.post(`/admin/recipes/${id}/approve`)
  await loadPendingRecipes()
}

async function rejectRecipe(id) {
  const reason = window.prompt('Причина отклонения', 'Нужно доработать рецепт')
  if (!reason) return
  await api.post(`/admin/recipes/${id}/reject`, { reason })
  await loadPendingRecipes()
}

onMounted(() => {
  loadPendingRecipes()
})
</script>
