<template>
  <div v-if="recipe" class="p-4">
    <h2 class="text-2xl font-bold mb-2">{{ recipe.title }}</h2>
    <p class="mb-4" v-if="recipe.description">{{ recipe.description }}</p>
    <div class="prose" v-html="recipe.ingredients"></div>
  </div>
  <div v-else class="p-4 text-gray-500">Загрузка рецепта...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const id = route.params.id
const recipe = ref(null)

onMounted(async () => {
  try {
    const res = await api.get(`/recipes/${id}`)
    recipe.value = res.data
  } catch {
    recipe.value = null
  }
})
</script>
