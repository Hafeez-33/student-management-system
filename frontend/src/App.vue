<script setup>
import StudentList from './components/StudentList.vue'
</script>

<template>
  <main class="app">
    <h1>Student Management System</h1>
    <p class="subtitle">Students</p>
    <StudentList />
  </main>
</template>

<style>
:root {
  font-family: system-ui, Segoe UI, sans-serif;
  color: #1a1a1a;
  background: #f7f7f7;
}

body {
  margin: 0;
}

.app {
  max-width: 60rem;
  margin: 2.5rem auto;
  padding: 0 1rem 2rem;
}

.subtitle {
  color: #555;
  margin-top: 0;
}
</style>
