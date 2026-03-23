<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

const resumes = ref([])
const showForm = ref(false)
const editing = ref(null)

const form = ref({ modified_date: '' })
const pdfFile = ref(null)
const error = ref('')

const resumesByDateAsc = computed(() =>
  [...resumes.value].sort((a, b) => {
    const dateA = a.modified_date || ''
    const dateB = b.modified_date || ''
    if (dateA === dateB) return a.id - b.id
    return dateA.localeCompare(dateB)
  })
)

function resumeNumberById(id) {
  const idx = resumesByDateAsc.value.findIndex((r) => r.id === id)
  return idx >= 0 ? idx + 1 : null
}

function nextResumeNumber() {
  return resumesByDateAsc.value.length + 1
}

function resumeNumberLabel(id) {
  const n = resumeNumberById(id)
  return n ? `${n}번째 이력서` : '이력서'
}

async function load() {
  const res = await api.get('/resumes/')
  resumes.value = res.data
}

onMounted(load)

function openAdd() {
  editing.value = null
  form.value = { modified_date: '' }
  pdfFile.value = null
  error.value = ''
  showForm.value = true
}

function openEdit(resume) {
  editing.value = resume
  form.value = {
    modified_date: resume.modified_date,
  }
  pdfFile.value = null
  error.value = ''
  showForm.value = true
}

function onFileChange(e) {
  pdfFile.value = e.target.files[0] || null
}

async function handleSubmit() {
  error.value = ''
  const fd = new FormData()
  const number = editing.value ? (resumeNumberById(editing.value.id) || 1) : nextResumeNumber()
  fd.append('label', `${number}번째 이력서`)
  fd.append('modified_date', form.value.modified_date)
  if (pdfFile.value) {
    fd.append('pdf_file', pdfFile.value)
  }
  try {
    if (editing.value) {
      await api.put(`/resumes/${editing.value.id}/`, fd)
    } else {
      await api.post('/resumes/', fd)
    }
    showForm.value = false
    await load()
  } catch (e) {
    const data = e.response?.data
    error.value = data ? Object.values(data).flat().join(' ') : '저장에 실패했습니다.'
  }
}

async function deleteResume(id) {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await api.delete(`/resumes/${id}/`)
  await load()
}
</script>

<template>
  <div class="container resume-container">
    <div class="page-header">
      <button class="btn btn-primary" @click="openAdd">+ 이력서 등록</button>
    </div>

    <div v-if="resumes.length" class="resume-grid">
      <div v-for="r in resumes" :key="r.id" class="card resume-card">
        <div class="resume-header">
          <strong>{{ resumeNumberLabel(r.id) }}</strong>
        </div>
        <div class="resume-date">{{ r.modified_date }}</div>
        <div class="resume-actions">
          <a v-if="r.pdf_url" :href="r.pdf_url" target="_blank" class="btn btn-secondary btn-sm">PDF 보기</a>
          <button class="btn btn-secondary btn-sm" @click="openEdit(r)">수정</button>
          <button class="btn btn-danger btn-sm" @click="deleteResume(r.id)">삭제</button>
        </div>
      </div>
    </div>
    <div v-else class="card empty-state">
      <p>등록된 이력서가 없습니다.</p>
    </div>

    <!-- Modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal card">
        <h3>{{ editing ? '이력서 수정' : '이력서 등록' }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>수정 날짜</label>
            <input v-model="form.modified_date" type="date" required />
          </div>
          <div class="form-group">
            <label>PDF 파일</label>
            <input type="file" accept=".pdf" @change="onFileChange" />
          </div>
          <p v-if="error" class="error">{{ error }}</p>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">저장</button>
            <button type="button" class="btn btn-secondary" @click="showForm = false">취소</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.resume-container {
  width: 100%;
  max-width: 1200px;
}

.resume-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.resume-card {
  border-left: 4px solid #10b981;
}
.resume-header {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}
.resume-date {
  font-size: 14px;
  color: #6b7280;
}
.resume-actions {
  display: flex;
  gap: 6px;
  margin-top: 12px;
}
.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}
.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: #6b7280;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  width: 100%;
  max-width: 480px;
}
.modal h3 {
  font-size: 18px;
  margin-bottom: 20px;
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
