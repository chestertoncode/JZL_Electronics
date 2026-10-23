<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import ProductCard from '@/components/ProductCard.vue'
import { useAuthStore } from '@/stores/auth'
type Product = { id: number; name: string; description: string; quantity: number; price: string | number; image?: string | null }
const products = ref<Product[]>([])
const search = ref('')
const loading = ref(true)
const error = ref('')
const auth = useAuthStore()
const router = useRouter()
const filtered = computed(() => products.value.filter(p => `${p.name} ${p.description}`.toLowerCase().includes(search.value.toLowerCase())))
onMounted(async () => {
  try { const { data } = await api.get('/products/'); products.value = Array.isArray(data) ? data : (data.results || []) }
  catch { error.value = 'Could not load products. Start the Django backend and refresh.' }
  finally { loading.value = false }
})
async function order(id: number) {
  if (!auth.isLoggedIn) return router.push('/login')
  try { await api.post('/orders/', { product: id, quantity: 1 }); alert('Order placed successfully!') }
  catch (e: any) { alert(e?.response?.data?.detail || 'Order failed. Check product stock.') }
}
async function removeProduct(id: number) {
  if (!confirm('Delete this product?')) return
  try { await api.delete(`/products/${id}/`); products.value = products.value.filter(p => p.id !== id) }
  catch { alert('Unable to delete product. Make sure you are logged in as staff.') }
}
</script>
<template>
  <section class="max-w-6xl mx-auto px-5 py-10">
    <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-5">
      <div><p class="text-orange-600 font-bold text-sm">OUR CATALOG</p><h1 class="text-4xl font-black mt-1">Electronics products</h1><p class="text-gray-500 mt-2">Find the components you need for your projects.</p></div>
      <RouterLink v-if="auth.isStaff" to="/products/new" class="bg-orange-500 text-white rounded-lg px-5 py-3 font-bold text-center">+ Add product</RouterLink>
    </div>
    <input v-model="search" placeholder="Search components..." class="mt-8 w-full md:max-w-md rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-orange-400" />
    <p v-if="loading" class="mt-8 text-gray-500">Loading products...</p>
    <p v-else-if="error" class="mt-8 bg-orange-50 p-4 rounded-xl text-orange-800">{{ error }}</p>
    <div v-else-if="filtered.length" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      <div v-for="product in filtered" :key="product.id">
        <ProductCard :product="product" @order="order" />
        <div v-if="auth.isStaff" class="flex gap-2 mt-2">
          <RouterLink :to="`/products/${product.id}/edit`" class="flex-1 text-center border rounded-lg py-2 font-semibold hover:bg-gray-100">Edit</RouterLink>
          <button @click="removeProduct(product.id)" class="flex-1 border border-red-200 text-red-600 rounded-lg py-2 font-semibold hover:bg-red-50">Delete</button>
        </div>
      </div>
    </div>
    <div v-else class="mt-8 rounded-xl border bg-white p-10 text-center text-gray-500">No matching products found.</div>
  </section>
</template>
