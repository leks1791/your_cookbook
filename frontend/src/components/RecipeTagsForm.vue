да<template>
  <div class="mb-6">
    <label class="block text-gray-700 mb-3 font-medium">Теги</label>
    
    <div class="flex flex-wrap gap-2 mb-3">
      <Tag
        v-for="tag in localTags"
        :key="tag"
        :removable="true"
        @remove="removeTag(tag)"
      >
        {{ tag }}
      </Tag>
      
      <div v-if="!showInput && localTags.length === 0" class="text-gray-400 text-sm italic">Нажмите + чтобы добавить</div>
    </div>
    
    <div v-if="showInput" class="flex gap-2 mb-3">
      <InputText
        ref="inputRef"
        v-model="newTag"
        type="text"
        placeholder="Введите тег и нажмите Enter"
        class="flex-1"
        @keyup.enter="addTag"
        @keyup.escape="cancelAdd"
      />
      <Button
        type="button"
        @click="addTag"
        label="Добавить"
        icon="pi pi-plus"
        size="small"
      />
      <Button
        type="button"
        @click="cancelAdd"
        label="Отмена"
        severity="secondary"
        size="small"
        outlined
      />
    </div>
    
    <Button
      v-if="!showInput"
      type="button"
      @click="startAddTag"
      label="Добавить тег"
      icon="pi pi-plus"
      outlined
      severity="secondary"
    />
    
    <div class="mt-4">
      <p class="text-xs text-gray-500 mb-2">Популярные теги:</p>
      <div class="flex flex-wrap gap-2">
        <Button
          v-for="suggestion in suggestions"
          :key="suggestion"
          type="button"
          @click="addSuggestion(suggestion)"
          :disabled="localTags.includes(suggestion)"
          :label="suggestion"
          severity="secondary"
          size="small"
          outlined
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import Tag from 'primevue/tag'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

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
