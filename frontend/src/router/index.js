import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
  },
  {
    path: '/companies',
    name: 'CompanyList',
    component: () => import('@/views/CompanyListView.vue'),
  },
  {
    path: '/companies/new',
    name: 'CompanyCreate',
    component: () => import('@/views/CompanyFormView.vue'),
  },
  {
    path: '/companies/:id',
    name: 'CompanyDetail',
    component: () => import('@/views/CompanyDetailView.vue'),
  },
  {
    path: '/companies/:id/edit',
    name: 'CompanyEdit',
    component: () => import('@/views/CompanyFormView.vue'),
  },
  {
    path: '/resumes',
    name: 'ResumeList',
    component: () => import('@/views/ResumeListView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
