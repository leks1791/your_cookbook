<template>
  <header class="bg-white shadow-sm sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-end items-center h-16">


        <div class="flex items-center gap-4">
          <router-link to="/catalog" class="text-stone-600 hover:text-orange-500 transition-colors">
            Каталог
          </router-link>
          
          <template v-if="isAuthenticated">
            <div class="flex items-center gap-4 ml-4">
              <Button 
                @click="$router.push('/dashboard')"
                icon="pi pi-user"
                rounded
                text
                severity="secondary"
              />
              <Button 
                @click="$emit('logout')" 
                label="Выйти"
                icon="pi pi-sign-out"
                severity="secondary"
                outlined
                size="small"
              />
            </div>
          </template>
          <template velse>
            <Button 
              @click="$router.push('/login')"
              label="Войти"
              icon="pi pi-sign-in"
              severity="success"
            />
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import ChefHat from './icons/ChefHat.vue'
import Button from 'primevue/button'

const auth = useAuthStore()

const isAuthenticated = computed(() => auth.isAuthenticated)

defineEmits(['logout'])
</script>
