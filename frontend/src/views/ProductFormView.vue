<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
const route = useRoute()
const router = useRouter()
const editing = !!route.params.id
const name = ref('')
const description = ref('')
const price = ref('')
const quantity = ref('0')
const image = ref<File | null>(null)
const error = ref('')
const busy = ref(false)
onMounted(async () => {
  if (!editing) return
  try {
    const { data } = await api.get(`/products/${route.params.id}/`)
    name.value = data.name; description.value = data.description; price.value = String(data.price); quantity.value = String(data.quantity)
  } catch { error.value = 'Unable to load this product. You may not have permission.' }
})
function pickImage(event: Event) { image.value = (event.target as HTMLInputElement).files?.[0] || null }
async function submit() {
  error.value = ''
  if (Number(price.value) < 0 || Number(quantity.value) < 0) { error.value = 'Price and quantity cannot be negative.'; return }
  const body = new FormData()
  body.append('name', name.value); body.append('description', description.value)
  body.append('price', price.value); body.append('quantity', quantity.value)
  if (image.value) body.append('image', image.value)
  busy.value = true
  try {
    if (editing) await api.patch(`/products/${route.params.id}/`, body)
    else await api.post('/products/', body)
    router.push('/products')
  } catch (e: any) { error.value = e?.response?.data ? Object.values(e.response.data).flat().join(' ') : 'Save failed. Make sure you are logged in as staff.' }
  finally { busy.value = false }
}
</script>
<template>
  <section class="max-w-2xl mx-auto px-5 py-12">
    <div class="bg-white border rounded-2xl p-7 md:p-9">
      <p class="text-orange-600 font-bold text-sm">INVENTORY MANAGEMENT</p><h1 class="text-3xl font-black mt-2">{{ editing ? 'Edit product' : 'Add a product' }}</h1><p class="text-gray-500 mt-2">Fill in the component details below.</p>
      <form @submit.prevent="submit" class="space-y-5 mt-7">
        <div><label class="block font-bold text-sm mb-1">Product name</label><input v-model="name" required maxlength="160" class="w-full border rounded-lg p-3 outline-none focus:ring-2 focus:ring-orange-400" /></div>
        <div><label class="block font-bold text-sm mb-1">Description</label><textarea v-model="description" rows="3" class="w-full border rounded-lg p-3 outline-none focus:ring-2 focus:ring-orange-400"></textarea></div>
        <div class="grid sm:grid-cols-2 gap-4">
          <div><label class="block font-bold text-sm mb-1">Price (₱)</label><input v-model="price" type="number" min="0" step="0.01" required class="w-full border rounded-lg p-3 outline-none focus:ring-2 focus:ring-orange-400" /></div>
          <div><label class="block font-bold text-sm mb-1">Quantity in stock</label><input v-model="quantity" type="number" min="0" step="1" required class="w-full border rounded-lg p-3 outline-none focus:ring-2 focus:ring-orange-400" /></div>
        </div>
        <div><label class="block font-bold text-sm mb-1">Product image</label><input type="file" accept="image/*" @change="pickImage" class="w-full border rounded-lg p-3" /><p class="text-xs text-gray-500 mt-1">Optional. Select an image from your computer.</p></div>
        <p v-if="error" class="bg-red-50 text-red-700 rounded-lg p-3 text-sm">{{ error }}</p>
        <div class="flex gap-3"><button :disabled="busy" class="flex-1 bg-orange-500 hover:bg-orange-600 text-white rounded-lg py-3 font-bold">{{ busy ? 'Saving...' : 'Save product' }}</button><button type="button" @click="router.push('/products')" class="border rounded-lg px-5 py-3 font-bold">Cancel</button></div>
      </form>
    </div>
  </section>
</template>
