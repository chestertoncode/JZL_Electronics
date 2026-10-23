<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import ProductCard from '@/components/ProductCard.vue'
import { useAuthStore } from '@/stores/auth'

type Product = { id: number; name: string; description: string; quantity: number; price: string | number; image?: string | null }
const products = ref<Product[]>([])
const loading = ref(true)
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

onMounted(async () => {
  try {
    const { data } = await api.get('/products/')
    products.value = Array.isArray(data) ? data.slice(0, 3) : (data.results || []).slice(0, 3)
  } catch { error.value = 'Could not load products. Make sure the Django backend is running.' }
  finally { loading.value = false }
})

async function order(id: number) {
  if (!auth.isLoggedIn) return router.push('/login')
  try {
    await api.post('/orders/', { product: id, quantity: 1 })
    alert('Order placed successfully!')
  } catch (e: any) { alert(e?.response?.data?.detail || 'Could not place order. Please check stock and try again.') }
}
</script>

<template>
  <div>
    <section class="bg-gray-900 text-white">
      <div class="max-w-6xl mx-auto px-5 py-16 md:py-24 grid md:grid-cols-2 gap-10 items-center">
        <div>
          <p class="text-orange-400 font-bold uppercase tracking-widest text-sm">Your electronics partner</p>
          <h1 class="text-4xl md:text-6xl font-black leading-tight mt-4">Components for your next big idea.</h1>
          <p class="text-gray-300 mt-5 text-lg max-w-xl">Explore electronic components, check availability, and manage your orders in one simple place.</p>
          <div class="flex flex-wrap gap-3 mt-8">
            <RouterLink to="/products" class="bg-orange-500 hover:bg-orange-600 px-6 py-3 rounded-lg font-bold">Browse products</RouterLink>
            <RouterLink to="/register" class="border border-gray-500 hover:bg-gray-800 px-6 py-3 rounded-lg font-bold">Join JZL</RouterLink>
          </div>
        </div>
        <div class="rounded-3xl bg-gray-800 p-8 md:p-12">
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-white text-gray-900 rounded-2xl p-5"><div class="text-4xl">🔧</div><p class="font-bold mt-3">Tools & parts</p><p class="text-sm text-gray-500 mt-1">For practical projects</p></div>
            <div class="bg-orange-500 rounded-2xl p-5"><div class="text-4xl">💡</div><p class="font-bold mt-3">Build ideas</p><p class="text-sm text-orange-50 mt-1">One component at a time</p></div>
            <div class="bg-gray-700 rounded-2xl p-5"><div class="text-4xl">📦</div><p class="font-bold mt-3">Track stock</p><p class="text-sm text-gray-300 mt-1">See available quantity</p></div>
            <div class="bg-white text-gray-900 rounded-2xl p-5"><div class="text-4xl">🛒</div><p class="font-bold mt-3">Easy orders</p><p class="text-sm text-gray-500 mt-1">Keep orders organized</p></div>
          </div>
        </div>
      </div>
    </section>
    <section class="max-w-6xl mx-auto px-5 py-14">
      <div class="flex items-end justify-between gap-4 mb-7">
        <div><p class="text-orange-600 font-bold text-sm">SHOP THE CATALOG</p><h2 class="text-3xl font-extrabold mt-1">Featured products</h2></div>
        <RouterLink to="/products" class="font-bold text-orange-600">View all →</RouterLink>
      </div>
      <p v-if="loading" class="text-gray-500">Loading products...</p>
      <p v-else-if="error" class="bg-orange-50 text-orange-800 p-4 rounded-xl">{{ error }}</p>
      <div v-else-if="products.length" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <ProductCard v-for="product in products" :key="product.id" :product="product" @order="order" />
      </div>
      <div v-else class="bg-white border rounded-2xl p-8 text-center">
        <p class="text-2xl">📦</p><h3 class="font-bold mt-2">No products yet</h3>
        <p class="text-gray-500 mt-1">Log in as a staff user and add your first item.</p>
      </div>
    </section>
  </div>
</template>
