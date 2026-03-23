<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const form = ref({
  company_name: '',
  position: '',
  source: '기타',
  job_url: '',
  memo: '',
})
const error = ref('')

onMounted(async () => {
  if (isEdit.value) {
    const res = await api.get(`/companies/${route.params.id}/`)
    const { company_name, position, source, job_url, memo } = res.data
    form.value = { company_name, position, source, job_url, memo }
  }
})

async function handleSubmit() {
  error.value = ''
  try {
    if (isEdit.value) {
      await api.put(`/companies/${route.params.id}/`, form.value)
    } else {
      await api.post('/companies/', form.value)
    }
    router.push('/companies')
  } catch (e) {
    const data = e.response?.data
    if (data) {
      error.value = Object.values(data).flat().join(' ')
    } else {
      error.value = '저장에 실패했습니다.'
    }
  }
}
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1>{{ isEdit ? '회사 수정' : '회사 등록' }}</h1>
    </div>

    <div class="card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>회사명</label>
          <input v-model="form.company_name" required />
        </div>
        <div class="form-group">
          <label>포지션</label>
          <input v-model="form.position" required />
        </div>
        <div class="form-group">
          <label>지원 경로</label>
          <select v-model="form.source">
            <option>사람인</option>
            <option>원티드</option>
            <option>공식홈페이지</option>
            <option>추천</option>
            <option>기타</option>
          </select>
        </div>
        <div class="form-group">
          <label>공고 링크</label>
          <input v-model="form.job_url" type="url" placeholder="https://" />
        </div>
        <div class="form-group">
          <label>메모</label>
          <textarea v-model="form.memo" rows="3"></textarea>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ isEdit ? '수정' : '등록' }}</button>
          <button type="button" class="btn btn-secondary" @click="router.back()">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.form-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}
.error {
  color: #e63946;
  font-size: 14px;
  margin-bottom: 12px;
}
</style>
