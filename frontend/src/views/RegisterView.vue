<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const displayName = ref('')
const username = ref('')
const password = ref('')
const error = ref('')
const busy = ref(false)
const auth = useAuthStore()
const router = useRouter()
async function submit() {
  error.value = ''
  if (password.value.length < 8) { error.value = 'Use at least 8 characters for your password.'; return }
  busy.value = true
  try { await auth.register(username.value, password.value, displayName.value); router.push('/') }
  catch (e: any) {
    const data = e?.response?.data
    error.value = data ? Object.values(data).flat().join(' ') : 'Registration failed. Check your connection and try again.'
  } finally { busy.value = false }
}
</script>
<template>
  <section class="max-w-md mx-auto px-5 py-14">
    <div class="bg-white border border-gray-200 rounded-2xl p-7 md:p-9 shadow-sm">
      <p class="text-orange-600 font-bold text-sm">JOIN JZL</p><h1 class="text-3xl font-black mt-2">Create an account</h1><p class="text-gray-500 mt-2">Register to place orders and track purchases.</p>
      <form @submit.prevent="submit" class="mt-7 space-y-4">
        <div><label class="block text-sm font-bold mb-1">Display name</label><input v-model="displayName" required maxlength="100" class="w-full border rounded-lg px-3 py-3 outline-none focus:ring-2 focus:ring-orange-400" /></div>
        <div><label class="block text-sm font-bold mb-1">Username</label><input v-model="username" required minlength="3" maxlength="150" autocomplete="username" class="w-full border rounded-lg px-3 py-3 outline-none focus:ring-2 focus:ring-orange-400" /></div>
        <div><label class="block text-sm font-bold mb-1">Password</label><input v-model="password" type="password" required minlength="8" autocomplete="new-password" class="w-full border rounded-lg px-3 py-3 outline-none focus:ring-2 focus:ring-orange-400" /><p class="text-xs text-gray-500 mt-1">Use at least 8 characters.</p></div>
        <p v-if="error" class="bg-red-50 text-red-700 rounded-lg p-3 text-sm">{{ error }}</p>
        <button :disabled="busy" class="w-full bg-orange-500 hover:bg-orange-600 disabled:opacity-60 text-white rounded-lg py-3 font-bold">{{ busy ? 'Creating account...' : 'Create account' }}</button>
      </form>
      <p class="text-center text-sm text-gray-500 mt-6">Already registered? <RouterLink to="/login" class="text-orange-600 font-bold">Log in</RouterLink></p>
    </div>
  </section>
</template>
