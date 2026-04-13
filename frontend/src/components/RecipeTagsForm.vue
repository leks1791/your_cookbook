да<template>
  <div class="mb-6">
    <label class="block text-gray-700 mb-3 font-medium">Теги</label>
    
    <div class="flex flex-wrap gap-2 mb-3">
      <span
        v-for="tag in localTags"
        :key="tag"
        class="inline-flex items-center gap-1 px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm"
      >
        {{ tag }}
        <button
          type="button"
          @click="removeTag(tag)"
          class="hover:text-orange-900"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </span>
      
      <div v-if="!showInput && localTags.length === 0" class="text-gray-400 text-sm italic">Нажмите + чтобы добавить</div>
    </div>
    
    <div v-if="showInput" class="flex gap-2 mb-3">
      <input
        ref="inputRef"
        v-model="newTag"
        type="text"
        placeholder="Введите тег и нажмите Enter"
        class="flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
        @keyup.enter="addTag"
        @keyup.escape="cancelAdd"
      />
      <button
        type="button"
        @click="addTag"
        class="px-4 py-2 bg-orange-500 text-white rounded-lg text-sm font-medium hover:bg-orange-600 transition"
      >
        Добавить
      </button>
      <button
        type="button"
        @click="cancelAdd"
        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-300 transition"
      >
        Отмена
      </button>
    </div>
    
    <button
      v-if="!showInput"
      type="button"
      @click="startAddTag"
      class="flex items-center gap-2 px-4 py-2 border-2 border-dashed border-gray-300 text-gray-500 rounded-lg font-medium hover:border-orange-400 hover:text-orange-500 transition"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
      Добавить тег
    </button>
    
    <div class="mt-4">
      <p class="text-xs text-gray-500 mb-2">Популярные теги:</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="suggestion in suggestions"
          :key="suggestion"
          type="button"
          @click="addSuggestion(suggestion)"
          :disabled="localTags.includes(suggestion)"
          class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs hover:bg-orange-100 hover:text-orange-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ suggestion }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const localTags = ref([])
const newTag = ref('')
const showInput = ref(false)
const inputRef = ref(null)
let isUpdatingFromParent = false

const suggestions = ref(['Завтрак', 'Обед', 'Ужин', 'Десерт', 'Вегетарианское', 'Без глютена', 'Быстро', 'Здоровое'])

onMounted(() => {
  // Инициализируем localTags из props только один раз
  if (props.modelValue && Array.isArray(props.modelValue)) {
    localTags.value = [...props.modelValue]
  }
})

function startAddTag() {
  showInput.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

function addTag() {
  const tag = newTag.value.trim()
  if (tag && !localTags.value.includes(tag)) {
    localTags.value.push(tag)
    emit('update:modelValue', [...localTags.value])
  }
  newTag.value = ''
  cancelAdd()
}

function addSuggestion(suggestion) {
  if (!localTags.value.includes(suggestion)) {
    localTags.value.push(suggestion)
    emit('update:modelValue', [...localTags.value])
  }
}

function removeTag(tag) {
  const index = localTags.value.indexOf(tag)
  if (index !== -1) {
    localTags.value.splice(index, 1)
    emit('update:modelValue', [...localTags.value])
  }
}

function cancelAdd() {
  showInput.value = false
  newTag.value = ''
}

// Watch for parent updates
watch(() => props.modelValue, (newVal) => {
  if (newVal && Array.isArray(newVal) && !isUpdatingFromParent) {
    const currentJson = JSON.stringify(localTags.value)
    const newJson = JSON.stringify(newVal)
    if (currentJson !== newJson) {
      isUpdatingFromParent = true
      localTags.value = [...newVal]
      setTimeout(() => {
        isUpdatingFromParent = false
      }, 0)
    }
  }
}, { immediate: true })
</script>
