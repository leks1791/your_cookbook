<template>
  <div class="mb-6">
    <label class="block text-gray-700 mb-3 font-medium">Ингредиенты</label>
    
    <div class="space-y-3 mb-4">
      <div
        v-for="(ingredient, index) in ingredients"
        :key="index"
        class="flex gap-3 items-center p-3 bg-gray-50 rounded-xl"
      >
        <span class="text-gray-400 font-medium w-6">{{ index + 1 }}</span>
        
        <input
          v-model="ingredient.amount"
          type="text"
          placeholder="Количество"
          class="w-24 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
        />
        
        <input
          v-model="ingredient.unit"
          type="text"
          placeholder="Ед. изм."
          class="w-28 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
        />
        
        <input
          v-model="ingredient.name"
          type="text"
          placeholder="Ингредиент"
          class="flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
        />
        
        <button
          type="button"
          @click="removeIngredient(index)"
          class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition"
          title="Удалить"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    
    <button
      type="button"
      @click="addIngredient"
      class="flex items-center gap-2 px-4 py-2 bg-orange-100 text-orange-600 rounded-lg font-medium hover:bg-orange-200 transition"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
      Добавить ингредиент
    </button>
    
    <div class="mt-4">
      <label class="block text-gray-600 mb-2 text-sm">Быстрый ввод (через запятую)</label>
      <textarea
        v-model="quickInput"
        placeholder="1 стакан муки, 2 яйца, 100г сахара..."
        rows="2"
        class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 resize-none"
        @blur="parseQuickInput"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const ingredients = ref([
  { amount: '', unit: '', name: '' }
])

const quickInput = ref('')

watch(ingredients, (newVal) => {
  emit('update:modelValue', JSON.stringify(newVal))
}, { deep: true })

function addIngredient() {
  ingredients.value.push({ amount: '', unit: '', name: '' })
}

function removeIngredient(index) {
  if (ingredients.value.length > 1) {
    ingredients.value.splice(index, 1)
  }
}

function parseQuickInput() {
  if (!quickInput.value.trim()) return
  
  const parts = quickInput.value.split(',').map(s => s.trim()).filter(Boolean)
  ingredients.value = parts.map(part => {
    const match = part.match(/^([\d\.]+\s*[гкгмллстл]*)?\s*(.+)$/i)
    if (match) {
      return {
        amount: match[1] || '',
        unit: '',
        name: match[2]
      }
    }
    return { amount: '', unit: '', name: part }
  })
  
  quickInput.value = ''
}

// Load from parent on mount
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    try {
      const parsed = JSON.parse(newVal)
      if (Array.isArray(parsed)) {
        ingredients.value = parsed.length > 0 ? parsed : [{ amount: '', unit: '', name: '' }]
      }
    } catch (e) {
      // Not JSON, ignore
    }
  }
}, { immediate: true })
</script>
