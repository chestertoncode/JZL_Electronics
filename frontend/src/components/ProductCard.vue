<script setup lang="ts">
defineProps<{ product: { id: number; name: string; description: string; quantity: number; price: string | number; image?: string | null } }>()
const emit = defineEmits<{ order: [id: number] }>()
const imageUrl = (path?: string | null) => path ? (path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`) : ''
</script>

<template>
  <article class="bg-white border border-gray-200 rounded-2xl overflow-hidden hover:shadow-md transition">
    <div class="h-44 bg-orange-50 flex items-center justify-center overflow-hidden">
      <img v-if="product.image" :src="imageUrl(product.image)" :alt="product.name" class="w-full h-full object-cover" />
      <div v-else class="text-5xl">🔌</div>
    </div>
    <div class="p-5">
      <h3 class="font-bold text-lg">{{ product.name }}</h3>
      <p class="text-gray-500 text-sm mt-2 min-h-10">{{ product.description || 'Electronic component' }}</p>
      <div class="flex justify-between items-center mt-4 gap-3">
        <span class="text-orange-600 font-extrabold text-xl">₱{{ Number(product.price).toLocaleString('en-PH', { minimumFractionDigits: 2 }) }}</span>
        <span class="text-xs text-gray-500">{{ product.quantity }} in stock</span>
      </div>
      <button @click="emit('order', product.id)" :disabled="product.quantity < 1" class="w-full mt-4 rounded-lg bg-gray-900 text-white py-2.5 font-semibold hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed">Place order</button>
    </div>
  </article>
</template>
