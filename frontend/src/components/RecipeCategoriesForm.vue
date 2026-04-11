<template>
  <div class="mb-6">
    <label class="block text-gray-700 mb-3 font-medium">Категории</label>
    
    <div v-if="loading" class="text-gray-500 text-sm">Загрузка категорий...</div>
    
    <div v-else-if="categories.length === 0" class="text-gray-400 text-sm italic mb-3">
      Категорий нет. 
      <router-link to="/categories" class="text-orange-500 hover:underline">Создать категорию</router-link>
    </div>
    
    <div v-else class="space-y-3">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <label
          v-for="category in categories"
          :key="category.id"
          class="relative flex items-center p-3 border-2 rounded-xl cursor-pointer transition hover:shadow-sm"
          :class="isSelected(category.id) ? 'border-orange-500 bg-orange-50' : 'border-gray-200 bg-white'"
        >
          <input
            type="checkbox"
            :value="category.id"
            :checked="isSelected(category.id)"
            @change="toggleCategory(category.id)"
            class="hidden"
          />
          
          <div
            class="w-4 h-4 rounded-full mr-3 flex-shrink-0"
            :style="{ backgroundColor: category.color }"
          ></div>
          
          <span class="flex-1 text-sm font-medium text-gray-700">{{ category.name }}</span>
          
          <svg
            v-if="isSelected(category.id)"
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 text-orange-500"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </label>
      </div>
      
      <div v-if="selectedCategories.length > 0" class="mt-3">
        <p class="text-xs text-gray-500 mb-2">Выбрано категорий: {{ selectedCategories.length }}</p>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="cat in selectedCategories"
            :key="cat.id"
            class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm"
            :style="{ backgroundColor: cat.color + '20', color: cat.color }"
          >
            {{ cat.name }}
            <button
              type="button"
              @click="toggleCategory(cat.id)"
              class="hover:opacity-70"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCategoryStore } from '../stores/categories'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const categoryStore = useCategoryStore()
const categories = ref([])
const loading = ref(true)

// Используем map для получения выбранных категорий вместо filter
const selectedCategories = computed(() => {
  if (!props.modelValue || !Array.isArray(props.modelValue)) return []
  return categoryStore.categories
    .filter(cat => props.modelValue.includes(cat.id))
})

onMounted(async () => {
  try {
    await categoryStore.fetchCategories()
    categories.value = [...categoryStore.categories]
  } catch (e) {
    console.error('Failed to load categories:', e)
  } finally {
    loading.value = false
  }
})

function isSelected(categoryId) {
  if (!props.modelValue || !Array.isArray(props.modelValue)) return false
  return props.modelValue.includes(categoryId)
}

function toggleCategory(categoryId) {
  if (!props.modelValue || !Array.isArray(props.modelValue)) {
    emit('update:modelValue', [categoryId])
    return
  }
  
  const current = [...props.modelValue]
  const index = current.indexOf(categoryId)
  
  if (index === -1) {
    current.push(categoryId)
  } else {
    current.splice(index, 1)
  }
  
  emit('update:modelValue', current)
}
</script>
