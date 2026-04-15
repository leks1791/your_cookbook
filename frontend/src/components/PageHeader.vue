<template>
  <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold text-stone-800">{{ title }}</h1>
    <slot name="actions">
      <Button 
        v-if="onCreate"
        @click="onCreate"
        :label="buttonText || 'Добавить рецепт'"
        icon="pi pi-plus"
        severity="success"
      />
    </slot>
  </div>
</template>

<script setup>
import Button from 'primevue/button'

defineProps({
  title: {
    type: String,
    required: true
  },
  onCreate: {
    type: Function,
    default: null
  },
  buttonText: {
    type: String,
    default: 'Добавить рецепт'
  }
})
</script>
