<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function handleRegister() {
  error.value = ''
  try {
    await axios.post('/api/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    router.push('/login')
  } catch (e) {
    const data = e.response?.data
    if (data) {
      error.value = Object.values(data).flat().join(' ')
    } else {
      error.value = '회원가입에 실패했습니다.'
    }
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h1>회원가입</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>아이디</label>
          <input v-model="username" type="text" required autofocus />
        </div>
        <div class="form-group">
          <label>이메일</label>
          <input v-model="email" type="email" />
        </div>
        <div class="form-group">
          <label>비밀번호 (8자 이상)</label>
          <input v-model="password" type="password" required minlength="8" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary" style="width:100%">회원가입</button>
      </form>
      <p class="auth-link">
        이미 계정이 있으신가요? <router-link to="/login">로그인</router-link>
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
