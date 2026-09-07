<script setup>
import { onMounted, ref } from 'vue'
import { getStudents } from '../api/students'

const students = ref([])
const loading = ref(false)
const error = ref('')

async function loadStudents() {
  loading.value = true
  error.value = ''
  students.value = []

  try {
    const response = await getStudents()
    students.value = response.data.items || []
  } catch {
    error.value = 'Unable to load students. Please try again.'
    students.value = []
  } finally {
    loading.value = false
  }
}

function fullName(student) {
  return `${student.first_name} ${student.last_name}`
}

onMounted(loadStudents)
</script>

<template>
  <section class="list">
    <div v-if="loading" class="status">Loading students...</div>

    <div v-else-if="error" class="status status-error" role="alert">
      <p>{{ error }}</p>
      <button type="button" class="retry" @click="loadStudents">Retry</button>
    </div>

    <div v-else-if="students.length === 0" class="status">No students found.</div>

    <table v-else class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Enrollment Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ fullName(student) }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.date_of_birth }}</td>
          <td class="status-cell">{{ student.enrollment_status }}</td>
          <td class="actions">
            <span class="placeholder">Edit</span>
            <span class="placeholder">Delete</span>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.list {
  margin-top: 1.5rem;
}

.status {
  padding: 1.25rem;
  background: #fff;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
}

.status-error {
  color: #8a1f11;
  border-color: #f0c2bb;
  background: #fff6f5;
}

.retry {
  margin-top: 0.5rem;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
  overflow: hidden;
}

th,
td {
  text-align: left;
  padding: 0.75rem 0.9rem;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

th {
  background: #f0f2f5;
  font-weight: 600;
}

.status-cell {
  text-transform: capitalize;
}

.actions {
  display: flex;
  gap: 0.75rem;
  color: #888;
}

.placeholder {
  font-size: 0.85rem;
}
</style>
