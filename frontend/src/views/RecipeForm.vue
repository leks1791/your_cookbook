<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
      <h2 class="text-2xl font-bold mb-6 text-gray-800">
        {{ isEdit ? 'Редактировать рецепт' : 'Новый рецепт' }}
      </h2>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div class="md:col-span-2">
            <label class="block text-gray-700 mb-2 font-medium">Название *</label>
            <input
              v-model="form.title"
              type="text"
              required
              placeholder="Например: Домашняя паста карбонара"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2 font-medium">Описание</label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Краткое описание блюда..."
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
          ></textarea>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-gray-700 mb-2 font-medium">Время подготовки (мин)</label>
            <input
              v-model.number="form.prep_time"
              type="number"
              min="0"
              placeholder="15"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-gray-700 mb-2 font-medium">Время приготовления (мин)</label>
            <input
              v-model.number="form.cook_time"
              type="number"
              min="0"
              placeholder="30"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="block text-gray-700 mb-2 font-medium">Порции</label>
            <input
              v-model.number="form.servings"
              type="number"
              min="1"
              placeholder="4"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-gray-700 mb-2 font-medium">Сложность</label>
            <select
              v-model="form.difficulty"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="">Выберите</option>
              <option value="easy">Легко</option>
              <option value="medium">Средне</option>
              <option value="hard">Сложно</option>
            </select>
          </div>
          <div>
            <label class="block text-gray-700 mb-2 font-medium">Кухня</label>
            <input
              v-model="form.cuisine"
              type="text"
              placeholder="Итальянская, Японская..."
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
        </div>

        <RecipeCategoriesForm v-model="form.category_ids" />
        
        <RecipeTagsForm v-model="form.tags" />
        
        <RecipeIngredientsForm v-model="form.ingredients" />
        
        <RecipeStepsForm v-model="form.steps" />
        
        <RecipePhotosForm v-model="form.photos" />
        
        <div class="mb-6">
          <label class="block text-gray-700 mb-2 font-medium">Заметки</label>
          <textarea
            v-model="form.notes"
            rows="3"
            placeholder="Дополнительные заметки, советы по подаче..."
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
          ></textarea>
        </div>
        
        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="loading"
            class="px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition disabled:opacity-50"
          >
            {{ loading ? 'Сохранение...' : 'Сохранить рецепт' }}
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
import RecipeTagsForm from '../components/RecipeTagsForm.vue'
import RecipeIngredientsForm from '../components/RecipeIngredientsForm.vue'
import RecipeStepsForm from '../components/RecipeStepsForm.vue'
import RecipePhotosForm from '../components/RecipePhotosForm.vue'
import RecipeCategoriesForm from '../components/RecipeCategoriesForm.vue'

const route = useRoute()
const router = useRouter()
const recipeStore = useRecipeStore()

const isEdit = computed(() => !!route.params.id)
const recipeId = computed(() => route.params.id)

const form = reactive({
  title: '',
  description: '',
  ingredients: JSON.stringify([{ amount: '', unit: '', name: '' }]),
  steps: JSON.stringify([{ order: 0, description: '', timer_seconds: null }]),
  tags: [],
  photos: [],
  prep_time: null,
  cook_time: null,
  servings: null,
  difficulty: '',
  cuisine: '',
  notes: '',
  category_ids: [],
})

const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (isEdit.value) {
    try {
      const recipe = await recipeStore.fetchRecipe(recipeId.value)
      // Используем Object.assign для предотвращения реактивных циклов
      Object.assign(form, {
        title: recipe.title,
        description: recipe.description || '',
        ingredients: recipe.ingredients,
        steps: recipe.steps || JSON.stringify([]),
        tags: recipe.tags || [],
        photos: recipe.photos || [],
        prep_time: recipe.prep_time,
        cook_time: recipe.cook_time,
        servings: recipe.servings,
        difficulty: recipe.difficulty || '',
        cuisine: recipe.cuisine || '',
        notes: recipe.notes || '',
        category_ids: recipe.categories ? recipe.categories.map(c => c.id) : [],
      })
    } catch (e) {
      error.value = 'Рецепт не найден'
    }
  }
})

async function handleSubmit() {
  loading.value = true
  error.value = ''
  
  try {
    // Валидация title
    if (!form.title || form.title.trim() === '') {
      error.value = 'Название рецепта обязательно'
      loading.value = false
      return
    }
    
    const payload = {
      title: form.title.trim(),
      description: form.description,
      ingredients: form.ingredients,
      steps: form.steps,
      tags: form.tags,
      photos: form.photos,
      prep_time: form.prep_time,
      cook_time: form.cook_time,
      servings: form.servings,
      difficulty: form.difficulty || null,
      cuisine: form.cuisine || null,
      notes: form.notes,
      category_ids: form.category_ids || [],
    }
    
    console.log('Sending payload:', payload)
    
    if (isEdit.value) {
      await recipeStore.updateRecipe(recipeId.value, payload)
    } else {
      await recipeStore.createRecipe(payload)
    }
    router.push('/recipes')
  } catch (e) {
    console.error('Save error:', e)
    error.value = e.response?.data?.detail || e.message || 'Ошибка сохранения'
  } finally {
    loading.value = false
  }
}
</script>
