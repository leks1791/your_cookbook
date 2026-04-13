<template>
  <div class="mb-6">
    <label class="block text-gray-700 mb-3 font-medium">Фото рецепта</label>
    
    <div
      class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-orange-400 transition cursor-pointer"
      @click="triggerFileInput"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
    >
      <input
        ref="fileInput"
        type="file"
        multiple
        accept="image/*"
        class="hidden"
        @change="handleFilesSelected"
      />
      
      <div v-if="!dragOver" class="text-gray-500">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="font-medium">Нажмите для загрузки</p>
        <p class="text-sm text-gray-400">или перетащите фото сюда</p>
      </div>
      
      <div v-else class="text-orange-500">
        <p class="font-medium">Отпустите для загрузки</p>
      </div>
    </div>
    
    <div v-if="photos.length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4">
      <div
        v-for="(photo, index) in photos"
        :key="photo.id"
        class="relative group rounded-xl overflow-hidden aspect-square bg-gray-100"
        draggable="true"
        @dragstart="handleDragStart(index)"
        @dragover="handleDragOverPhoto"
        @drop="handleDropPhoto(index)"
        @dragend="handleDragEnd"
      >
        <img
          :src="photo.preview || photo.url"
          alt="Recipe photo"
          class="w-full h-full object-cover"
        />
        
        <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100">
          <button
            type="button"
            @click.stop="removePhoto(index)"
            class="p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition"
            title="Удалить"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </button>
          <button
            type="button"
            class="p-2 bg-gray-700 text-white rounded-full hover:bg-gray-600 transition cursor-grab"
            title="Перетащите для изменения порядка"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M7 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 2zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 14zm6-8a2 2 0 1 0-.001-4.001A2 2 0 0 0 13 4zm0 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 6zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 12z" />
            </svg>
          </button>
        </div>
        
        <div v-if="photo.isPrimary" class="absolute top-2 left-2 px-2 py-1 bg-green-500 text-white text-xs rounded-full">
          Обложка
        </div>
        
        <button
          v-if="!photo.isPrimary"
          type="button"
          @click="setPrimaryPhoto(index)"
          class="absolute top-2 right-2 px-2 py-1 bg-white bg-opacity-80 text-gray-700 text-xs rounded-full opacity-0 group-hover:opacity-100 transition hover:bg-white"
        >
          Сделать обложкой
        </button>
      </div>
    </div>
    
    <p class="text-xs text-gray-500 mt-3">
      Перетаскивайте фото для изменения порядка. Первое фото будет обложкой.
    </p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const photos = ref([])
const fileInput = ref(null)
const dragOver = ref(false)

let draggedIndex = null
let isUpdatingFromParent = false

watch(() => props.modelValue, (newVal) => {
  if (newVal && Array.isArray(newVal) && !isUpdatingFromParent) {
    const currentJson = JSON.stringify(photos.value)
    const newJson = JSON.stringify(newVal)
    if (currentJson !== newJson) {
      isUpdatingFromParent = true
      photos.value = newVal.map(p => ({
        ...p,
        isPrimary: p.isPrimary || false
      }))
      setTimeout(() => {
        isUpdatingFromParent = false
      }, 0)
    }
  }
}, { immediate: true })

watch(photos, (newVal) => {
  if (isUpdatingFromParent) return
  emit('update:modelValue', newVal)
}, { deep: true })

function triggerFileInput() {
  fileInput.value?.click()
}

function handleDragOver(e) {
  e.preventDefault()
  dragOver.value = true
}

function handleDragLeave() {
  dragOver.value = false
}

function handleDrop(e) {
  e.preventDefault()
  dragOver.value = false
  const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'))
  processFiles(files)
}

function handleFilesSelected(e) {
  const files = Array.from(e.target.files)
  processFiles(files)
  e.target.value = ''
}

function processFiles(files) {
  files.forEach(file => {
    const reader = new FileReader()
    reader.onload = (e) => {
      photos.value.push({
        id: Date.now() + Math.random(),
        url: '',
        preview: e.target.result,
        file: file,
        isPrimary: photos.value.length === 0
      })
    }
    reader.readAsDataURL(file)
  })
}

function removePhoto(index) {
  photos.value.splice(index, 1)
  
  if (photos.value.length > 0 && !photos.value.some(p => p.isPrimary)) {
    photos.value[0].isPrimary = true
  }
}

function setPrimaryPhoto(index) {
  photos.value.forEach((p, i) => {
    p.isPrimary = i === index
  })
}

function handleDragStart(index) {
  draggedIndex = index
}

function handleDragOverPhoto(e) {
  e.preventDefault()
}

function handleDropPhoto(dropIndex) {
  if (draggedIndex === null || draggedIndex === dropIndex) return
  
  const draggedPhoto = photos.value[draggedIndex]
  photos.value.splice(draggedIndex, 1)
  photos.value.splice(dropIndex, 0, draggedPhoto)
  
  draggedIndex = null
}

function handleDragEnd() {
  draggedIndex = null
}
</script>

<style scoped>
[draggable] {
  cursor: grab;
}

[draggable]:active {
  cursor: grabbing;
}
</style>
