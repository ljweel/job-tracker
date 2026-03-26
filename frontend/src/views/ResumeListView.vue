<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const documents = ref([])
const showForm = ref(false)
const editingType = ref(null)
const editingDoc = ref(null)

const form = ref({ label: '', modified_date: '' })
const pdfFile = ref(null)
const error = ref('')

const docTypes = ['이력서', '포트폴리오', '자기소개서']

function docsByType(type) {
  return documents.value.filter((d) => d.doc_type === type)
}

async function load() {
  const res = await api.get('/resumes/')
  documents.value = res.data
}

onMounted(load)

function openAdd(type) {
  editingType.value = type
  editingDoc.value = null
  form.value = { label: '', modified_date: '' }
  pdfFile.value = null
  error.value = ''
  showForm.value = true
}

function openEdit(doc) {
  editingType.value = doc.doc_type
  editingDoc.value = doc
  form.value = { label: doc.label, modified_date: doc.modified_date }
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
  fd.append('doc_type', editingType.value)
  fd.append('label', form.value.label)
  fd.append('modified_date', form.value.modified_date)
  if (pdfFile.value) {
    fd.append('pdf_file', pdfFile.value)
  }
  try {
    if (editingDoc.value) {
      await api.put(`/resumes/${editingDoc.value.id}/`, fd)
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

async function deleteDoc(id) {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await api.delete(`/resumes/${id}/`)
  await load()
}
</script>

<template>
  <div class="container doc-container">
    <div class="page-header">
      <h1 style="font-size: 20px; font-weight: 700;">서류 관리</h1>
    </div>

    <div class="doc-sections">
      <div v-for="type in docTypes" :key="type" class="doc-section">
        <div class="section-header">
          <h2>{{ type }}</h2>
          <button class="btn btn-primary btn-sm" @click="openAdd(type)">+ {{ type }} 등록</button>
        </div>

        <div v-if="docsByType(type).length" class="doc-list">
          <div v-for="doc in docsByType(type)" :key="doc.id" class="card doc-card">
            <div class="doc-info">
              <div class="doc-label">{{ doc.label }}</div>
              <div class="doc-date">수정일: {{ doc.modified_date }}</div>
            </div>
            <div class="doc-actions">
              <a v-if="doc.pdf_url" :href="doc.pdf_url" target="_blank" class="btn btn-secondary btn-sm">PDF 보기</a>
              <button class="btn btn-secondary btn-sm" @click="openEdit(doc)">수정</button>
              <button class="btn btn-danger btn-sm" @click="deleteDoc(doc.id)">삭제</button>
            </div>
          </div>
        </div>
        <div v-else class="doc-empty">
          <p>등록된 {{ type }}가 없습니다.</p>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal card">
        <h3>{{ editingDoc ? `${editingType} 수정` : `${editingType} 등록` }}</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>제목</label>
            <input v-model="form.label" placeholder="미입력 시 파일명으로 자동 설정" />
          </div>
          <div class="form-group">
            <label>수정 날짜</label>
            <input v-model="form.modified_date" type="date" required />
          </div>
          <div class="form-group">
            <label>PDF 파일</label>
            <input type="file" accept=".pdf" @change="onFileChange" />
            <p v-if="editingDoc?.pdf_url" class="helper-text">기존 파일이 있습니다. 새 파일을 선택하면 교체됩니다.</p>
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
.doc-container {
  width: 100%;
  max-width: 1200px;
}
.doc-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.section-header h2 {
  font-size: 16px;
  font-weight: 600;
}
.doc-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.doc-card {
  border-left: 4px solid #10b981;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.doc-label {
  font-size: 15px;
  font-weight: 500;
}
.doc-date {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}
.doc-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}
.doc-empty {
  text-align: center;
  padding: 20px;
  color: #9ca3af;
  font-size: 14px;
  background: #f9fafb;
  border-radius: 8px;
}
.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}
.helper-text {
  color: #6b7280;
  font-size: 12px;
  margin-top: 4px;
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
