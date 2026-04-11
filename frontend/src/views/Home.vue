<template>
  <!-- Hero секция -->
  <header class="max-w-6xl mx-auto px-6 py-16 text-center">
    <h2 class="text-5xl md:text-6xl font-extrabold mb-6">Ваши лучшие рецепты — <br/><span class="text-orange-500">теперь в одном месте.</span></h2>
    <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">Хватит искать рецепт в заметках, скриншотах и старых тетрадках. Создайте свою идеальную кулинарную книгу, где всё только проверенное и любимое.</p>
    <router-link to="/register" class="bg-gray-900 text-white px-10 py-4 rounded-xl text-lg font-semibold hover:bg-gray-800 transition">Создать свою книгу</router-link>
  </header>

  <!-- Преимущества -->
  <section class="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-12">
    <div v-for="feature in features" :key="feature.title" class="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
      <div class="text-4xl mb-4">{{ feature.icon }}</div>
      <h3 class="text-xl font-bold mb-3">{{ feature.title }}</h3>
      <p class="text-gray-600">{{ feature.desc }}</p>
    </div>
  </section>
</template>

<script setup>
const features = [
  { icon: '📔', title: 'Всё под рукой', desc: 'Забудьте о хаосе в скриншотах и записках. Ваша база данных рецептов всегда в кармане.' },
  { icon: '✨', title: 'Только ваш выбор', desc: 'Никаких навязанных вариантов. Сохраняйте именно ту версию блюда, которая нравится вам.' },
  { icon: '🚀', title: 'Удобный формат', desc: 'Создавайте свои пошаговые инструкции, добавляйте фото и теги для быстрого поиска.' }
]
</script>
