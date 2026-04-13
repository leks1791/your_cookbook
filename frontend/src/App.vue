<template>
  <div class="min-h-screen bg-orange-50 flex flex-col">
    <Header :isAuthenticated="auth.isAuthenticated" @logout="logout" />
    <main class="flex-1 py-8">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { useAuthStore } from './stores/auth'
import { onMounted, watch } from 'vue'
import api from './api'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

auth.init()

async function fetchMe() {
  try {
    const res = await api.get('/auth/me')
    const name = res?.data?.username ?? null
    if (name) {
      auth.setUsername(name)
    }
  } catch {
    // ignore
  }
}

onMounted(async () => {
  if (auth.isAuthenticated) {
    await fetchMe()
  }
})

watch(
  () => auth.isAuthenticated,
  async (newVal) => {
    if (newVal) {
      await fetchMe()
    } else {
      auth.setUsername(null)
    }
  }
)

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
