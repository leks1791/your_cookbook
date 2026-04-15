<template>
  <div class="space-y-8 max-w-6xl mx-auto">
    <PageHeader
      title="Мой профиль"
      :on-create="() => navigateTo('/recipes/new')"
    />

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <Card
        class="bg-gradient-to-br from-orange-500 to-orange-600 text-white border-none shadow-md cursor-pointer hover:shadow-lg transition-shadow"
        @click="navigateTo('/recipes/new')"
      >
        <CardContent class="p-6 flex items-center gap-4">
          <div class="bg-white/20 w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0">
            <i class="pi pi-plus text-xl text-white"></i>
          </div>
          <div>
            <h3 class="text-xl font-bold">Добавить рецепт</h3>
            <p class="text-orange-100 text-sm">Сохраните новый кулинарный шедевр</p>
          </div>
        </CardContent>
      </Card>

      <Card class="bg-white border-stone-200 shadow-sm cursor-pointer hover:shadow-md transition-shadow">
        <CardContent class="p-6 flex items-center gap-4">
          <div class="bg-stone-100 w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0">
            <i class="pi pi-shopping-cart text-xl text-stone-600"></i>
          </div>
          <div>
            <h3 class="text-xl font-bold text-stone-800">Список покупок</h3>
            <p class="text-stone-500 text-sm">Соберите ингредиенты для готовки</p>
          </div>
        </CardContent>
      </Card>
    </div>

    <section>
      <h2 class="text-2xl font-serif font-bold text-stone-800 mb-4">План на сегодня</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card
          v-for="meal in meals"
          :key="meal"
          class="overflow-hidden border-stone-200 shadow-sm flex flex-col"
        >
          <div class="h-32 relative">
            <img
              :src="`https://picsum.photos/seed/${meal}/400/200`"
              :alt="meal"
              class="w-full h-full object-cover"
              referrerPolicy="no-referrer"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
            <div class="absolute bottom-3 left-3 text-white font-bold text-lg">{{ meal }}</div>
          </div>
          <CardContent class="p-4 flex-1 flex flex-col justify-between">
            <div>
              <h4 class="font-medium text-stone-800 mb-1">Овсянка с ягодами</h4>
              <div class="flex items-center gap-2 text-xs text-stone-500">
                <Clock class="h-3 w-3" /> 15 мин
              </div>
            </div>
            <button class="w-full mt-4 px-4 py-2 border border-stone-300 rounded-md text-stone-600 hover:text-orange-500 hover:border-orange-500 transition-colors text-sm font-medium">
              Заменить
            </button>
          </CardContent>
        </Card>
      </div>
    </section>

    <section>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-2xl font-serif font-bold text-stone-800">Недавно добавленные</h2>
        <button
          @click="navigateTo('/recipes')"
          class="text-orange-500 hover:text-orange-600 transition-colors text-sm font-medium"
        >
          Все рецепты
        </button>
      </div>

      <div v-if="loading" class="h-48 flex items-center justify-center text-stone-400">
        Загрузка...
      </div>

      <div
        v-else-if="recentRecipes.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
      >
        <Card
          v-for="recipe in recentRecipes"
          :key="recipe.id"
          class="overflow-hidden cursor-pointer hover:shadow-md transition-shadow"
          @click="navigateTo(`/recipes/${recipe.id}`)"
        >
          <div class="h-40 relative">
            <img
              :src="recipe.imageUrl || `https://picsum.photos/seed/${recipe.id}/400/300`"
              :alt="recipe.title"
              class="w-full h-full object-cover"
              referrerPolicy="no-referrer"
            />
          </div>
          <CardContent class="p-4">
            <h4 class="font-bold text-stone-800 mb-1 line-clamp-1">{{ recipe.title }}</h4>
            <div class="flex items-center gap-3 text-xs text-stone-500">
              <div class="flex items-center gap-1">
                <Clock class="h-3 w-3" /> {{ (recipe.prepTime || 0) + (recipe.cookTime || 0) }} мин
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div
        v-else
        class="text-center py-12 bg-white rounded-xl border border-dashed border-stone-300"
      >
        <p class="text-stone-500 mb-4">У вас пока нет рецептов.</p>
        <button
          @click="navigateTo('/recipes/new')"
          class="px-6 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors font-medium"
        >
          Добавить первый рецепт
        </button>
      </div>
    </section>

    <section>
      <h2 class="text-2xl font-serif font-bold text-stone-800 mb-4">Мои подборки</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card
          v-for="collection in collections"
          :key="collection"
          class="cursor-pointer hover:shadow-md transition-shadow group"
        >
          <CardContent class="p-4 flex flex-col items-center text-center gap-3">
            <div class="h-16 w-16 bg-orange-100 text-orange-500 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <Folder class="h-8 w-8" />
            </div>
            <div>
              <h4 class="font-medium text-stone-800">{{ collection }}</h4>
              <p class="text-xs text-stone-500">{{ getRandomCount() }} рецептов</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '../components/PageHeader.vue'
import Clock from '../components/icons/Clock.vue'
import Folder from '../components/icons/Folder.vue'
import Card from '../components/ui/Card.vue'
import CardContent from '../components/ui/CardContent.vue'
import { useRecipeStore } from '../stores/recipes'

const router = useRouter()
const recipeStore = useRecipeStore()
const recentRecipes = ref([])
const loading = ref(true)
const meals = ['Завтрак', 'Обед', 'Ужин']
const collections = ['На Новый год', 'Диета', 'Для детей', 'Быстрые ужины']

async function fetchRecentRecipes() {
  loading.value = true
  try {
    await recipeStore.fetchRecipes(1, 4)
    recentRecipes.value = recipeStore.recipes
  } catch (error) {
    console.error('Error fetching recipes:', error)
  } finally {
    loading.value = false
  }
}

function navigateTo(path) {
  router.push(path)
}

function getRandomCount() {
  return Math.floor(Math.random() * 20) + 1
}

onMounted(() => {
  fetchRecentRecipes()
})
</script>
