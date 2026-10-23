import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProductsView from '@/views/ProductsView.vue'
import ProductFormView from '@/views/ProductFormView.vue'
import OrdersView from '@/views/OrdersView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/products', component: ProductsView },
    { path: '/products/new', component: ProductFormView, meta: { requiresStaff: true } },
    { path: '/products/:id/edit', component: ProductFormView, meta: { requiresStaff: true } },
    { path: '/orders', component: OrdersView, meta: { requiresAuth: true } },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) return '/login'
  if (to.meta.requiresStaff && !auth.isStaff) return '/'
})

export default router
