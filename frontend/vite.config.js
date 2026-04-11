import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    host: true, // Позволяет Vite слушать внешний хост
    watch: {
      usePolling: true, // Важно для Docker: без этого изменения файлов не видны
    }
  },
})
