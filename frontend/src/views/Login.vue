<template>
  <div class="min-h-screen bg-orange-50 flex items-center justify-center p-6">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-lg p-8">
      <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">Вход в аккаунт</h2>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Email или username</label>
          <input
            v-model="form.emailOrUsername"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 mb-2">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition disabled:opacity-50"
        >
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
      
      <p class="text-center mt-6 text-gray-600">
        Нет аккаунта?
        <router-link to="/register" class="text-orange-500 hover:text-orange-600 font-medium">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  emailOrUsername: '',
  password: '',
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    await auth.login(form.emailOrUsername, form.password)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}
</script>