import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guest: true },
  },
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

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!to.meta.guest && !auth.isLoggedIn) {
    return { name: 'Login' }
  }
  if (to.meta.guest && auth.isLoggedIn) {
    return { name: 'Dashboard' }
  }
})

export default router
