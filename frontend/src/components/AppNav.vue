<template>
  <nav class="navbar">
    <div class="nav-inner">
      <router-link to="/" class="nav-brand">JobTracker</router-link>
      <div class="nav-links">
        <router-link to="/">대시보드</router-link>
        <router-link to="/companies">회사 관리</router-link>
        <router-link to="/resumes">서류 관리</router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid #e9ecef;
  padding: 0 16px;
}
.nav-inner {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}
.nav-brand {
  font-size: 18px;
  font-weight: 700;
  color: #4361ee;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}
.nav-links a {
  font-size: 14px;
  color: #495057;
  font-weight: 500;
}
.nav-links a.router-link-active {
  color: #4361ee;
}
</style>
