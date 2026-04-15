<template>
  <section class="max-w-5xl mx-auto space-y-6">
    <div>
      <h1 class="text-3xl font-bold text-stone-800">Избранное</h1>
      <p class="text-stone-500 mt-2">
        Здесь будут собраны ваши любимые рецепты.
      </p>
    </div>

    <div class="bg-white border border-stone-200 rounded-2xl p-8 text-center">
      <p class="text-stone-600 mb-4">Раздел уже подключен в роутинг, но список избранного пока не реализован.</p>
      <router-link
        to="/recipes"
        class="inline-flex items-center justify-center px-5 py-2.5 rounded-xl bg-orange-500 text-white font-medium hover:bg-orange-600 transition-colors"
      >
        Перейти к рецептам
      </router-link>
    </div>
  </section>
</template>
