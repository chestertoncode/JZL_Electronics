<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const username = ref('')
const password = ref('')
const error = ref('')
const busy = ref(false)
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
async function submit() {
  error.value = ''; busy.value = true
  try { await auth.login(username.value, password.value); router.push(typeof route.query.next === 'string' ? route.query.next : '/') }
  catch (e: any) { error.value = e?.response?.data?.detail || 'Login failed. Check your username and password, and confirm the backend is running.' }
  finally { busy.value = false }
}
</script>
<template>
  <section class="max-w-md mx-auto px-5 py-14">
    <div class="bg-white border border-gray-200 rounded-2xl p-7 md:p-9 shadow-sm">
      <p class="text-orange-600 font-bold text-sm">WELCOME BACK</p><h1 class="text-3xl font-black mt-2">Log in</h1><p class="text-gray-500 mt-2">Access your JZL Electronics account.</p>
      <form @submit.prevent="submit" class="mt-7 space-y-4">
        <div><label class="block text-sm font-bold mb-1">Username</label><input v-model="username" required autocomplete="username" class="w-full border rounded-lg px-3 py-3 focus:ring-2 focus:ring-orange-400 outline-none" /></div>
        <div><label class="block text-sm font-bold mb-1">Password</label><input v-model="password" type="password" required autocomplete="current-password" class="w-full border rounded-lg px-3 py-3 focus:ring-2 focus:ring-orange-400 outline-none" /></div>
        <p v-if="error" class="bg-red-50 text-red-700 rounded-lg p-3 text-sm">{{ error }}</p>
        <button :disabled="busy" class="w-full bg-orange-500 hover:bg-orange-600 disabled:opacity-60 text-white rounded-lg py-3 font-bold">{{ busy ? 'Logging in...' : 'Log in' }}</button>
      </form>
      <p class="text-center text-sm text-gray-500 mt-6">No account? <RouterLink to="/register" class="text-orange-600 font-bold">Register here</RouterLink></p>
    </div>
  </section>
</template>
