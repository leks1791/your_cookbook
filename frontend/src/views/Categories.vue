<template>
  <div class="min-h-screen py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Категории рецептов</h1>
            <p class="text-gray-600 mt-2">Управляйте категориями для ваших рецептов</p>
          </div>
          <button 
            @click="showAddModal = true"
            class="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition flex items-center"
          >
            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Добавить категорию
          </button>
        </div>
      </div>

      <!-- Categories List -->
      <div v-if="loading" class="text-center py-8">
        <p class="text-gray-500">Загрузка...</p>
      </div>

      <div v-else-if="categories.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
        <p class="text-gray-500 mb-4">У вас ещё нет категорий</p>
        <button 
          @click="showAddModal = true"
          class="text-orange-500 hover:text-orange-600 font-medium"
        >
          Добавить первую категорию →
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="category in categories" 
          :key="category.id"
          class="bg-white rounded-lg shadow p-6 hover:shadow-md transition"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center">
              <div 
                class="w-12 h-12 rounded-full flex items-center justify-center text-white text-xl font-bold"
                :style="{ backgroundColor: category.color }"
              >
                {{ category.name.charAt(0).toUpperCase() }}
              </div>
              <div class="ml-4">
                <h3 class="font-semibold text-gray-900">{{ category.name }}</h3>
                <p class="text-sm text-gray-500">{{ category.description || 'Нет описания' }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ category.recipe_count || 0 }} рецептов</p>
              </div>
            </div>
            <div class="flex space-x-2">
              <button 
                @click="editCategory(category)"
                class="text-blue-500 hover:text-blue-600 p-1"
                title="Редактировать"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
              <button 
                @click="deleteCategory(category.id)"
                class="text-red-500 hover:text-red-600 p-1"
                title="Удалить"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Add/Edit Modal -->
      <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h2 class="text-xl font-bold mb-4">
            {{ editingCategory ? 'Редактировать категорию' : 'Новая категория' }}
          </h2>
          
          <form @submit.prevent="saveCategory">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Название</label>
              <input 
                v-model="form.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="Например: Завтраки"
              />
            </div>
            
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Описание</label>
              <textarea 
                v-model="form.description"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                rows="3"
                placeholder="Краткое описание категории"
              ></textarea>
            </div>
            
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Цвет</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="color in colors"
                  :key="color"
                  type="button"
                  @click="form.color = color"
                  class="w-10 h-10 rounded-full transition transform hover:scale-110"
                  :style="{ 
                    backgroundColor: color,
                    border: form.color === color ? '3px solid #333' : '2px solid transparent'
                  }"
                ></button>
              </div>
            </div>
            
            <div class="flex justify-end space-x-3">
              <button 
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
              >
                Отмена
              </button>
              <button 
                type="submit"
                class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition"
              >
                {{ editingCategory ? 'Сохранить' : 'Создать' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Categories',
  data() {
    return {
      categories: [],
      loading: true,
      showAddModal: false,
      editingCategory: null,
      form: {
        name: '',
        description: '',
        color: '#f97316'
      },
      colors: [
        '#f97316', '#ef4444', '#ec4899', '#8b5cf6', 
        '#3b82f6', '#06b6d4', '#10b981', '#84cc16'
      ]
    }
  },
  async mounted() {
    await this.loadCategories()
  },
  methods: {
    async loadCategories() {
      try {
        this.loading = true
        const response = await api.get('/categories')
        this.categories = response.data
      } catch (error) {
        console.error('Ошибка загрузки категорий:', error)
        alert('Не удалось загрузить категории')
      } finally {
        this.loading = false
      }
    },
    editCategory(category) {
      this.editingCategory = category
      this.form = {
        name: category.name,
        description: category.description || '',
        color: category.color || '#f97316'
      }
      this.showAddModal = true
    },
    async saveCategory() {
      try {
        if (this.editingCategory) {
          await api.put(`/categories/${this.editingCategory.id}`, this.form)
          alert('Категория обновлена!')
        } else {
          await api.post('/categories', this.form)
          alert('Категория создана!')
        }
        this.closeModal()
        await this.loadCategories()
        // Notify dashboard to refresh categories
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('category_updated'))
        }
      } catch (error) {
        console.error('Ошибка сохранения категории:', error)
        alert('Не удалось сохранить категорию')
      }
    },
    async deleteCategory(id) {
      if (!confirm('Вы уверены, что хотите удалить эту категорию?')) {
        return
      }
      
      try {
        await api.delete(`/categories/${id}`)
        alert('Категория удалена!')
        await this.loadCategories()
      } catch (error) {
        console.error('Ошибка удаления категории:', error)
        alert('Не удалось удалить категорию')
      }
    },
    closeModal() {
      this.showAddModal = false
      this.editingCategory = null
      this.form = {
        name: '',
        description: '',
        color: '#f97316'
      }
    }
  }
}
</script>
