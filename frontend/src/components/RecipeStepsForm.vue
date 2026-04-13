<template>
  <div class="mb-6">
    <label class="block text-gray-700 mb-3 font-medium">Шаги приготовления</label>
    
    <div class="space-y-4 mb-4">
      <div
        v-for="(step, index) in (Array.isArray(steps) ? steps : [])"
        :key="index"
        class="flex gap-3 items-start p-4 bg-gray-50 rounded-xl group"
        draggable="true"
        @dragstart="handleDragStart(index)"
        @dragover="handleDragOver"
        @drop="handleDrop(index)"
        @dragend="handleDragEnd"
      >
        <div class="flex flex-col gap-1 mt-1">
          <button
            type="button"
            class="cursor-grab p-1 text-gray-400 hover:text-gray-600"
            title="Перетащите для изменения порядка"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M7 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 2zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 14zm6-8a2 2 0 1 0-.001-4.001A2 2 0 0 0 13 4zm0 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 6zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 12z" />
            </svg>
          </button>
          <span class="text-gray-400 font-medium text-sm">{{ index + 1 }}</span>
        </div>
        
        <div class="flex-1">
          <textarea
            v-model="step.description"
            placeholder="Опишите шаг приготовления"
            rows="2"
            class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 resize-none"
          ></textarea>
          
          <div class="flex items-center gap-3 mt-2">
            <div class="flex items-center gap-2">
              <label class="text-xs text-gray-500">Таймер:</label>
              <input
                v-model.number="step.timer_seconds"
                type="number"
                min="0"
                placeholder="мин"
                class="w-20 px-2 py-1 border border-gray-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <span class="text-xs text-gray-500">сек</span>
            </div>
          </div>
        </div>
        
        <button
          type="button"
          @click="removeStep(index)"
          class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition opacity-0 group-hover:opacity-100"
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
      @click="addStep"
      class="flex items-center gap-2 px-4 py-2 bg-orange-100 text-orange-600 rounded-lg font-medium hover:bg-orange-200 transition"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
      Добавить шаг
    </button>
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

const steps = ref([
  { id: Date.now(), description: '', timer_seconds: null }
])

let draggedIndex = null
let isUpdatingFromParent = false

// Функция для обновления order при изменении шагов
function updateOrder() {
  if (isUpdatingFromParent) return
  const currentSteps = steps.value
  emit('update:modelValue', JSON.stringify(currentSteps.map((s, index) => ({
    order: index,
    description: s.description,
    timer_seconds: s.timer_seconds
  }))))
}

// Отслеживаем изменения с debounce
let debounceTimer = null
watch(steps, (newVal) => {
  if (isUpdatingFromParent) return
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    updateOrder()
  }, 10)
}, { deep: true })

function addStep() {
  steps.value = [
    ...steps.value,
    { id: Date.now(), description: '', timer_seconds: null }
  ]
}

function removeStep(index) {
  if (steps.value.length > 1) {
    steps.value = steps.value.filter((_, i) => i !== index)
  }
}

function handleDragStart(index) {
  draggedIndex = index
}

function handleDragOver(e) {
  e.preventDefault()
}

function handleDrop(dropIndex) {
  if (draggedIndex === null || draggedIndex === dropIndex) return
  
  const currentSteps = [...steps.value]
  const draggedStep = currentSteps[draggedIndex]
  currentSteps.splice(draggedIndex, 1)
  currentSteps.splice(dropIndex, 0, draggedStep)
  steps.value = currentSteps
  draggedIndex = null
}

function handleDragEnd() {
  draggedIndex = null
}

// Load from parent on mount
watch(() => props.modelValue, (newVal) => {
  if (newVal && !isUpdatingFromParent) {
    try {
      const parsed = JSON.parse(newVal)
      if (Array.isArray(parsed) && parsed.length > 0) {
        // Проверка, действительно ли данные изменились
        const currentJson = JSON.stringify(steps.value)
        const newJson = JSON.stringify(parsed)
        if (currentJson !== newJson) {
          isUpdatingFromParent = true
          steps.value = parsed.map(s => ({ 
            id: Date.now() + Math.random(), 
            ...s 
          }))
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

<style scoped>
[draggable] {
  cursor: grab;
}

[draggable]:active {
  cursor: grabbing;
}
</style>
