<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

const companies = ref([])

onMounted(async () => {
  const res = await api.get('/companies/')
  companies.value = res.data
})

const statusCounts = computed(() => {
  const counts = { '진행중': 0, '최종통과': 0, '불합격': 0 }
  companies.value.forEach((c) => {
    if (c.status && counts[c.status] !== undefined) counts[c.status]++
  })
  return counts
})

const totalCount = computed(() => companies.value.length)

const recentCompanies = computed(() => {
  return [...companies.value]
    .sort((a, b) => {
      const dateA = a.last_stage_date || a.first_stage_date || ''
      const dateB = b.last_stage_date || b.first_stage_date || ''
      return dateB.localeCompare(dateA)
    })
    .slice(0, 10)
})

function formatSupportPeriod(company) {
  const start = company.first_stage_date
  const end = company.last_stage_date
  if (!start) return '-'
  const startText = new Date(start).toLocaleDateString('ko-KR')
  if (!end || start === end) return startText
  const endText = new Date(end).toLocaleDateString('ko-KR')
  return `${startText} ~ ${endText}`
}
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1>대시보드</h1>
    </div>

    <div class="stats-grid">
      <div class="stat-card card">
        <div class="stat-label">전체 지원</div>
        <div class="stat-value">{{ totalCount }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">진행중</div>
        <div class="stat-value progress">{{ statusCounts['진행중'] }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">최종통과</div>
        <div class="stat-value accepted">{{ statusCounts['최종통과'] }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">불합격</div>
        <div class="stat-value rejected">{{ statusCounts['불합격'] }}</div>
      </div>
    </div>

    <div class="card" style="margin-top: 24px" v-if="companies.length">
      <h2 style="font-size: 18px; margin-bottom: 16px;">최근 지원 현황</h2>
      <table class="table">
        <thead>
          <tr>
            <th>회사명</th>
            <th>포지션</th>
            <th>지원 기간</th>
            <th>상태</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in recentCompanies" :key="c.id">
            <td>
              <router-link :to="`/companies/${c.id}`">{{ c.company_name }}</router-link>
            </td>
            <td>{{ c.position }}</td>
            <td>{{ formatSupportPeriod(c) }}</td>
            <td>
              <span v-if="c.status" class="badge" :class="{
                'badge-progress': c.status === '진행중',
                'badge-accepted': c.status === '최종통과',
                'badge-rejected': c.status === '불합격',
              }">{{ c.status }}</span>
              <span v-else class="badge badge-none">없음</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card empty-state" v-else>
      <p>아직 지원한 회사가 없습니다.</p>
      <router-link to="/companies/new" class="btn btn-primary">첫 회사 등록하기</router-link>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.stat-card {
  text-align: center;
}
.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 32px;
  font-weight: 700;
}
.stat-value.progress { color: #1d4ed8; }
.stat-value.accepted { color: #065f46; }
.stat-value.rejected { color: #991b1b; }

.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}
.table th {
  font-size: 13px;
  color: #6b7280;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: #6b7280;
}
.empty-state p {
  margin-bottom: 16px;
}
</style>
