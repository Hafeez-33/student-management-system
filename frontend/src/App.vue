<script setup>
// Import proves the API service layer is wired and loadable
import { getStudents } from './api/students'
</script>

<template>
  <main class="app">
    <h1>Student Management System</h1>
    <p>Vue frontend is running. Student UI will be added next.</p>
    <p class="meta">API service loaded: {{ typeof getStudents === 'function' ? 'yes' : 'no' }}</p>
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
  max-width: 40rem;
  margin: 3rem auto;
  padding: 0 1rem;
}

.meta {
  color: #555;
  font-size: 0.9rem;
}
</style>
