<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

const props = defineProps({
  initial: { type: Object, default: null },
})
const emit = defineEmits(['save', 'cancel'])

const isEdit = computed(() => !!props.initial)

const form = ref({
  stage: '서류',
  method: '온라인',
  date: '',
  result: '진행중',
  memo: '',
})

const stageOptions = ['서류', '코테', '커피챗', '면접', '과제']
const stageEntries = ref([{ id: 1, stage: '서류' }])
let stageEntrySeq = 2

// 서류 관련
const allDocuments = ref([])
const selectedDocs = ref({ '이력서': null, '포트폴리오': null, '자기소개서': null })
const docTypeOptions = ['이력서', '포트폴리오', '자기소개서']

const showDocForm = ref(false)
const docForm = ref({ doc_type: '이력서', label: '', modified_date: '' })
const docPdf = ref(null)
const docError = ref('')

const hasDocument = computed(() => {
  return stageEntries.value.some((entry) => entry.stage === '서류')
})

function docsByType(type) {
  return allDocuments.value.filter((d) => d.doc_type === type)
}

function normalizeStageList(stageValue) {
  const expand = (value) => {
    if (Array.isArray(value)) return value.flatMap(expand)
    if (typeof value === 'string') {
      const trimmed = value.trim()
      if (!trimmed) return []
      try {
        const parsed = JSON.parse(trimmed)
        if (Array.isArray(parsed)) return parsed.flatMap(expand)
      } catch (_) {
        // Legacy fallback for non-JSON single value.
      }
      return [value]
    }
    if (value == null) return []
    return [String(value)]
  }

  const normalized = expand(stageValue)
  return normalized.length ? normalized : ['서류']
}

onMounted(async () => {
  if (props.initial) {
    const stageList = normalizeStageList(props.initial.stage)
    stageEntries.value = stageList.map((stage) => ({ id: stageEntrySeq++, stage }))
    form.value = {
      stage: props.initial.stage,
      method: props.initial.method,
      date: props.initial.date,
      result: props.initial.result,
      memo: props.initial.memo,
    }
    if (props.initial.documents_detail) {
      for (const doc of props.initial.documents_detail) {
        selectedDocs.value[doc.doc_type] = doc.id
      }
    }
  }
  await loadDocuments()
})

async function loadDocuments() {
  const res = await api.get('/resumes/')
  allDocuments.value = res.data
}

function addStageEntry() {
  stageEntries.value.push({ id: stageEntrySeq++, stage: '서류' })
}

function removeStageEntry(id) {
  if (stageEntries.value.length === 1) return
  stageEntries.value = stageEntries.value.filter((entry) => entry.id !== id)
}

function onDocPdfChange(e) {
  docPdf.value = e.target.files[0] || null
}

async function handleAddDoc() {
  docError.value = ''
  const fd = new FormData()
  fd.append('doc_type', docForm.value.doc_type)
  fd.append('label', docForm.value.label)
  fd.append('modified_date', docForm.value.modified_date)
  if (docPdf.value) {
    fd.append('pdf_file', docPdf.value)
  }
  try {
    const res = await api.post('/resumes/', fd)
    await loadDocuments()
    selectedDocs.value[res.data.doc_type] = res.data.id
    showDocForm.value = false
    docForm.value = { doc_type: '이력서', label: '', modified_date: '' }
    docPdf.value = null
  } catch (e) {
    const data = e.response?.data
    docError.value = data ? Object.values(data).flat().join(' ') : '서류 등록에 실패했습니다.'
  }
}

