<script setup>
import AppNav from './components/AppNav.vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
</script>

<template>
  <AppNav v-if="auth.isLoggedIn" />
  <router-view />
</template>
