<script setup lang="ts">
defineProps<{ name: string; manaCost: number; description: string }>()
</script>

<template>
  <div class="rounded-xl border p-4">
    <p class="font-bold text-orange-600">{{ name }}</p>
    <p class="text-gray-600">{{ description }}</p>
    <p class="text-sm text-gray-500">Mana cost: {{ manaCost }}</p>
    <slot />
  </div>
</template>
