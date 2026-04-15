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
        
        <Button
          type="button"
          @click="removeIngredient(index)"
          icon="pi pi-trash"
          severity="danger"
          text
          size="small"
          title="Удалить"
        />
      </div>
    </div>
    
    <Button
      type="button"
      @click="addIngredient"
      label="Добавить ингредиент"
      icon="pi pi-plus"
      severity="secondary"
      outlined
    />
    
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
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

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
let isUpdatingFromParent = false

watch(ingredients, (newVal) => {
  if (isUpdatingFromParent) return
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
  if (newVal && !isUpdatingFromParent) {
    try {
      const parsed = JSON.parse(newVal)
      if (Array.isArray(parsed)) {
        const currentJson = JSON.stringify(ingredients.value)
        const newJson = JSON.stringify(parsed)
        if (currentJson !== newJson) {
          isUpdatingFromParent = true
          ingredients.value = parsed.length > 0 ? parsed : [{ amount: '', unit: '', name: '' }]
          setTimeout(() => {
            isUpdatingFromParent = false
          }, 0)
        }
      }
    } catch (e) {
      // Not JSON, ignore
    }
  }
}, { immediate: true })
</script>
