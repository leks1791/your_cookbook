<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
      <router-link to="/" class="text-2xl font-bold text-orange-600">Your CookBook</router-link>
      <div class="flex items-center space-x-4">
        <template v-if="isAuthenticated">
          <div class="text-gray-600 font-medium">Привет, {{ displayName }}!</div>
          <button @click="$emit('logout')" class="text-gray-600 hover:text-orange-600">Выйти</button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 hover:text-orange-600">Войти</router-link>
          <router-link to="/register" class="bg-orange-500 text-white px-4 py-2 rounded-full hover:bg-orange-600 transition">Регистрация</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated)
const displayName = computed(() => auth.username ?? 'Гость')
</script>
