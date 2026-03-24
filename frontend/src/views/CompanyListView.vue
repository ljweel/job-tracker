<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

const companies = ref([])
const filterStatus = ref('')

onMounted(async () => {
  const res = await api.get('/companies/')
  companies.value = res.data
})

const filtered = computed(() => {
  const sorted = [...companies.value].sort((a, b) => a.id - b.id)
  if (!filterStatus.value) return sorted
  return sorted.filter((c) => c.status === filterStatus.value)
})

async function deleteCompany(id) {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await api.delete(`/companies/${id}/`)
  companies.value = companies.value.filter((c) => c.id !== id)
}
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1>회사 관리</h1>
      <router-link to="/companies/new" class="btn btn-primary">+ 회사 등록</router-link>
    </div>

    <div class="filter-bar card" style="margin-bottom: 16px;">
      <label style="font-size:14px; margin-right:8px;">상태 필터:</label>
      <select v-model="filterStatus" style="width:auto;">
        <option value="">전체</option>
        <option>진행중</option>
        <option>최종통과</option>
        <option>불합격</option>
      </select>
    </div>

    <div class="card" v-if="filtered.length">
      <table class="table">
        <thead>
          <tr>
            <th>회사명</th>
            <th>포지션</th>
            <th>지원 경로</th>
            <th>상태</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td>
              <router-link :to="`/companies/${c.id}`">{{ c.company_name }}</router-link>
            </td>
            <td>{{ c.position }}</td>
            <td>{{ c.source }}</td>
            <td>
              <span v-if="c.status" class="badge" :class="{
                'badge-progress': c.status === '진행중',
                'badge-accepted': c.status === '최종통과',
                'badge-rejected': c.status === '불합격',
              }">{{ c.status }}</span>
              <span v-else class="badge badge-none">없음</span>
            </td>
            <td>
              <router-link :to="`/companies/${c.id}/edit`" class="btn btn-secondary btn-sm">수정</router-link>
              <button class="btn btn-danger btn-sm" @click="deleteCompany(c.id)">삭제</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="card empty-state" v-else>
      <p>등록된 회사가 없습니다.</p>
    </div>
  </div>
</template>

<style scoped>
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
.btn-sm {
  padding: 4px 10px;
  font-size: 12px;
}
.filter-bar {
  display: flex;
  align-items: center;
  padding: 12px 16px;
}
.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: #6b7280;
}
</style>
