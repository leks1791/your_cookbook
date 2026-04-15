<template>
  <div class="flex flex-col w-full min-h-screen">
    <PublicHeader />
    <div class="flex-1">
      <section class="relative h-[600px] flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 z-0 bg-[url('https://images.unsplash.com/photo-1495521821757-a1efb6729352?q=80&w=2000&auto=format&fit=crop')] bg-cover bg-center brightness-[0.6]"></div>
      <div class="relative z-10 text-center px-4 max-w-3xl mx-auto">
        <h1 class="text-4xl md:text-6xl font-serif font-bold text-white mb-6 leading-tight">
          Сохраняй любимые рецепты в одном месте
        </h1>
        <p class="text-lg md:text-xl text-stone-200 mb-8">
          Собирайте собственную кулинарную книгу, изучайте рецепты каталога и переносите понравившиеся блюда в свою коллекцию.
        </p>
        <div class="bg-white p-2 rounded-lg shadow-lg flex flex-col sm:flex-row gap-2 max-w-2xl mx-auto">
          <div class="relative flex-1">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-stone-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Что хотим найти? Например, паста"
              class="w-full pl-10 h-12 border-none focus-visible:ring-0 text-lg px-4"
              @keyup.enter="handleSearch"
            />
          </div>
          <button
            @click="handleSearch"
            class="bg-orange-500 hover:bg-orange-600 text-white h-12 px-8 text-lg w-full sm:w-auto rounded-md transition-colors"
          >
            Найти
          </button>
        </div>
      </div>
    </section>

    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-serif font-bold text-stone-800 mb-10 text-center">Популярные категории</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div
            v-for="cat in categories"
            :key="cat.name"
            :class="[cat.color, 'rounded-2xl p-6 text-center cursor-pointer hover:scale-105 transition-transform']"
            @click="handleCategoryClick(cat.name)"
          >
            <div class="text-4xl mb-3">{{ cat.emoji }}</div>
            <h3 class="font-medium text-stone-800">{{ cat.name }}</h3>
          </div>
        </div>
      </div>
    </section>

    <section class="py-20 bg-stone-50">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-end mb-10">
          <div>
            <h2 class="text-3xl font-serif font-bold text-stone-800">Рецепты от админа</h2>
            <p class="text-stone-500 mt-2">Подборка рецептов, которые доступны всем пользователям.</p>
          </div>
          <router-link to="/catalog" class="text-orange-500 hover:text-orange-600 font-medium transition-colors">
            Смотреть все
          </router-link>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <article
            v-for="recipe in adminRecipes"
            :key="recipe.id"
            class="bg-white rounded-2xl overflow-hidden shadow-sm border border-stone-100 hover:shadow-md transition-shadow group cursor-pointer"
            @click="handleRecipeClick(recipe.id)"
          >
            <div class="p-5">
              <div class="flex items-center justify-between gap-2 mb-3">
                <span class="px-2 py-1 rounded-full text-xs font-semibold bg-orange-100 text-orange-700">
                  Админ
                </span>
                <span class="text-xs text-stone-400">Каталог</span>
              </div>
              <h3 class="font-bold text-lg text-stone-800 mb-2 line-clamp-2">{{ recipe.title }}</h3>
              <p class="text-sm text-stone-500 line-clamp-3">
                {{ recipe.description || 'Описание пока не добавлено.' }}
              </p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-end mb-10">
          <div>
            <h2 class="text-3xl font-serif font-bold text-stone-800">Рецепты сообщества</h2>
            <p class="text-stone-500 mt-2">Одобренные публичные рецепты от пользователей.</p>
          </div>
          <router-link to="/catalog" class="text-orange-500 hover:text-orange-600 font-medium transition-colors">
            Перейти в каталог
          </router-link>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <article
            v-for="recipe in communityRecipes"
            :key="recipe.id"
            class="bg-stone-50 rounded-2xl overflow-hidden shadow-sm border border-stone-100 hover:shadow-md transition-shadow group cursor-pointer"
            @click="handleRecipeClick(recipe.id)"
          >
            <div class="p-5">
              <div class="flex items-center justify-between gap-2 mb-3">
                <span class="px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                  Сообщество
                </span>
                <span class="text-xs text-stone-400">Публичный</span>
              </div>
              <h3 class="font-bold text-lg text-stone-800 mb-2 line-clamp-2">{{ recipe.title }}</h3>
              <p class="text-sm text-stone-500 line-clamp-3">
                {{ recipe.description || 'Описание пока не добавлено.' }}
              </p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="py-24 bg-orange-500 text-white text-center">
      <div class="container mx-auto px-4 max-w-3xl">
        <h2 class="text-4xl font-serif font-bold mb-6">Готовы начать кулинарное путешествие?</h2>
        <p class="text-xl text-orange-100 mb-10">
          Создайте свою личную книгу рецептов, отправляйте лучшие блюда на модерацию и делитесь ими с другими пользователями.
        </p>
        <button
          @click="handleCtaClick"
          class="h-14 px-10 text-lg font-bold text-orange-600 bg-white hover:bg-stone-100 rounded-md transition-colors"
        >
          {{ user ? 'Перейти в дашборд' : 'Открыть каталог' }}
        </button>
      </div>
    </section>
    </div>
    <PublicFooter />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCatalogStore } from '../stores/catalog'
import PublicHeader from './PublicHeader.vue'
import PublicFooter from './PublicFooter.vue'

const router = useRouter()
const authStore = useAuthStore()
const catalogStore = useCatalogStore()

const searchQuery = ref('')
const user = computed(() => authStore.user)
const adminRecipes = computed(() => catalogStore.home.admin)
const communityRecipes = computed(() => catalogStore.home.community)

const categories = [
  { name: 'Завтраки', emoji: '🍳', color: 'bg-yellow-100' },
  { name: 'Обеды', emoji: '🍲', color: 'bg-orange-100' },
  { name: 'Ужины', emoji: '🍝', color: 'bg-red-100' },
  { name: 'Десерты', emoji: '🍰', color: 'bg-pink-100' },
  { name: 'Веганское', emoji: '🥗', color: 'bg-green-100' },
  { name: 'За 15 минут', emoji: '⏱️', color: 'bg-blue-100' },
]

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/catalog?search=${encodeURIComponent(searchQuery.value)}`)
  }
}

const handleCategoryClick = () => {
  router.push('/catalog')
}

const handleRecipeClick = (recipeId) => {
  router.push(`/catalog/${recipeId}`)
}

const handleCtaClick = () => {
  if (user.value) {
    router.push('/dashboard')
  } else {
    router.push('/catalog')
  }
}

onMounted(() => {
  catalogStore.fetchHomeCatalog().catch(() => {})
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
