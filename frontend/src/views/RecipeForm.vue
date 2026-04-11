<template>
  <div class="max-w-2xl mx-auto p-6">
    <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
      <h2 class="text-2xl font-bold mb-6 text-gray-800">
        {{ isEdit ? 'Редактировать рецепт' : 'Новый рецепт' }}
      </h2>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2 font-medium">Название</label>
          <input
            v-model="form.title"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2 font-medium">Описание</label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
          ></textarea>
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 mb-2 font-medium">Ингредиенты</label>
          <textarea
            v-model="form.ingredients"
            required
            rows="4"
            placeholder="Перечислите ингредиенты через запятую"
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
          ></textarea>
        </div>
        
        <div class="flex space-x-4">
          <button
            type="submit"
            :disabled="loading"
            class="px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition disabled:opacity-50"
          >
            {{ loading ? 'Сохранение...' : 'Сохранить' }}
          </button>
          <router-link
            to="/recipes"
            class="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-medium hover:bg-gray-200 transition"
          >
            Отмена
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRecipeStore } from '../stores/recipes'

const route = useRoute()
const router = useRouter()
const recipeStore = useRecipeStore()

const isEdit = computed(() => !!route.params.id)
const recipeId = computed(() => route.params.id)

const form = reactive({
  title: '',
  description: '',
  ingredients: '',
})

const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (isEdit.value) {
    try {
      const recipe = await recipeStore.fetchRecipe(recipeId.value)
      form.title = recipe.title
      form.description = recipe.description || ''
      form.ingredients = recipe.ingredients
    } catch (e) {
      error.value = 'Рецепт не найден'
    }
  }
})

async function handleSubmit() {
  loading.value = true
  error.value = ''
  
  try {
    if (isEdit.value) {
      await recipeStore.updateRecipe(recipeId.value, form)
    } else {
      await recipeStore.createRecipe(form)
    }
    router.push('/recipes')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка сохранения'
  } finally {
    loading.value = false
  }
}
</script>
