<template>
  <footer class="border-t bg-white py-8 mt-auto">
    <div class="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-stone-500">
      <p>© 2026 RecipeBook. Все права защищены.</p>
      <div class="flex gap-4">
        <router-link to="/about" class="hover:text-orange-500">О проекте</router-link>
        <span class="hover:text-orange-500 cursor-pointer">Контакты</span>
        <a href="https://github.com" target="_blank" rel="noreferrer" class="hover:text-orange-500">GitHub</a>
      </div>
    </div>
  </footer>
</template>
