<template>
  <div class="space-y-8">
    <!-- Hero секция с градиентом -->
    <header class="max-w-6xl mx-auto px-6 py-20 text-center relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-orange-100/50 to-amber-50/50 rounded-3xl -z-10" />
      <h2 class="text-5xl md:text-7xl font-extrabold mb-6 leading-tight">
        Ваши лучшие рецепты —<br />
        <span class="hero-gradient">теперь в одном месте.</span>
      </h2>
      <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
        Хватит искать рецепты в заметках, скриншотах и старых тетрадках. 
        Создайте свою идеальную кулинарную книгу, где всё — только проверенное и любимое.
      </p>
      <router-link 
        to="/register" 
        class="inline-block bg-gradient-to-r from-orange-500 to-amber-500 text-white px-12 py-5 rounded-2xl text-xl font-semibold hover:from-orange-600 hover:to-amber-600 transition-all shadow-lg hover:shadow-xl hover:-translate-y-1"
      >
        Создать свою книгу
      </router-link>
    </header>

    <!-- Преимущества с карточками -->
    <section class="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-8">
      <div 
        v-for="(feature, index) in features" 
        :key="feature.title" 
        class="card-gradient p-8 rounded-3xl"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="text-5xl mb-6 transform hover:scale-110 transition-transform duration-300">{{ feature.icon }}</div>
        <h3 class="text-2xl font-bold mb-4 text-gray-800">{{ feature.title }}</h3>
        <p class="text-gray-600 leading-relaxed">{{ feature.desc }}</p>
      </div>
    </section>

    <!-- Призыв к действию -->
    <section class="max-w-4xl mx-auto px-6 py-16 text-center">
      <div class="card-gradient p-12 rounded-3xl">
        <h3 class="text-3xl font-bold mb-4">Готовы начать?</h3>
        <p class="text-gray-600 mb-8">Присоединяйтесь к тысячам любителей кулинарии</p>
        <router-link 
          to="/login" 
          class="inline-block bg-gray-900 text-white px-10 py-4 rounded-xl text-lg font-semibold hover:bg-gray-800 transition-all hover:shadow-lg"
        >
          Войти в аккаунт
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
const features = [
  { icon: '📔', title: 'Всё под рукой', desc: 'Забудьте о хаосе в скриншотах и записках. Ваша база данных рецептов всегда в кармане.' },
  { icon: '✨', title: 'Только ваш выбор', desc: 'Никаких навязанных вариантов. Сохраняйте именно ту версию блюда, которая нравится вам.' },
  { icon: '🚀', title: 'Удобный формат', desc: 'Создавайте свои пошаговые инструкции, добавляйте фото и теги для быстрого поиска.' }
]
</script>
