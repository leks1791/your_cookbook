<template>
  <div class="flex flex-col w-full min-h-screen">
    <PublicHeader />
    
    <main class="flex-1 container mx-auto px-4 py-12 max-w-5xl">
      <!-- Заголовок -->
      <section class="text-center mb-16">
        <h1 class="text-4xl md:text-5xl font-bold text-stone-800 mb-6">
          О проекте RecipeBook
        </h1>
        <p class="text-xl text-stone-600 max-w-3xl mx-auto">
          Ваша личная кулинарная книга и сообщество любителей готовки
        </p>
      </section>

      <!-- Какие проблемы решает -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-stone-800 mb-8 text-center">
          Какие проблемы мы решаем
        </h2>
        
        <div class="grid md:grid-cols-2 gap-6">
          <div class="bg-white p-6 rounded-xl shadow-sm border border-stone-100">
            <div class="h-12 w-12 bg-orange-100 text-orange-500 rounded-lg flex items-center justify-center mb-4">
              <BookOpen class="h-6 w-6" />
            </div>
            <h3 class="text-lg font-semibold text-stone-800 mb-2">
              Потерянные рецепты
            </h3>
            <p class="text-stone-600">
              Забудьте о записках на холодильнике, сохранённых скриншотах и потерянных вкладках браузера. Все ваши рецепты в одном безопасном месте.
            </p>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-stone-100">
            <div class="h-12 w-12 bg-blue-100 text-blue-500 rounded-lg flex items-center justify-center mb-4">
              <Users class="h-6 w-6" />
            </div>
            <h3 class="text-lg font-semibold text-stone-800 mb-2">
              Обмен опытом
            </h3>
            <p class="text-stone-600">
              Делитесь рецептами с друзьями и сообществом. Управляйте своими публикациями и moderруйте контент других пользователей.
            </p>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-stone-100">
            <div class="h-12 w-12 bg-green-100 text-green-500 rounded-lg flex items-center justify-center mb-4">
              <Search class="h-6 w-6" />
            </div>
            <h3 class="text-lg font-semibold text-stone-800 mb-2">
              Сложности поиска
            </h3>
            <p class="text-stone-600">
              Быстрый поиск по названию, ингредиентам и тегам. Находите нужные рецепты за секунды, а не минуты.
            </p>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-stone-100">
            <div class="h-12 w-12 bg-purple-100 text-purple-500 rounded-lg flex items-center justify-center mb-4">
              <Heart class="h-6 w-6" />
            </div>
            <h3 class="text-lg font-semibold text-stone-800 mb-2">
              Нет системы
            </h3>
            <p class="text-stone-600">
              Организуйте рецепты по категориям, тегами и коллекциям. Создавайте свои подборки для разных случаев жизни.
            </p>
          </div>
        </div>
      </section>

      <!-- Возможности -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-stone-800 mb-8 text-center">
          Возможности платформы
        </h2>

        <div class="space-y-4">
          <div class="flex items-start gap-4 p-4 bg-white rounded-lg shadow-sm">
            <div class="h-8 w-8 bg-orange-500 text-white rounded-full flex items-center justify-center flex-shrink-0">
              1
            </div>
            <div>
              <h3 class="font-semibold text-stone-800">Личная библиотека рецептов</h3>
              <p class="text-stone-600">Создавайте, редактируйте и храните свои рецепты с фото, пошаговыми инструкциями и временем приготовления</p>
            </div>
          </div>

          <div class="flex items-start gap-4 p-4 bg-white rounded-lg shadow-sm">
            <div class="h-8 w-8 bg-orange-500 text-white rounded-full flex items-center justify-center flex-shrink-0">
              2
            </div>
            <div>
              <h3 class="font-semibold text-stone-800">Каталог сообщества</h3>
              <p class="text-stone-600">Открывайте новые рецепты от других пользователей, добавляйте любимые в избранное</p>
            </div>
          </div>

          <div class="flex items-start gap-4 p-4 bg-white rounded-lg shadow-sm">
            <div class="h-8 w-8 bg-orange-500 text-white rounded-full flex items-center justify-center flex-shrink-0">
              3
            </div>
            <div>
              <h3 class="font-semibold text-stone-800">Умный поиск и фильтрация</h3>
              <p class="text-stone-600">Ищите по названию, ингредиентам, времени приготовления и категориям</p>
            </div>
          </div>

          <div class="flex items-start gap-4 p-4 bg-white rounded-lg shadow-sm">
            <div class="h-8 w-8 bg-orange-500 text-white rounded-full flex items-center justify-center flex-shrink-0">
              4
            </div>
            <div>
              <h3 class="font-semibold text-stone-800">Модерация контента</h3>
              <p class="text-stone-600">Администраторы могут проверять и одобрять рецепты от сообщества, поддерживая высокое качество контента</p>
            </div>
          </div>

          <div class="flex items-start gap-4 p-4 bg-white rounded-lg shadow-sm">
            <div class="h-8 w-8 bg-orange-500 text-white rounded-full flex items-center justify-center flex-shrink-0">
              5
            </div>
            <div>
              <h3 class="font-semibold text-stone-800">Коллекции и теги</h3>
              <p class="text-stone-600">Создавайте тематические подборки: "Завтраки за 15 минут", "Десерты без выпечки", "Для семейного ужина"</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Технологии -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-stone-800 mb-6 text-center">
          Технологический стек
        </h2>
        <div class="flex flex-wrap justify-center gap-3">
          <span class="px-4 py-2 bg-stone-100 text-stone-700 rounded-full text-sm font-medium">Vue 3</span>
          <span class="px-4 py-2 bg-stone-100 text-stone-700 rounded-full text-sm font-medium">Python FastAPI</span>
          <span class="px-4 py-2 bg-stone-100 text-stone-700 rounded-full text-sm font-medium">PostgreSQL</span>
          <span class="px-4 py-2 bg-stone-100 text-stone-700 rounded-full text-sm font-medium">Docker</span>
          <span class="px-4 py-2 bg-stone-100 text-stone-700 rounded-full text-sm font-medium">TailwindCSS</span>
          <span class="px-4 py-2 bg-stone-100 text-stone-700 rounded-full text-sm font-medium">Pinia</span>
        </div>
      </section>

      <!-- Призыв к действию -->
      <section class="text-center">
        <h2 class="text-2xl font-bold text-stone-800 mb-4">
          Готовы начать?
        </h2>
        <p class="text-stone-600 mb-8">
          Присоединяйтесь к сообществу любителей готовки уже сегодня
        </p>
        <div class="flex justify-center gap-4">
          <router-link
            to="/register"
            class="px-6 py-3 bg-orange-500 text-white rounded-xl font-semibold hover:bg-orange-600 transition"
          >
            Создать аккаунт
          </router-link>
          <router-link
            to="/catalog"
            class="px-6 py-3 border border-stone-300 text-stone-700 rounded-xl font-semibold hover:bg-stone-50 transition"
          >
            Смотреть рецепты
          </router-link>
        </div>
      </section>
    </main>

    <PublicFooter />
  </div>
</template>

<script setup>
import PublicHeader from '../components/PublicHeader.vue'
import PublicFooter from '../components/PublicFooter.vue'
import BookOpen from '../components/icons/BookOpen.vue'
import Users from '../components/icons/UserIcon.vue'
import Search from '../components/icons/Search.vue'
import Heart from '../components/icons/Heart.vue'
</script>
