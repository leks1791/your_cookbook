import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
      meta: { public: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { public: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: { public: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/recipes',
      name: 'recipes',
      component: () => import('../views/Recipes.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/recipes/:id',
      name: 'recipe-detail',
      component: () => import('../views/RecipeDetail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/recipes/new',
      name: 'recipe-create',
      component: () => import('../views/RecipeForm.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/recipes/:id/edit',
      name: 'recipe-edit',
      component: () => import('../views/RecipeForm.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tags',
      name: 'tags',
      component: () => import('../views/TagsPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tags/:tag',
      name: 'recipes-by-tag',
      component: () => import('../views/RecipesByTag.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login' }
  }

  if (
    auth.isAuthenticated &&
    ['home', 'login', 'register'].includes(String(to.name))
  ) {
    return { name: 'dashboard' }
  }
})

export default router
