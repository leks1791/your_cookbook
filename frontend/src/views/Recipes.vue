<template>
  <div class="max-w-6xl mx-auto p-6">
    <PageHeader
      title="Мои рецепты"
      button-text="Добавить рецепт"
      :on-create="() => $router.push('/recipes/new')"
    />

    <div v-if="loading" class="text-center py-16 text-gray-500">Загрузка...</div>

    <div v-else-if="recipes.length === 0" class="text-center py-16 bg-white rounded-2xl shadow-sm">
      <div class="text-6xl mb-4">📖</div>
      <p class="text-xl text-gray-600 mb-4">У вас пока нет рецептов</p>
      <button
        @click="$router.push('/recipes/new')"
        class="inline-block px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition"
      >
        Добавить первый рецепт
      </button>
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="recipe in recipes"
        :key="recipe.id"
        class="bg-white rounded-2xl shadow-sm border border-gray-200 hover:shadow-lg transition cursor-pointer group relative"
        @click="$router.push(`/recipes/${recipe.id}`)"
      >
        <div class="p-6">
          <div class="flex items-start justify-between gap-3 mb-2">
            <h3 class="text-xl font-bold text-gray-800 group-hover:text-orange-500 transition">
              {{ recipe.title }}
            </h3>
            <span
              class="px-2 py-1 rounded-full text-[11px] font-semibold whitespace-nowrap"
              :class="statusClass(recipe.publication_status)"
            >
              {{ statusLabel(recipe.publication_status) }}
            </span>
          </div>
          <p class="text-gray-600 mb-4 line-clamp-2 text-sm">{{ recipe.description || 'Нет описания' }}</p>

          <div v-if="recipe.tags && recipe.tags.length" class="flex flex-wrap gap-1 mb-4">
            <span
              v-for="tag in recipe.tags.slice(0, 3)"
              :key="tag"
              class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full text-xs font-medium"
            >
              {{ tag }}
            </span>
          </div>

          <div class="flex items-center gap-4 text-xs text-gray-500 mb-4">
            <div v-if="recipe.prep_time" class="flex items-center gap-1">
              <Clock class="h-4 w-4" />
              <span>{{ recipe.prep_time }} мин</span>
            </div>
            <div v-if="recipe.servings" class="flex items-center gap-1">
              <Users class="h-4 w-4" />
              <span>{{ recipe.servings }} порц.</span>
            </div>
          </div>

          <div class="text-xs text-gray-400">
            {{ formatDate(recipe.created_at) }}
          </div>
        </div>

        <div class="absolute top-4 right-4">
          <div class="relative" @click.stop>
            <button
              @click="toggleMenu(recipe.id)"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition"
            >
              <MoreVertical class="h-5 w-5" />
            </button>

            <div
              v-if="activeMenuId === recipe.id"
              class="absolute right-0 mt-2 w-52 bg-white rounded-lg shadow-lg border border-gray-100 z-10"
            >
              <router-link
                :to="`/recipes/${recipe.id}/edit`"
                class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 hover:text-orange-600 transition"
                @click.stop
              >
                <Edit class="h-4 w-4" />
                Редактировать
              </router-link>
              <button
                v-if="recipe.publication_status !== 'pending_review'"
                @click="submitForReview(recipe.id)"
                class="flex items-center gap-2 w-full px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 transition"
              >
                <Settings class="h-4 w-4" />
                Отправить на модерацию
              </button>
              <button
                @click="deleteRecipe(recipe.id)"
                class="flex items-center gap-2 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
              >
                <Trash2 class="h-4 w-4" />
                Удалить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-10">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="changePage(page)"
        :class="[
          'px-4 py-2 rounded-lg transition',
          page === currentPage
            ? 'bg-orange-500 text-white'
            : 'bg-white text-gray-700 hover:bg-orange-50 border border-orange-100',
        ]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRecipeStore } from '../stores/recipes'
import PageHeader from '../components/PageHeader.vue'
import Clock from '../components/icons/Clock.vue'
import MoreVertical from '../components/icons/ListTodo.vue'
import Edit from '../components/icons/Settings.vue'
import Trash2 from '../components/icons/LogOut.vue'
import Users from '../components/icons/UserIcon.vue'
import Settings from '../components/icons/Settings.vue'

const recipeStore = useRecipeStore()

const recipes = computed(() => recipeStore.recipes)
const loading = computed(() => recipeStore.loading)
const pagination = computed(() => recipeStore.pagination)
const currentPage = computed(() => pagination.value.page)
const totalPages = computed(() => pagination.value.totalPages)
const activeMenuId = ref(null)

onMounted(() => {
  recipeStore.fetchRecipes()
})

async function deleteRecipe(id) {
  activeMenuId.value = null
  if (confirm('Удалить рецепт?')) {
    await recipeStore.deleteRecipe(id)
    await recipeStore.fetchRecipes(currentPage.value)
  }
}

async function submitForReview(id) {
  activeMenuId.value = null
  await recipeStore.submitForReview(id)
  await recipeStore.fetchRecipes(currentPage.value)
}

function changePage(page) {
  recipeStore.fetchRecipes(page)
}

function toggleMenu(id) {
  activeMenuId.value = activeMenuId.value === id ? null : id
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function statusLabel(status) {
  return {
    draft: 'Черновик',
    pending_review: 'На модерации',
    approved: 'Одобрен',
    rejected: 'Отклонён',
  }[status] || status
}

function statusClass(status) {
  return {
    draft: 'bg-stone-100 text-stone-700',
    pending_review: 'bg-amber-100 text-amber-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
  }[status] || 'bg-stone-100 text-stone-700'
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
