<template>
  <button 
    :class="[
      'flex items-center justify-center gap-2 px-4 py-2 rounded-md font-medium text-sm transition-colors',
      variant === 'primary' 
        ? 'bg-orange-500 text-white hover:bg-orange-600' 
        : 'border border-stone-300 text-stone-600 hover:text-orange-500 hover:border-orange-500'
    ]"
    @click="$emit('click', $event)"
  >
    <slot name="icon" />
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (val) => ['primary', 'secondary'].includes(val)
  }
})

defineEmits(['click'])
</script>
