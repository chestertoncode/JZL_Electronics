<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '@/services/api'
type Order = { id: number; product_name: string; quantity: number; total_price: string; status: string; created_at: string }
const orders = ref<Order[]>([])
const error = ref('')
const loading = ref(true)
onMounted(async () => {
  try { const { data } = await api.get('/orders/'); orders.value = Array.isArray(data) ? data : (data.results || []) }
  catch { error.value = 'Could not load orders. Please log in again.' }
  finally { loading.value = false }
})
</script>
<template>
  <section class="max-w-5xl mx-auto px-5 py-12">
    <p class="text-orange-600 font-bold text-sm">ACCOUNT</p><h1 class="text-4xl font-black mt-1">My orders</h1><p class="text-gray-500 mt-2">Review your recent purchases.</p>
    <p v-if="loading" class="mt-8 text-gray-500">Loading orders...</p>
    <p v-else-if="error" class="mt-8 p-4 rounded-xl bg-orange-50 text-orange-800">{{ error }}</p>
    <div v-else-if="orders.length" class="mt-8 overflow-x-auto bg-white border rounded-2xl">
      <table class="w-full text-sm text-left"><thead class="bg-gray-50 text-gray-600"><tr><th class="p-4">Order</th><th class="p-4">Product</th><th class="p-4">Qty</th><th class="p-4">Total</th><th class="p-4">Status</th><th class="p-4">Date</th></tr></thead>
        <tbody><tr v-for="order in orders" :key="order.id" class="border-t"><td class="p-4">#{{ order.id }}</td><td class="p-4 font-semibold">{{ order.product_name }}</td><td class="p-4">{{ order.quantity }}</td><td class="p-4">₱{{ Number(order.total_price).toFixed(2) }}</td><td class="p-4"><span class="bg-orange-50 text-orange-700 rounded-full px-3 py-1">{{ order.status }}</span></td><td class="p-4">{{ new Date(order.created_at).toLocaleDateString() }}</td></tr></tbody>
      </table>
    </div>
    <div v-else class="mt-8 bg-white border rounded-2xl p-10 text-center"><p class="text-gray-500">You haven't placed any orders yet.</p><RouterLink to="/products" class="inline-block mt-4 text-orange-600 font-bold">Browse products →</RouterLink></div>
  </section>
</template>
