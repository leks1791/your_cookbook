<template>
  <div class="min-h-screen flex">
    <!-- Сайдбар фиксированный слева -->
    <Sidebar @logout="handleLogout" />
    
    <!-- Вторая колонка: хедер + main -->
    <div class="flex-1 flex flex-col ml-64">
      <AppHeader v-if="!hideHeader" @logout="handleLogout" />
      <main class="flex-1 p-6 overflow-y-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import Sidebar from './Sidebar.vue'
import AppHeader from './AppHeader.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const hideHeader = computed(() => route.meta.hideHeader === true)

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