function handleSubmit() {
  const selectedStages = stageEntries.value.map((entry) => entry.stage)
  const documentIds = selectedStages.includes('서류')
    ? Object.values(selectedDocs.value).filter((id) => id != null)
    : []
  const data = {
    stage: selectedStages,
    method: form.value.method,
    date: form.value.date,
    result: form.value.result,
    memo: form.value.memo,
    document_ids: documentIds,
  }
  emit('save', data)
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('cancel')">
    <div class="modal card">
      <h3>{{ isEdit ? '전형 절차 수정' : '전형 절차 추가' }}</h3>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>형태</label>
          <div class="stage-entry-list">
            <div v-for="(entry, idx) in stageEntries" :key="entry.id" class="stage-entry-row">
              <span class="stage-entry-index">{{ idx + 1 }}</span>
              <select v-model="entry.stage">
                <option v-for="s in stageOptions" :key="s">{{ s }}</option>
              </select>
              <button type="button" class="btn btn-secondary btn-sm" @click="removeStageEntry(entry.id)">삭제</button>
            </div>
            <button type="button" class="btn btn-secondary btn-sm" @click="addStageEntry">+ 형태 추가</button>
            <p class="helper-text">동일한 형태를 여러 번 선택해도 한 전형 절차에 함께 저장됩니다.</p>
          </div>
        </div>

        <!-- 서류 선택 시 종류별 서류 선택 -->
        <div v-if="hasDocument" class="form-group">
          <label>제출 서류</label>
          <div class="doc-select-list">
            <div v-for="dt in docTypeOptions" :key="dt" class="doc-select-row">
              <span class="doc-type-label">{{ dt }}</span>
              <select v-model="selectedDocs[dt]">
                <option :value="null">선택 안 함</option>
                <option v-for="d in docsByType(dt)" :key="d.id" :value="d.id">{{ d.label }}</option>
              </select>
            </div>
          </div>
          <button type="button" class="btn btn-secondary btn-sm" style="margin-top:8px;" @click="showDocForm = !showDocForm">
            {{ showDocForm ? '취소' : '+ 새 서류 등록' }}
          </button>

          <!-- 인라인 서류 등록 폼 -->
          <div v-if="showDocForm" class="inline-doc-form">
            <div class="form-group">
              <label>서류 종류</label>
              <select v-model="docForm.doc_type">
                <option v-for="dt in docTypeOptions" :key="dt">{{ dt }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>제목</label>
              <input v-model="docForm.label" placeholder="미입력 시 파일명으로 자동 설정" />
            </div>
            <div class="form-group">
              <label>수정 날짜</label>
              <input v-model="docForm.modified_date" type="date" required />
            </div>
            <div class="form-group">
              <label>PDF 파일</label>
              <input type="file" accept=".pdf" @change="onDocPdfChange" />
            </div>
            <p v-if="docError" class="error">{{ docError }}</p>
            <button type="button" class="btn btn-primary btn-sm" @click="handleAddDoc">서류 등록</button>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>방식</label>
            <select v-model="form.method">
              <option>온라인</option>
              <option>오프라인</option>
            </select>
          </div>
          <div class="form-group">
            <label>결과</label>
            <select v-model="form.result">
              <option>진행중</option>
              <option>통과</option>
              <option>최종통과</option>
              <option>불합격</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>날짜</label>
          <input v-model="form.date" type="date" required />
        </div>
        <div class="form-group">
          <label>메모</label>
          <textarea v-model="form.memo" rows="3"></textarea>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">저장</button>
          <button type="button" class="btn btn-secondary" @click="emit('cancel')">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
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
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
}
.modal h3 {
  font-size: 18px;
  margin-bottom: 20px;
}
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
.doc-select-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.doc-select-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.doc-type-label {
  width: 70px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  flex-shrink: 0;
}
.doc-select-row select {
  flex: 1;
}
.stage-entry-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.stage-entry-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.stage-entry-row select {
  flex: 1;
}
.stage-entry-index {
  width: 18px;
  text-align: right;
  color: #6b7280;
  font-size: 13px;
}
.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
  white-space: nowrap;
}
.helper-text {
  color: #6b7280;
  font-size: 12px;
}
.inline-doc-form {
  margin-top: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}
.inline-doc-form .form-group {
  margin-bottom: 10px;
}
.inline-doc-form label {
  font-size: 13px;
}
.error {
  color: #e63946;
  font-size: 13px;
  margin-bottom: 8px;
}
</style>
