<template>
  <div class="max-w-6xl mx-auto p-6 space-y-6">
    <div class="flex items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-stone-800">Публичный каталог</h1>
        <p class="text-stone-500 mt-2">Одобренные рецепты от админа и сообщества.</p>
      </div>
      <select
        v-model="selectedSource"
        class="px-4 py-2 rounded-xl border border-stone-300 bg-white text-stone-700"
        @change="loadCatalog(1)"
      >
        <option value="">Все</option>
        <option value="admin">От админа</option>
        <option value="community">От сообщества</option>
      </select>
    </div>

    <div v-if="loading" class="py-12 text-center text-stone-500">Загрузка каталога...</div>

    <div v-else-if="recipes.length === 0" class="bg-white border border-stone-200 rounded-2xl p-10 text-center text-stone-500">
      В каталоге пока нет рецептов.
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="recipe in recipes"
        :key="recipe.id"
        class="bg-white rounded-2xl border border-stone-200 shadow-sm hover:shadow-md transition overflow-hidden"
      >
        <div class="p-6 space-y-4">
          <div class="flex items-start justify-between gap-3">
            <h2 class="text-xl font-bold text-stone-800">{{ recipe.title }}</h2>
            <span
              class="px-2.5 py-1 rounded-full text-xs font-semibold"
              :class="recipe.is_admin_recipe ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'"
            >
              {{ recipe.is_admin_recipe ? 'Админ' : 'Сообщество' }}
            </span>
          </div>

          <p class="text-stone-600 text-sm min-h-10">
            {{ recipe.description || 'Описание пока не добавлено.' }}
          </p>

          <div class="flex gap-3 text-xs text-stone-500">
            <span v-if="recipe.prep_time">Подготовка: {{ recipe.prep_time }} мин</span>
            <span v-if="recipe.cook_time">Готовка: {{ recipe.cook_time }} мин</span>
            <span v-if="recipe.servings">Порций: {{ recipe.servings }}</span>
          </div>

          <div class="flex gap-3">
            <router-link
              :to="`/catalog/${recipe.id}`"
              class="px-4 py-2 rounded-xl bg-stone-100 text-stone-700 font-medium hover:bg-stone-200 transition"
            >
              Открыть
            </router-link>
            <button
              v-if="auth.isAuthenticated"
              class="px-4 py-2 rounded-xl bg-orange-500 text-white font-medium hover:bg-orange-600 transition"
              @click="cloneRecipe(recipe.id)"
            >
              Добавить в мою книгу
            </button>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCatalogStore } from '../stores/catalog'

const router = useRouter()
const auth = useAuthStore()
const catalogStore = useCatalogStore()
const selectedSource = ref('')

const recipes = computed(() => catalogStore.recipes)
const loading = computed(() => catalogStore.loading)

async function loadCatalog(page = 1) {
  await catalogStore.fetchCatalog(page, 12, selectedSource.value || null)
}

async function cloneRecipe(id) {
  const created = await catalogStore.cloneRecipe(id)
  router.push(`/recipes/${created.id}`)
}

onMounted(() => {
  loadCatalog()
})
</script>
