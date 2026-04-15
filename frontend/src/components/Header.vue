<template>
  <header class="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-md">
    <div class="container mx-auto px-4 h-16 flex items-center justify-between gap-4">
      <router-link to="/" class="flex items-center gap-2 text-orange-500 font-serif text-xl font-bold">
        <ChefHat class="h-6 w-6" />
        <span>RecipeBook</span>
      </router-link>

      <div class="hidden md:flex flex-1 max-w-md relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-stone-400" />
        <input 
          type="text"
          placeholder="Поиск по названию или ингредиентам..." 
          class="w-full pl-9 pr-4 py-2 bg-stone-100 border-transparent rounded-md focus-visible:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 transition-colors"
        />
      </div>

      <nav class="flex items-center gap-4">
        <router-link to="/categories" class="hidden md:block text-sm font-medium text-stone-600 hover:text-orange-500 transition-colors">
          Категории
        </router-link>
        <router-link to="/recipes" class="hidden md:block text-sm font-medium text-stone-600 hover:text-orange-500 transition-colors">
          Случайный рецепт
        </router-link>
        
        <template v-if="isAuthenticated">
          <div class="flex items-center gap-4 ml-4">
            <button 
              @click="$router.push('/dashboard')"
              class="p-2 rounded-md hover:bg-stone-100 transition-colors"
              title="Профиль"
            >
              <UserIcon class="h-5 w-5 text-stone-600" />
            </button>
            <button 
              @click="$emit('logout')" 
              class="hidden sm:flex items-center gap-2 px-4 py-2 border border-stone-300 rounded-md text-stone-600 hover:text-orange-500 hover:border-orange-500 transition-colors text-sm font-medium"
            >
              <LogOut class="h-4 w-4" />
              Выйти
            </button>
          </div>
        </template>
        <template v-else>
          <button 
            @click="$router.push('/login')"
            class="flex items-center gap-2 bg-orange-500 text-white px-4 py-2 rounded-md hover:bg-orange-600 transition-colors text-sm font-medium ml-4"
          >
            <LogIn class="h-4 w-4" />
            Войти
          </button>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import ChefHat from './icons/ChefHat.vue'
import Search from './icons/Search.vue'
import LogIn from './icons/LogIn.vue'
import LogOut from './icons/LogOut.vue'
import UserIcon from './icons/UserIcon.vue'

const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated)

defineEmits(['logout'])
</script>