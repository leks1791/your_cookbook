<template>
  <div class="min-h-screen">
    <!-- Toast уведомления -->
    <Toast position="top-right" />
    
    <!-- Главная страница - всегда без сайдбара и хедера -->
    <router-view v-if="route.path === '/'" v-slot="{ Component }">
      <component :is="Component" :key="route.fullPath" />
    </router-view>
    
    <!-- Public страницы (без сайдбара и хедера) -->
    <router-view v-else-if="toPublicLayout" v-slot="{ Component }">
      <component :is="Component" :key="route.fullPath" />
    </router-view>
    
    <!-- Authenticated страницы с MainLayout (сайдбар + хедер + main) -->
    <MainLayout v-else>
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </MainLayout>
  </div>
</template>

<script setup>
import MainLayout from './components/MainLayout.vue'
import Toast from 'primevue/toast'
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const auth = useAuthStore()
const route = useRoute()

// Public страницы - всегда без сайдбара и MainLayout, независимо от авторизации
const toPublicLayout = computed(() => {
  const publicRoutes = ['login', 'register', 'about', 'catalog', 'categories', 'tags', 'recipes-by-tag', 'catalog-detail']
  const routeName = route.name
  const routePath = route.path.replace('/', '')
  return publicRoutes.includes(routeName) || publicRoutes.includes(routePath)
})

auth.init()
</script>
