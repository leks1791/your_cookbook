<template>
  <aside class="fixed left-0 top-0 h-screen w-64 bg-white border-r border-stone-200 p-6 flex flex-col z-40">
    <div class="mb-8">
      <router-link to="/" class="flex items-center gap-2 text-orange-500 font-serif text-2xl font-bold hover:text-orange-600 transition-colors">
        <ChefHat class="h-8 w-8" />
        <span>RecipeBook</span>
      </router-link>
    </div>

    <nav class="flex-1 space-y-2">
      <router-link
        to="/dashboard"
        class="flex items-center gap-3 px-3 py-2 rounded-md text-stone-600 hover:bg-orange-50 hover:text-orange-500 font-medium transition-colors"
        active-class="bg-orange-50 text-orange-500"
      >
        <i class="pi pi-home"></i>
        Дашборд
      </router-link>
      <router-link
        to="/recipes"
        class="flex items-center gap-3 px-3 py-2 rounded-md text-stone-600 hover:bg-orange-50 hover:text-orange-500 font-medium transition-colors"
        active-class="bg-orange-50 text-orange-500"
      >
        <i class="pi pi-book"></i>
        Рецепты
      </router-link>
      <router-link
        to="/categories"
        class="flex items-center gap-3 px-3 py-2 rounded-md text-stone-600 hover:bg-orange-50 hover:text-orange-500 font-medium transition-colors"
        active-class="bg-orange-50 text-orange-500"
      >
        <i class="pi pi-folder"></i>
        Категории
      </router-link>
      <router-link
        to="/favorites"
        class="flex items-center gap-3 px-3 py-2 rounded-md text-stone-600 hover:bg-orange-50 hover:text-orange-500 font-medium transition-colors"
        active-class="bg-orange-50 text-orange-500"
      >
        <i class="pi pi-heart"></i>
        Избранное
      </router-link>
      <router-link
        to="/tags"
        class="flex items-center gap-3 px-3 py-2 rounded-md text-stone-600 hover:bg-orange-50 hover:text-orange-500 font-medium transition-colors"
        active-class="bg-orange-50 text-orange-500"
      >
        <i class="pi pi-tags"></i>
        Теги
      </router-link>

      <div v-if="auth.isAdmin" class="pt-4 mt-4 border-t border-stone-200">
        <router-link
          to="/admin/moderation"
          class="flex items-center gap-3 px-3 py-2 rounded-md text-stone-600 hover:bg-orange-50 hover:text-orange-500 font-medium transition-colors"
          active-class="bg-orange-50 text-orange-500"
        >
          <i class="pi pi-shield"></i>
          Модерация
        </router-link>
      </div>
    </nav>

    <div class="p-4 border-t">
      <Button 
        label="Выйти"
        icon="pi pi-sign-out"
        severity="secondary"
        outlined
        @click="$emit('logout')"
        class="w-full"
      />
    </div>
  </aside>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import ChefHat from './icons/ChefHat.vue'
import Button from 'primevue/button'

const auth = useAuthStore()

defineEmits(['logout'])
</script>
