<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
const auth = useAuthStore()
const router = useRouter()
function signOut() {
  auth.logout()
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-white border-b border-gray-200 sticky top-0 z-20">
      <nav class="max-w-6xl mx-auto px-5 py-4 flex flex-wrap items-center justify-between gap-4">
        <RouterLink to="/" class="flex items-center gap-2 font-extrabold text-xl">
          <span class="bg-orange-500 text-white rounded-lg px-2 py-1">JZL</span>
          <span>Electronics</span>
        </RouterLink>
        <div class="flex flex-wrap items-center gap-4 text-sm font-semibold">
          <RouterLink to="/" class="hover:text-orange-600">Home</RouterLink>
          <RouterLink to="/products" class="hover:text-orange-600">Products</RouterLink>
          <RouterLink v-if="auth.isLoggedIn" to="/orders" class="hover:text-orange-600">My Orders</RouterLink>
          <RouterLink v-if="auth.isStaff" to="/products/new" class="hover:text-orange-600">Add Product</RouterLink>
          <template v-if="auth.isLoggedIn">
            <span class="text-gray-500">Hi, {{ auth.user?.display_name || auth.user?.username }}</span>
            <button @click="signOut" class="rounded-lg bg-gray-900 px-4 py-2 text-white hover:bg-gray-700">Log out</button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="hover:text-orange-600">Log in</RouterLink>
            <RouterLink to="/register" class="rounded-lg bg-orange-500 px-4 py-2 text-white hover:bg-orange-600">Create account</RouterLink>
          </template>
        </div>
      </nav>
    </header>
    <main class="flex-1"><RouterView /></main>
    <footer class="bg-gray-900 text-gray-300 mt-12">
      <div class="max-w-6xl mx-auto px-5 py-7 flex flex-wrap justify-between gap-3 text-sm">
        <span>© 2026 JZL Electronics</span>
        <span>CPE Elective 2 • Electronics Components Store</span>
      </div>
    </footer>
  </div>
</template>
