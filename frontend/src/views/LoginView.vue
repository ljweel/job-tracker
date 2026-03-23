<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch {
    error.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>아이디</label>
          <input v-model="username" type="text" required autofocus />
        </div>
        <div class="form-group">
          <label>비밀번호</label>
          <input v-model="password" type="password" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary" style="width:100%">로그인</button>
      </form>
      <p class="auth-link">
        계정이 없으신가요? <router-link to="/register">회원가입</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.auth-card {
  width: 100%;
  max-width: 400px;
}
.auth-card h1 {
  font-size: 24px;
  margin-bottom: 24px;
  text-align: center;
}
.error {
  color: #e63946;
  font-size: 14px;
  margin-bottom: 12px;
}
.auth-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #6b7280;
}
</style>
