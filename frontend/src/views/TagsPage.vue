<template>
  <div class="min-h-screen p-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Ваши теги</h1>
        <p class="text-gray-600 mt-2">
          Всего тегов: {{ tags.length }}
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-8">
        <p class="text-gray-500">Загрузка...</p>
      </div>

      <!-- No tags -->
      <div v-else-if="tags.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
        <p class="text-gray-500 mb-4">У вас ещё нет тегов. Добавьте теги к своим рецептам.</p>
        <router-link to="/recipes" class="text-orange-500 hover:text-orange-600 font-medium">
          Перейти к рецептам →
        </router-link>
      </div>

      <!-- Tags grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        <router-link 
          v-for="tag in tags" 
          :key="tag.name"
          :to="`/tags/${encodeURIComponent(tag.name)}`"
          class="flex flex-col items-center justify-center p-6 bg-white rounded-xl border border-gray-200 hover:border-orange-400 hover:shadow-md transition"
        >
          <div class="flex items-center gap-2 mb-2">
            <svg class="h-5 w-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <span class="text-lg font-semibold text-gray-800">{{ tag.name }}</span>
          </div>
          <div class="bg-orange-100 text-orange-800 text-sm font-semibold px-3 py-1 rounded-full">
            {{ tag.count }} рецепта
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const tags = ref([])
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/recipes/tags')
    tags.value = res.data || []
  } catch (error) {
    console.error('Ошибка загрузки тегов:', error)
    tags.value = []
  } finally {
    loading.value = false
  }
})
</script>
