import axios from 'axios'
import router from './router'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

// Request interceptor: добавляем Authorization токен ко всем запросам
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: обрабатываем 401 Unauthorized централизованно
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Очищаем токен и перенаправляем на логин
      localStorage.removeItem('token')
      // Если пользователь не на странице логина/регистрации — перенаправляем
      if (!router.currentRoute.value.meta?.public) {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default api