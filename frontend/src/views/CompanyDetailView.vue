<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import StageForm from '@/components/StageForm.vue'

const route = useRoute()
const router = useRouter()
const company = ref(null)
const showStageForm = ref(false)
const editingStage = ref(null)

async function load() {
  const res = await api.get(`/companies/${route.params.id}/`)
  company.value = res.data
}

onMounted(load)

function openAddStage() {
  editingStage.value = null
  showStageForm.value = true
}

function openEditStage(stage) {
  editingStage.value = { ...stage }
  showStageForm.value = true
}

async function handleSaveStage(data) {
  const companyId = route.params.id
  if (editingStage.value?.id) {
    await api.put(`/companies/${companyId}/stages/${editingStage.value.id}/`, data)
  } else {
    await api.post(`/companies/${companyId}/stages/`, data)
  }
  showStageForm.value = false
  await load()
}

async function deleteStage(stageId) {
  if (!confirm('이 전형 절차를 삭제하시겠습니까?')) return
  await api.delete(`/companies/${route.params.id}/stages/${stageId}/`)
  await load()
}

const sortedStages = computed(() => {
  if (!company.value?.stages) return []
  return [...company.value.stages].sort((a, b) => a.date.localeCompare(b.date))
})

function statusBadgeClass(status) {
  return {
    'badge-progress': status === '진행중',
    'badge-accepted': status === '최종통과',
    'badge-rejected': status === '불합격',
    'badge-none': !status,
  }
}

function resultBadgeClass(result) {
  return {
    'badge-progress': result === '진행중',
    'badge-pass': result === '통과',
    'badge-accepted': result === '최종통과',
    'badge-rejected': result === '불합격',
  }
}

function stageList(stageValue) {
  const expand = (value) => {
    if (Array.isArray(value)) return value.flatMap(expand)
    if (typeof value === 'string') {
      const trimmed = value.trim()
      if (!trimmed) return []
      try {
        const parsed = JSON.parse(trimmed)
        if (Array.isArray(parsed)) return parsed.flatMap(expand)
      } catch (_) {
        // Keep backward compatibility with plain string values.
      }
      return [value]
    }
    if (value == null) return []
    return [String(value)]
  }
  return expand(stageValue)
}
</script>

<template>
  <div class="container" v-if="company">
    <div class="page-header">
      <h1>{{ company.company_name }}</h1>
      <div style="display:flex; gap:8px;">
        <router-link :to="`/companies/${company.id}/edit`" class="btn btn-secondary">수정</router-link>
        <button class="btn btn-secondary" @click="router.push('/companies')">목록</button>
      </div>
    </div>

    <div class="card info-card">
      <div class="info-grid">
        <div><span class="info-label">포지션</span>{{ company.position }}</div>
        <div><span class="info-label">지원 경로</span>{{ company.source }}</div>
        <div>
          <span class="info-label">상태</span>
          <span class="badge" :class="statusBadgeClass(company.status)">{{ company.status || '없음' }}</span>
        </div>
        <div>
          <span class="info-label">공고 링크</span>
          <a v-if="company.job_url" :href="company.job_url" target="_blank" rel="noopener">링크 열기</a>
          <span v-else style="color:#9ca3af;">없음</span>
        </div>
      </div>
      <div v-if="company.memo" class="info-memo">
        <span class="info-label">메모</span>
        <p>{{ company.memo }}</p>
      </div>
    </div>

    <div style="margin-top:32px;">
      <div class="page-header">
        <h2 style="font-size:20px;">전형 절차</h2>
        <button class="btn btn-primary" @click="openAddStage">+ 전형 절차 추가</button>
      </div>

      <div v-if="sortedStages.length" class="timeline">
        <div v-for="stage in sortedStages" :key="stage.id" class="timeline-item card">
          <div class="timeline-header">
            <div class="stage-badges">
              <span v-for="(name, idx) in stageList(stage.stage)" :key="`${stage.id}-${idx}`" class="stage-pill">
                {{ name }}
              </span>
            </div>
            <span class="badge" :class="resultBadgeClass(stage.result)">{{ stage.result }}</span>
          </div>
          <div class="timeline-meta">
            <span>{{ stage.date }}</span>
            <span>{{ stage.method }}</span>
            <template v-if="stage.documents_detail">
              <template v-for="doc in stage.documents_detail" :key="doc.id">
                <a
                  v-if="doc.pdf_url"
                  :href="doc.pdf_url"
                  target="_blank"
                  rel="noopener"
                  class="resume-tag resume-link"
                >
                  [{{ doc.doc_type }}] {{ doc.label }}
                </a>
                <span v-else class="resume-tag">[{{ doc.doc_type }}] {{ doc.label }}</span>
              </template>
            </template>
          </div>
          <p v-if="stage.memo" class="timeline-memo">{{ stage.memo }}</p>
          <div class="timeline-actions">
            <button class="btn btn-secondary btn-sm" @click="openEditStage(stage)">수정</button>
            <button class="btn btn-danger btn-sm" @click="deleteStage(stage.id)">삭제</button>
          </div>
        </div>
      </div>
      <div v-else class="card empty-state">
        <p>등록된 전형 절차가 없습니다.</p>
      </div>
    </div>

    <StageForm
      v-if="showStageForm"
      :initial="editingStage"
      @save="handleSaveStage"
      @cancel="showStageForm = false"
    />
  </div>
</template>

<style scoped>
.info-card {
  margin-bottom: 8px;
}
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.info-label {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 4px;
}
.info-memo {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e9ecef;
}
.info-memo p {
  white-space: pre-wrap;
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.timeline-item {
  border-left: 4px solid #4361ee;
}
.timeline-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  justify-content: space-between;
}
.stage-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.stage-pill {
  background: #e2e8f0;
  color: #334155;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
}
.timeline-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #6b7280;
}
.timeline-memo {
  margin-top: 8px;
  font-size: 14px;
  white-space: pre-wrap;
  color: #374151;
}
.timeline-actions {
  display: flex;
  gap: 6px;
  margin-top: 12px;
}
.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}
.resume-tag {
  background: #dbeafe;
  color: #1d4ed8;
  padding: 1px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}
.resume-link {
  text-decoration: none;
}
.resume-link:hover {
  background: #bfdbfe;
}
.empty-state {
  text-align: center;
  padding: 32px 20px;
  color: #6b7280;
}
</style>
