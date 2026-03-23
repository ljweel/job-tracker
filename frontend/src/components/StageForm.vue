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
  resume: null,
})

const stageOptions = ['서류', '코테', '커피챗', '면접', '과제']
const stageEntries = ref([{ id: 1, stage: '서류' }])
let stageEntrySeq = 2

// 이력서 관련
const resumes = ref([])
const showResumeForm = ref(false)
const resumeForm = ref({ label: '', modified_date: '' })
const resumePdf = ref(null)
const resumeError = ref('')

const hasDocument = computed(() => {
  return stageEntries.value.some((entry) => entry.stage === '서류')
})

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
    form.value = { ...props.initial }
  }
  await loadResumes()
})

async function loadResumes() {
  const res = await api.get('/resumes/')
  resumes.value = res.data
}

function addStageEntry() {
  stageEntries.value.push({ id: stageEntrySeq++, stage: '서류' })
}

function removeStageEntry(id) {
  if (stageEntries.value.length === 1) return
  stageEntries.value = stageEntries.value.filter((entry) => entry.id !== id)
}

function onResumePdfChange(e) {
  resumePdf.value = e.target.files[0] || null
}

async function handleAddResume() {
  resumeError.value = ''
  const fd = new FormData()
  fd.append('label', resumeForm.value.label)
  fd.append('modified_date', resumeForm.value.modified_date)
  if (resumePdf.value) {
    fd.append('pdf_file', resumePdf.value)
  }
  try {
    const res = await api.post('/resumes/', fd)
    await loadResumes()
    form.value.resume = res.data.id
    showResumeForm.value = false
    resumeForm.value = { label: '', modified_date: '' }
    resumePdf.value = null
  } catch (e) {
    const data = e.response?.data
    resumeError.value = data ? Object.values(data).flat().join(' ') : '이력서 등록에 실패했습니다.'
  }
}

function handleSubmit() {
  const selectedStages = stageEntries.value.map((entry) => entry.stage)
  const data = {
    stage: selectedStages,
    method: form.value.method,
    date: form.value.date,
    result: form.value.result,
    memo: form.value.memo,
    resume: selectedStages.includes('서류') ? form.value.resume : null,
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

        <!-- 서류 선택 시 이력서 선택 영역 -->
        <div v-if="hasDocument" class="form-group">
          <label>제출 이력서</label>
          <div class="resume-select-area">
            <select v-model="form.resume">
              <option :value="null">선택 안 함</option>
              <option v-for="r in resumes" :key="r.id" :value="r.id">{{ r.label }}</option>
            </select>
            <button type="button" class="btn btn-secondary btn-sm" @click="showResumeForm = !showResumeForm">
              {{ showResumeForm ? '취소' : '+ 이력서 추가' }}
            </button>
          </div>

          <!-- 인라인 이력서 등록 폼 -->
          <div v-if="showResumeForm" class="inline-resume-form">
            <div class="form-group">
              <label>버전명 / 라벨</label>
              <input v-model="resumeForm.label" required placeholder="예: v3 - 백엔드 강조" />
            </div>
            <div class="form-group">
              <label>수정 날짜</label>
              <input v-model="resumeForm.modified_date" type="date" required />
            </div>
            <div class="form-group">
              <label>PDF 파일</label>
              <input type="file" accept=".pdf" @change="onResumePdfChange" />
            </div>
            <p v-if="resumeError" class="error">{{ resumeError }}</p>
            <button type="button" class="btn btn-primary btn-sm" @click="handleAddResume">이력서 등록</button>
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
.resume-select-area {
  display: flex;
  gap: 8px;
  align-items: center;
}
.resume-select-area select {
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
.inline-resume-form {
  margin-top: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}
.inline-resume-form .form-group {
  margin-bottom: 10px;
}
.inline-resume-form label {
  font-size: 13px;
}
.error {
  color: #e63946;
  font-size: 13px;
  margin-bottom: 8px;
}
</style>
