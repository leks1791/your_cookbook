<template>
  <button
    :class="[
      'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2',
      sizeClasses[size],
      variantClasses[variant],
      $attrs.class || ''
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'outline', 'link', 'ghost'].includes(v)
  },
  size: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'sm', 'lg'].includes(v)
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const sizeClasses = computed(() => ({
  default: 'px-4 py-2 text-sm',
  sm: 'px-3 py-1.5 text-xs',
  lg: 'px-6 py-3 text-base'
}))

const variantClasses = computed(() => ({
  default: 'bg-orange-500 text-white hover:bg-orange-600',
  outline: 'border border-stone-300 bg-transparent hover:bg-stone-100 text-stone-700',
  link: 'text-orange-500 hover:text-orange-600 p-0',
  ghost: 'bg-transparent hover:bg-stone-100 text-stone-700'
}))
</script>
